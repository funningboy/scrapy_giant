# -*- coding: utf-8 -*-

import unittest
import time
import threading
import time
from datetime import datetime, date

from test.test_start import TestTwseId
from handler.iddb_handler import *

class TestTwseIdDBQuery(TestTwseId):

    def setUp(self):
        super(TestTwseIdDBQuery, self).setUp()

    def tearDown(self):
        super(TestTwseIdDBQuery, self).tearDown()

    def test_on_run(self):
        dbhandler = TwseIdDBHandler()
        self.assertTrue(dbhandler.stock.get_id(u'鴻海') == u'2317')
        self.assertTrue(dbhandler.stock.get_name(u'2317') == u'鴻海')
        ids = [id for id in dbhandler.stock.get_ids(debug=False, limit=10, opt='twse')]
        nms = [nm for nm in dbhandler.stock.get_names(debug=False, limit=10, opt='twse')]
        print zip(ids, nms)

# traderid
#        self.assertTrue(dbhandler.trader.get_id(u'美林') == '1590')
#        self.assertTrue(dbhandler.trader.get_name('1590') == u'美林')
#        ids = [id for id in dbhandler.trader.get_ids(debug=False, limit=10, opt='twse')]
#        nms = [nm for nm in dbhandler.trader.get_names(debug=False, limit=10, opt='twse')]
#        print zip(ids, nms)

if __name__ == '__main__':
    unittest.main()
