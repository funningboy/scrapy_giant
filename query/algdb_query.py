

class BaseAlgDBQuery(object):

    def __init__(self):
        self._client = connect_mongodb_service()
        self._db = self._client.twsedb
        self._coll = self._client.twsedb.


class SuperManAlgDBQuery():

