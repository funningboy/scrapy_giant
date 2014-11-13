@celery.task(name='bin.tasks.run_alg_query')
def run_alg_query(hisdb, alg, starttime, endtime, stockids=[], traderids=[], debug=False):
    raise NotImplementedError
