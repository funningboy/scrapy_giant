# -*- coding: utf-8 -*-

# 1.please following these steps to  make sure the mongodb and celery services has started before this run.
# % export C_FORCE_ROOT=true
# % export DEBUG=true
# % mongod --dbpath tmp &
# % celery -A bin.tasks work -l info &

import timeit
from bin.tasks import *
from algorithm.tasks import *
from handler.iddb_handler import TwseIdDBHandler

def main():
    stockids = TwseIdDBHandler().stock.get_ids(debug=True)
    stockids = list(stockids)

    t = timeit.Timer()
    args = ('twsehistrader', 'INFO', 'twsehistrader.log', True, True)
    run_algorithm_service(*args)
    print "run trader scrapy using (%.4f)s/%d" % (t.timeit(), len(stockids))


if __name__ == '__main__':
    main()

