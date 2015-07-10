# -*- coding: utf-8 -*-

# need rank table to filter incoming data?

from workers.worker import DAGWorker

class GWorker(DAGWorker):

    _hisitems = [
        'stockitem',
        'traderitem',
        'credititem',
        'futureitem'
    ]

    _algitems = [
        'dualemaitem', 
        'btraderitem', 
        'bbanditem', 
        'kmeansitem'
    ]
    
    def __init__(self, **kwargs):
        super(GWorker, self).__init__(**kwargs)

    def _populate_items(self):
        methods = [
            self._populate_hisitem,
            self._populate_algitem
        ]
        return methods

    def _collect_incoming_kwargs(self, node):
        kwargs = dict(self.node[node]['ptr']._kwargs)
        for pre, cur in self.in_edges(node):
            if self.node[pre]['ptr'].status == 'finish':
                item = self.node[pre]['ptr'].retval
                for it in self._populate_items():
                    it(item, kwargs)

        self.node[node]['ptr'].update_kwargs(kwargs=kwargs)

    def _populate_hisitem(self, item, kwargs):  
        for name in self._hisitems:
            if name in item:
                if isinstance(item[name], list):
                    stockids = [i['stockid'].encode('utf-8') for i in item[name] if i['stockid']]
                    kwargs['stockids'] += stockids
                    kwargs['stockids'] = list(set(kwargs['stockids']))

                    if name in ['traderitem']:
                        traderids = [i['traderid'].encode('utf-8') for i in item[name] if i['traderid']]
                        kwargs['traderids'] += traderids
                        kwargs['traderids'] = list(set(kwargs['traderids']))
 
    def _populate_algitem(self, item, kwargs):
        for name in self._algitems:
            if name in item:
                if isinstance(item[name], list):
                    stockids = [i['stockid'] for i in item[name] if i['stockid']]
                    kwargs['stockids'] += stockids
                    kwargs['stockids'] = list(set(kwargs['stockids']))
        

 