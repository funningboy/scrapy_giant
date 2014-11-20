# -*- coding: utf-8 -*-

# 1.please following these steps to  make sure the mongodb and celery services has started before this run.
# % export C_FORCE_ROOT=true
# turn on debug mode
# % export DEBUG=true
## start mongodb as backend
# % mongod --dbpath tmp &
## start rabbitmq as broker
# sudo rabbitmq-server -detached
## start celery worker
# % celery -A bin.tasks work -l info &
# % celery -A handler.tasks work -l info &

import timeit
from datetime import datetime, timedelta
from bin.tasks import *
from handler.tasks import *
from handler.iddb_handler import TwseIdDBHandler

def main():
    stockids = TwseIdDBHandler().stock.get_ids(debug=True)
    stockids = list(stockids)

    # load payload
    args = ('twsehistrader', 'INFO', 'twsehistrader.log', True, True)
    run_scrapy_service.delay(*args).get()
    args = ('twsehisstock', 'INFO', 'twsehisstock.log', True, True)
    run_scrapy_service.delay(*args).get()

    t = timeit.Timer()
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    args = ('twse', starttime, endtime, ['2317'])
    cursor = run_hisstock_query.delay(*args).get()
    print cursor
    print "run stock 300d query using (%.4f)s" % (t.timeit())

#    t = timeit.Timer()
#    starttime = datetime.utcnow() - timedelta(days=300)
#    endtime = datetime.utcnow()
#    args = ('twse', starttime, endtime, ['2317'])
#    cursor = run_hisstock_query.delay(*args).get()
#    print cursor
#    print "run stock 300d query using (%.4f)s" % (t.timeit())



if __name__ == '__main__':
    main()
