# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

from algorithm.tasks import *

args = ('twse', 'twsedualem', starttime, endtime, limit, debug)
run_algorithm_service()
alg.run(*args)
algitem = alg.query_summary()
for it in algitem:
    print it.end_time, it.portfolio_value
alg = TwseDualemaAlg()
args = (starttime, endtime, ['2317'], [], 'totalvolume', 10, alg.to_detail)
alg.run(*args)
algitem = alg.query_detail()
for it in algitem:
    print it.time, it.open, it.portfolio_value

alg = TwseBestTraderAlg()
algs = (starttime, endtime, )
alg.run(*args)
algitem = alg.query_summary()
for it in algitem:
    print it.end_time, it.portfolio_value
alg = TwseDualemaAlg()
args = (starttime, endtime, ['2317', '2330', '1314'], ['1440'], 'totalvolume', 10, alg.to_detail)
alg.run(*args)
algitem = alg.query_detail()
for it in algitem:
    print it.time, it.open, it.portfolio_value


