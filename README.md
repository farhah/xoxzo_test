# xoxzo_test
make phone call using xoxzo api

### Install package

`git clone git@github.com:farhah/xoxzo_test.git`

`pip install xoxzo_test/dist/xoxzo-phonecall-0.1.tar.gz`


## Preparation

1. Install redis

`sudo apt-get install redis-server`

`sudo systemctl restart redis-server.service`

`sudo systemctl enable redis-server.service`

2. Instal supervisor

`sudo apt install supervisor`

`sudo touch /etc/supervisor/conf.d/djangorq.conf`

```
[program:myworker]
command= /home/farhah/.virtualenvs/p3/bin/python manage.py rqworker
stdout_logfile = /var/log/redis/redis-server.log

numprocs=1

directory=/path/to/project
user = farhah
environment=
        XOXZO_SID="VzaYbNeQncmSUPOw08rGBJH7yIXf6jEh",
        XOXZO_AUTH="bght4jfmsozi5yq6nlpa90x31urd27ke"
stopsignal=TERM

autostart=true
autorestart=true
```

3. Install nginx + gunicorn from `https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04`

## Prepare environment variable
add these lines into `/path/to/.virtualenv/virtual_env_name/bin/postactivate`
```python
XOXZO_SID=bght4jfmsozi5yq6nlpa90x31urd27ke
XOXZO_AUTH=VzaYbNeQncmSUPOw08rGBJH7yIXf6jEh
```


#### in settings.py of mezzanine project, add these lines:
```python

INSTALLED_APPS = (
    "xoxzo_call_api",
    "django_rq",
)

XOXZO_SID = os.getenv('XOXZO_SID')
XOXZO_AUTH = os.getenv('XOXZO_AUTH')
```

```python
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': '',
        'DEFAULT_TIMEOUT': 360,
    }
}
```

~~#### `sudo vi /etc/systemd/system/gunicorn.service`
under `[Service]`

~~`EnvironmentFile=/home/farhah/.virtualenvs/p3/bin/postactivate`



