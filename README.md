

https://www.quantopian.com/help#api-doco

Mac OS setup flow
0.1 install basic tools and env
```
pip install virtualenv
pip install -r requirements.txt
```

0.2 normal run
0.3 debug run
nose
Redis vs RabbitMQ
http://blog.langoor.mobi/django-celery-redis-vs-rabbitmq-message-broker/
sudo rabbitmq-server -detached
sudo rabbitmqctl stop
sudo mongod --dbpath ./tmp
export DJANGO_SETTINGS_MODULE=main.settings
export DJANGO_PROJECT_DIR=`pwd`
python manage.py celery worker --loglevel=info
run as celery task
broker=rabbitmq
backend=mongodb
```
mongod --dbpath data &
celery -A bin.tasks worker -l info
celery -A algorithm.tasks worker -l info
python manage.py syncdb
python manage.py test handler

python
>>> from bin.tasks import *
>>> from datetime import datetime, timedelta
>>> from handler.iddb_handler import TwseIdDBHandler
>>> args = ('twsehistrader', 'INFO', 'test.log', True, True)
>>> run_scrapy_service(*args)
>>> stockids = TwseIdDBHandler().stock.get_ids(debug=True)
>>> traderids = []
>>> agrs = ('twse', 'superman', datetime.utcnow() - timedelta(days=60), datetime.utcnow(), stockids, traderids, True)
>>> run_algorithm_service(*args)
>>>
>>> run_report_service()
