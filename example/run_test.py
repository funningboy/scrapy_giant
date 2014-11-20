# -*- coding: utf-8 -*-

# 1.please following these steps to  make sure the mongodb and celery services has started before this run.
# % export C_FORCE_ROOT=true
# % export DEBUG=true
# % mongod --dbpath tmp &
# % celery -A bin.tasks worker -l info &

import timeit
from bin.tasks import *

def main():
    r = add.delay(1, 2).get()
    print r

#    t = timeit.Timer()
#    args = ('twsehistrader', 'INFO', 'twsehistrader.log', True, True)
#    run_scrapy_service.delay(*args).get()
#    print "run trader scrapy using (%.4f)s" % (t.timeit())


if __name__ == '__main__':
    main()


