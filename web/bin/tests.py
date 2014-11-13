# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.test import TestCase

from bin.tasks import *
from query.iddb_query import (TwseIdDBQuery, OtcIdDBQuery)


class TeseScrapyService(TestCase):

    def test_on_run(self):
        args = (
            'twsehisstock',
            'INFO',
            "./log/%s_%s.log" % ('twsehisstock', datetime.today().strftime("%Y%m%d_%H%M")),
            True,
            True
        )
        result = run_scrapy_service.delay(*args)
        result.get()

class TestAlgorithmService(TestCase):

    def test_on_run(self):
        args = (
            'twse',
            'superman',
            datetime.utcnow() - timedelta(days=60),
            datetime.utcnow(),
            TwseIdDBQuery().get_stockids(debug=True),
            [],
            True
        )
        result = run_algorithm_service.delay(*args)
        print result.get()

#class TestHisStockDBQuery(TestCase):
#
#
#class TestHisTraderDBQuery(TestCase):
