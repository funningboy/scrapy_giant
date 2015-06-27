
from workers.worker import DAGWorker

class GiantWorker(DAGWorker):

    def __init__(self, **kwargs):
        super(GiantWorker, self).__init__()

    def _collect_incoming_kwargs(self, node):
        kwargs = dict(self.node[node]['ptr']._kwargs)

        for pre, cur in self.in_edges(node):
            if self.node[pre]['ptr'].status == 'finish':
                item = self.node[pre]['ptr'].retval

                populate_items = [
                    self._populate_hisitem,
                    self._populate_algitem,
                    self._populate_itemall,
                ]
                for it in populate_items:
                    it(item, kwargs)

        self.node[node]['ptr']._kwargs = kwargs

    def _populate_hisitem(self, item, kwargs):
        if 'stockitem' in item:
            if isinstance(item['stockitem'], list):
                stockids = [i['stockid'] for i in item['stockitem'] if i['stockid']]
                kwargs['stockids'] += stockids

        if 'traderitem' in item:
            if isinstance(item['traderitem'], list):
                traderids = [i['traderid'] for i in item['traderitem'] if i['traderid']]
                kwargs['traderids'] += traderids

                stockids = [i['stockid'] for i in item['traderitem'] if i['stockid']]
                kwargs['stockids'] += stockids

        if 'credititem' in item:
            if isinstance(item['credititem'], list):
                stockids = [i['stockid'] for i in item['credititem'] if i['stockid']]
                kwargs['stockids'] += stockids

        if 'futureitem' in item:
            if isinstance(item['futureitem'], list):
                stockids = [i['stockid'] for i in item['futureitem'] if i['stockid']]
                kwargs['stockids'] += stockids

    def _populate_algitem(self, item, kwargs):
        pass

    def _populate_itemall(self, item, kwargs):
        kwargs['stockids'] = list(set(kwargs['stockids']))
        kwargs['traderids'] = list(set(kwargs['traderids']))
 