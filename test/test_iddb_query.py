# -*- coding: utf-8 -*-

import unittest
import time
import threading
import time
from datetime import datetime, date

from test.test_start import *
from query.iddb_query import *

class TestTwseIdFrameQuery(TestTwseHisAll):

    def setUp(self):
        super(TestTwseIdFrameQuery, self).setUp()

    def tearDown(self):
        super(TestTwseIdFrameQuery, self).tearDown()

    def test_on_run(self):
        iddbq = TwseIdDBQuery()
        self.assertTrue(iddbq.get_stockid(u'鴻海') == u'2317')
        self.assertTrue(iddbq.get_stocknm(u'2317') == u'鴻海')

if __name__ == '__main__':
    unittest.main()
