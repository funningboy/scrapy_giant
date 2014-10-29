# -*- coding: utf-8 -*-

# from pandas.util.testing import assert_frame_equal, assert_series_equal
import unittest
import json
import threading
import pandas as pd
from bson.code import Code

from bin.mongodb_driver import *

class TestMongoDBDriver(unittest.TestCase):
    """ test MongoDBDriver
    """

    def setUp(self):
        # start mongodb service
        self._proc = start_mongodb_service()

    def test_on_run(self):
        client = connect_mongodb_service()
        # drop = clear database/collection
        client.drop_database('panda_frame_example')
        db = client.panda_frame_example
        db.drop_collection('collection')

        def wap_thread_insert():
            for i in xrange(2):
                # panda frame
                expframe = pd.DataFrame({
                    1: pd.Series(['sean', 30], index=['name', 'age']),
                    2: pd.Series(['john', 31], index=['name', 'age'])
                })
                # insert to mongodb
                records = json.loads(expframe.to_json()).values()
                postid = db.collection.insert(records)

        # multi thread insert
        threads = [threading.Thread(target=wap_thread_insert) for i in range(4)]
        [it.start() for it in threads]
        [it.join() for it in threads]

        self.assertEqual(db.collection.count(), 16)

        # # mongodb will resort it to give a new index token called '_id',
        #  so it doesn't work to compare the recovered data with original frame
        # self.assertTrue(assert_series_equal(rstframe['name'], expframe.T['name']))
        # # compare exp frame vs rst frame via numpy array
        # self.assertTrue((rstframe['name'].values == expframe.T['name'].values).all())
        # self.assertTrue((rstframe['age'].values == expframe.T['age'].values).all())

        def wap_thread_query_0():
            """ recover panda frame """
            # find
            cursor = db.collection.find({
                '$and': [
                    {'name': {'$eq': 'sean'}},
                    {'age': {'$gte': 20}},
                    {'age': {'$lte': 40}}]}).sort('_id', 1).limit(1)

            # recover
            expframe = pd.DataFrame(['sean', 30], index=['name', 'age'])
            rstframe = pd.DataFrame(list(cursor))
            # remove mongo index token '_id'
            self.assertFalse(rstframe.empty)
            if rstframe.empty:
                del rstframe['_id']

            # assert
            self.assertEqual(expframe.T['name'].values, rstframe['name'].values)
            self.assertEqual(expframe.T['age'].values, rstframe['age'].values)

        def wap_thread_query_1():
            """ Aggregation -> adv Map Reduce """

            imap = Code('\
                function () { \
                    var key = [this.name, this.age]; \
                    var value = { \
                        name : this.name, \
                        list_age : [], \
                        sum_age : this.age, \
                        count : 1, \
                        avg_age : 0 \
                    }; \
                    emit(key, value); \
                };')

            # sum of age
            ireduce = Code(' \
                function (key, values) { \
                    var redval = { \
                            name : this.name, \
                            list_age : [], \
                            sum_age : 0, \
                            count : 0, \
                            avg_age : 0 \
                        }; \
                     for (var i = 0; i < values.length; i++) { \
                        redval.sum_age += values[i].sum_age; \
                        redval.count += values[i].count; \
                        redval.list_age.push(values[i].sum_age); \
                    } \
                    return redval; \
                };')

            # map the new key, value after "map reduce" proc
            results = db.collection.map_reduce(imap, ireduce, 'results')
            cursor = results.find({'_id': {'$eq': 'sean'}}).sort('_id', 1).limit(1)
            self.assertTrue(isinstance(cursor[0]['value'], dict))
            mp = cursor[0]['value']
            self.assertEqual(mp['sum_age'], 240)
            self.assertEqual(mp['list_age'], [30]*8)

        def wap_thread_query_2():
            pass

        def wap_thread_query_3():
            pass

        def wap_thread_query(mode):
            if mode == 0:
                wap_thread_query_0()
            elif mode == 1:
                wap_thread_query_1()
            elif mode == 2:
                wap_thread_query_2()

        # multi thread query
        threads = [threading.Thread(target=wap_thread_query, args=(i,)) for i in range(4)]
        [it.start() for it in threads]
        [it.join() for it in threads]

    def tearDown(self):
        close_mongodb_service(self._proc)

if __name__ == '__main__':
    unittest.main()
#    # profile testcase
#    # >>> python -m memory_profiler mongodb.py
#    # >>> python -m cProfile mongodb.py
#    # as unittest.main()
#    test_classes_to_run = [TestMongoDBDriver]
#    loader = unittest.TestLoader()
#    suites_list = []
#    for test_class in test_classes_to_run:
#        suite = loader.loadTestsFromTestCase(test_class)
#        suites_list.append(suite)
#
#    def wap_unittest_run():
#        big_suite = unittest.TestSuite(suites_list)
#        runner = unittest.TextTestRunner()
#        runner.run(big_suite)
#
# only for memory_profiler used
#    @profile
#    def wap_profile_run():
#        wap_unittest_run()
#
#    wap_unittest_run()
