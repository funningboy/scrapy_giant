# -*- coding: utf-8 -*-

from algorithm.algdb_handler import *
from datetime import datetime, timedelta
from handler.tasks import *

starttime = datetime.utcnow() - timedelta(days=50)
endtime = datetime.utcnow()
alg = TwseDualemaAlg(debug=True)
item = alg.run(starttime, endtime, ['1101'], alg.to_detail)
print item
#alg = TwseBestTraderAlg(debug=True)
#item = alg.run(starttime, endtime, ['2317'], [], alg.to_detail)
#print item
#alg = TwseBBandsAlg(debug=True)
#item = alg.run(starttime, endtime, ['2317'], alg.to_detail)
#print item
alg = OtcDualemaAlg(debug=False)
item = alg.run(starttime, endtime, ['5371'], alg.to_detail)
print item
