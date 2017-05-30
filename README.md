# xoxzo_test
make phone call using xoxzo api

### terminal
export XOXZO_SID=bght4jfmsozi5yq6nlpa90x31urd27ke
export XOXZO_AUTH=VzaYbNeQncmSUPOw08rGBJH7yIXf6jEh


### in settings.py of mezzanine project, add these lines:
XOXZO_SID = os.getenv('XOXZO_SID')
XOXZO_AUTH = os.getenv('XOXZO_AUTH')

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': '',
        'DEFAULT_TIMEOUT': 360,
    }
}
