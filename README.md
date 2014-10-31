python
>>> from bin.tasks import *
>>> run_scrapy.delay("twsehistrader", True).get() # async get
>>> run_hisdb_query("twse", 2317, 1330, ).get() # as pandas frame back
