import requests, datetime, json
from sys          import stderr
from os.path      import basename, dirname, abspath, expanduser
from decimal      import Decimal
from json.decoder import JSONDecodeError
from redis        import Redis, ConnectionError
from coins        import *



class Base(object):

    _name                          = "base"
    _description                   = "Base Engine"
    _uri                           = "http://api.pricefetcher.com/BTCUSD"
    _coinpair                      = BTC_USD
    _timeout                       = 10
    _max_age                       = 30
    _max_time_without_price_change = 180 # zero means infinity
    _redis_expiration              = 3600


    @property
    def name(self):
        return self._name


    @property
    def description(self):
        return self._description


    @property
    def uri(self):
        return self._uri


    @property
    def coinpair(self):
        return self._coinpair


    @property
    def timeout(self):
        return self._timeout


    def _clean_output_values(self):
        self._price                 = None
        self._volume                = None
        self._timestamp             = None
        self._last_change_timestamp = None
        self._error                 = None
        self._time                  = None
        self._age                   = None


    def __init__(self, session=None, session_storage=None):

        app_dir  = dirname(dirname(abspath(__file__)))
        app_name = basename(app_dir)
        redis_conf_files = [expanduser("~") + '/.' + app_name + '/redis.json',
                            expanduser("~") + '/.' + app_name + '/redis_default.json',
                            app_dir + '/data/redis.json',
                            app_dir + '/data/redis_default.json']

        redis_conf = {}
        for file_ in redis_conf_files:
            try:
                with open(file_, 'r') as f:
                    redis_conf = json.load(f)
            except JSONDecodeError as e:
                print(f'Error in "{file_}", {str(e)}', file=stderr)
                exit(1)
            except Exception as e:
                redis_conf = {}
            if redis_conf:
                break
        
        self._redis_enable = redis_conf.get('enable', False)

        self._engine_session_id = app_name + '/' + self._name

        if self._redis_enable:

            redis_connection = {}

            for key, type_ in [('host',             str),
                               ('port',             int),
                               ('db',               int),
                               ('unix_socket_path', str)]:
                if key in redis_conf:
                    try:
                        redis_connection[key] = type_(redis_conf[key])
                    except Exception as e:
                        print(f'Error in "{file_}", {str(e)}', file=stderr)
                        exit(1)

            try:
                self._redis = Redis(**redis_connection)
                self._redis.ping()
            except Exception as e:
                print(f'Error in "{file_}", {str(e)}', file=stderr)
                exit(1)

        self._session_storage = session_storage

        self._session = session
        self._clean_output_values()


    @property
    def price(self):
        return self._price


    @property
    def volume(self):
        return self._volume


    @property
    def age(self):
        return self._age


    @property
    def max_age(self):
        return self._max_age


    @property
    def timestamp(self):
        return self._timestamp

    @property
    def last_change_timestamp(self):
        return self._last_change_timestamp

    @property
    def error(self):
        return self._error


    @property
    def time(self):
        return self._time


    @staticmethod
    def _name_from_file(_file):
        name = basename(_file)
        if name.endswith('.py'):
            name = name[:-3]
        return name


    @staticmethod
    def _now():
        return datetime.datetime.now().replace(microsecond=0)


    @staticmethod
    def _utcfromtimestamp(timestamp):
        return datetime.datetime.utcfromtimestamp(int(timestamp))


    def _map(self, data):
        return {
            'price':  data['last'],
            'volume': data['volume'],
            'timestamp': self._utcfromtimestamp(data['timestamp']) }


    def __bool__(self):
        return not(bool(self._error))


    def __str__(self):
        name  = '{} {}'.format(self.description, self.coinpair
            ) if self.description else self.name
        if self.price == None:
            return name
        value = self.price if self else self.error
        return '{} = {}'.format(name, value)


    @property
    def as_dict(self):
        out = {}
        for attr in [
            'coinpair',
            'description',
            'error',
            'name',
            'price',
            'timeout',
            'timestamp',
            'last_change_timestamp',
            'uri',
            'volume',
            'time',
            'age']:
            out[attr] = getattr(self, attr, None)
        out['ok'] = bool(self)
        return out


    @property
    def as_json(self):
        data = self.as_dict
        for k in data.keys():
            if k in data:
                v = data[k]
                if isinstance(v, Decimal):
                    data[k] = float(v)
                if isinstance(v, datetime.datetime):
                    data[k] = datetime.datetime.timestamp(v)
                elif v!=None and not(isinstance(v, (int, bool, float))):
                    data[k] = str(v)
        return json.dumps(data, indent=4, sort_keys=True)


    def __call__(self):

        start_time = datetime.datetime.now()

        get = requests.get if self._session==None else self._session.get

        self._clean_output_values()

        try:
            response = get(self.uri, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self._error = e
            return False
        except Exception as e:
            self._error = e
            return False

        if not response:
            self._error = "No response from server"
            return False

        if response.status_code != 200:
            self._error = "Response error (code {})".format(
                response.status_code)
            return False

        try:
            self._age = int(response.headers['age'])
        except ValueError:
            self._age = None
        except KeyError:
            self._age = None

        if self._age!=None and self._age > self._max_age:
            self._error = str(f"Response age error (age > {self._max_age})")
            return False

        try:
            response = response.json()
        except Exception:
            self._error = "Response format error (not JSON)"
            return False

        try:
            info = self._map(response)
            self._price = Decimal(str(info['price']))
        except Exception:
            self._error = "Engine error (bad mapping)"
            return False

        if 'timestamp' in info:
            if isinstance(info['timestamp'], datetime.datetime):
                self._timestamp = info['timestamp']
            else:
                self._error = "Engine error (bad mapping)"
                return False
        else:
            self._timestamp = self._now()
        self._last_change_timestamp = self._timestamp

        if 'volume' in info:
            try:
                self._volume = Decimal(str(info['volume']))
            except Exception:
                self._error = "Engine error (bad mapping)"
                return False
        else:
            self._volume = 0.0

        self._time = datetime.datetime.now() - start_time

        if self._redis_enable or isinstance(self._session_storage, dict):

            session_id = self._engine_session_id

            if self._max_time_without_price_change:

                if self._redis_enable:
                    try:
                        pre_data = json.loads(self._redis.get(session_id))
                    except Exception:
                        pre_data = {}
                elif isinstance(self._session_storage, dict):
                    try:
                        pre_data = self._session_storage[session_id]
                    except Exception:
                        pre_data = {}
                if not isinstance(pre_data, dict):
                    pre_data = {}

                try:
                    pre_last_change_timestamp = datetime.datetime.fromtimestamp(pre_data['last_change_timestamp'])
                except Exception:
                    pre_last_change_timestamp = None

                try:
                    pre_price = Decimal(pre_data['price'])
                except Exception:
                    pre_price = None

                if pre_price!=None and pre_last_change_timestamp!=None:
                    if pre_price==self._price:
                        self._last_change_timestamp = pre_last_change_timestamp
            
                max_time_without_price_change = datetime.timedelta(seconds=self._max_time_without_price_change)
                time_without_price_change     = datetime.datetime.now()-self._last_change_timestamp

                if time_without_price_change > max_time_without_price_change:
                    self._error = str(f"Too much time without price change (t > {max_time_without_price_change})")
                    return False

            if self._redis_enable:
                time = datetime.timedelta(seconds=self._redis_expiration)
                self._redis.setex(session_id, time, self.as_json)
            elif isinstance(self._session_storage, dict):
                self._session_storage[session_id] = self.as_dict

        return True

if __name__ == '__main__':
    print("File: {}, Ok!".format(repr(__file__)))
