
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
                    self._populate_algitem
                ]
                for it in populate_items:
                    it(item, kwargs)

        self.node[node]['ptr']._kwargs = kwargs

    def _populate_hisitem(self, item, kwargs):
        for name in ['stockitem', 'traderitem', 'credititem', 'futureitem']:
            if name in item:
                if isinstance(item[name], list):
                    stockids = [i['stockid'] for i in item[name] if i['stockid']]
                    kwargs['stockids'] += stockids
                    kwargs['stockids'] = list(set(kwargs['stockids']))

                    if name in ['traderitem']:
                        traderids = [i['traderid'] for i in item[name] if i['traderid']]
                        kwargs['traderids'] += traderids
                        kwargs['traderids'] = list(set(kwargs['traderids']))
         
    def _populate_algitem(self, item, kwargs):
        for name in ['dualemaitem', 'btraderitem', 'bbanditem', 'kmeansitem']:
            if name in item:
                if isinstance(item[name], list):
                    stockids = [i['stockid'] for i in item[name] if i['stockid']]
                    kwargs['stockids'] += stockids
                    kwargs['stockids'] = list(set(kwargs['stockids']))
        

 