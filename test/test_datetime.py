
# -*- coding: utf-8 -*-

import unittest
import os
from bson import json_util
import json
from datetime import datetime

from bin.mongodb_driver import *

class TestTimeStamp(unittest.TestCase):

    def setUp(self):
        if not has_mongodb_service():
            self._proc = start_mongodb_service()
        self._client = connect_mongodb_service()
        # clear db, collletion
        self._client.drop_database('time')
        self._db = self._client.time
        self._db.drop_collection('timecoll')
        self._coll = self._db.timecoll

    def test_on_run(self):
        date = datetime.strptime("%s" % ('2014-10-01'), "%Y-%m-%d")
        bulk = self._coll.initialize_ordered_bulk_op()
        bulk.insert({
            'date': date,
            'foo': 1
        })
        bulk.find({
            'date': date,
            'foo': 1
        }).update({
            '$set': {
                'ext': 1
            }
        })
        bulk.execute()

        cursor = self._coll.find()
        item = list(cursor)[0]
        stream = json.dumps(item, sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        if not has_mongodb_service():
            close_mongodb_service(self._proc)

if __name__ == '__main__':
    unittest.main()
