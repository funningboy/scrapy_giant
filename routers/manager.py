# -*- coding: utf-8 -*-

import yaml
import threading
import json
from bson import json_util
from datetime import datetime, timedelta
from workers.gworker import GiantWorker
from workers.nodes import Node
from handler.tasks import collect_hisitem

#from algorithm.tasks import collect_algitem

class Manager(threading.Thread):

    _run_queue = []
    _wait_queue = []
    _max_concurrent = 10

    def __init__(self):
        threading.Thread.__init__(self)

    @classmethod
    def parse_task(cls, path, kwargs={}):
        with open(path) as stream:
            try:
                stream = yaml.load(stream)
                assert(set(stream.keys()) == set(['kwargs', 'task', 'description']))
            except:
                print "loading %s fail" %(path)
                raise
            
            # collect_hisitem/target, collect_algitem/target
            parse_kwargs = [
                cls._parse_opt,
                cls._parse_target,
                cls._parse_starttime,
                cls._parse_endtime,
                cls._parse_stockids,
                cls._parse_traderids,
                cls._parse_base,
                cls._parse_order,
                cls._parse_callback,
                cls._parse_limit,
                cls._parse_cfg,
                cls._parse_debug
            ]        
            for it in parse_kwargs:
                it(stream['kwargs'], kwargs)        
            return stream

    @classmethod
    def _parse_opt(cls, okwargs, nkwargs={}):
        opt = None
        if 'opt' in nkwargs:
            try:
                opt = eval(nkwargs['opt'])
            except:
                opt = str(nkwargs['opt'])
                pass
        elif 'opt' in okwargs:
            try:
                opt = eval(okwargs['opt'])
            except:
                opt = str(okwargs['opt'])
                pass

        if opt: 
            okwargs['opt'] = opt
        else:
            print "parse opt fail"
            raise

    @classmethod
    def _parse_target(cls, okwargs, nkwargs={}):
        target = None
        if 'target' in nkwargs:
            try:
                target = eval(nkwargs['target'])
            except:
                target = str(nkwargs['target'])
                pass
        elif 'target' in okwargs:
            try:
                target = eval(okwargs['target'])
            except:
                target = str(okwargs['target'])
                pass

        if target:
            okwargs['target'] = target
        else:
            print "parse target fail"
            raise

    @classmethod
    def _parse_starttime(cls, okwargs, nkwargs={}):
        starttime = datetime.utcnow() - timedelta(days=30)
        if 'starttime' in nkwargs:
            try:
                starttime = eval(nkwargs['starttime'])
            except:
                starttime = nkwargs['starttime']
                pass
        elif 'starttime' in okwargs:
            try:
                starttime = eval(okwargs['endtime'])
            except:
                starttime = okwargs['endtime']
                pass

        if isinstance(starttime, datetime):
            okwargs['starttime'] = starttime 
        else:
            print "parse starttime fail"
            raise 

    @classmethod
    def _parse_endtime(cls, okwargs, nkwargs={}):
        endtime = datetime.utcnow()
        if 'endtime' in nkwargs:
            try:
                endtime = eval(nkwargs['endtime'])
            except:
                endtime = nkwargs['endtime']
                pass
        elif 'endtime' in okwargs:
            try:
                endtime = eval(okwargs['endtime'])
            except:
                endtime = okwargs['endtime']
                pass

        if isinstance(endtime, datetime):
            okwargs['endtime'] = endtime
        else:
            print "parse endtime fail"
            raise

    @classmethod
    def _parse_stockids(cls, okwargs, nkwargs={}):
        stockids = []
        if 'stockids' in nkwargs:
            try:
                stockids = eval(nkwargs['stockids'])
            except:
                stockids = list(nkwargs['stockids']) 
                pass
        elif 'stockids' in okwargs:
            try:
                stockids = eval(okwargs['stockids'])
            except:
                stockids = list(nkwargs['stockids'])
                pass

        if isinstance(stockids, list):
            okwargs['stockids'] = stockids
        else:
            print "parse stockids fail"
            raise

    @classmethod
    def _parse_traderids(cls, okwargs, nkwargs={}):
        traderids = []
        if 'traderids' in nkwargs:
            try:
                traderids = eval(nkwargs['traderids'])
            except:
                traderids = list(nkwargs['traderids'])
                pass
        elif 'traderids' in okwargs:
            try:
                traderids = eval(okwargs['traderids'])
            except:
                traderids = list(nkwargs['traderids'])
                pass

        if isinstance(traderids, list):
            okwargs['traderids'] = traderids
        else:
            print "parse traderids fail"
            raise

    @classmethod
    def _parse_base(cls, okwargs, nkwargs={}):
        pass

    @classmethod
    def _parse_order(cls, okwargs, nkwargs={}):
        order = []
        if 'order' in nkwargs:
            try:
                order = eval(nkwargs['order'])
            except:
                order = list(nkwargs['order'])
                pass
        elif 'order' in okwargs:
            try:
                order = eval(okwargs['order'])
            except:
                order = list(okwargs['order'])
                pass

        if isinstance(order, list):
            okwargs['order'] = order
        else:
            print "parse order fail"
            raise

    @classmethod
    def _parse_callback(cls, okwargs, nkwargs={}):
        pass

    @classmethod
    def _parse_limit(cls, okwargs, nkwargs={}):
        limit = 20
        if 'limit' in nkwargs:
            try:
                limit = eval(nkwargs['limit'])
            except:
                limit = int(nkwargs['limit'])
                pass
        elif 'limit' in okwargs:
            try:
                limit = eval(okwargs['lmit'])
            except:
                limit = int(okwargs['limit'])
                pass

        if isinstance(limit, int):
            okwargs['limit'] = limit
        else:
            print "parse limit fail"
            raise

    @classmethod
    def _parse_debug(cls, okwargs, nkwargs={}):
        try:
            #django.setting
            okwargs['debug'] = True
        except:
            print "parse debug fail"
            raise

    @classmethod
    def _parse_cfg(cls, okwargs, nkwargs={}):
        pass

    @classmethod
    def create_graphs(cls, path, priority=1):
        with open(path, 'r') as stream:
            stream = yaml.load(stream)
            assert(set(stream.keys()) == set(['Nodes', 'Edges']))

            G = GiantWorker()
            create_methods = [
                cls._create_edges,
                cls._create_nodes,
                cls._valid_graph,
                cls._start_to_run
            ]
            for it in create_methods:
                it(stream, G)

            task = {
                'priority': priority,
                'graph': G,
            }
            cls._wait_queue.append(task)

    @classmethod
    def update_graphs(cls, stream, graph):
        pass

    @classmethod
    def _del_nodes(cls, stream, graph):
        pass

    @classmethod
    def _create_nodes(cls, stream, graph):
        assert(isinstance(stream['Nodes'], list))
        for i, node in enumerate(stream['Nodes']):
            try:
                node = eval(node)
                task = eval(node['task'])
                n = Node(func=task, kwargs=node['kwargs'])
                graph.add_node(i, {'ptr': n})
            except:
                print "create graph.node %d fail" %(i)
                raise

    @classmethod
    def _create_edges(cls, stream, graph):
        assert(isinstance(stream['Edges'], list))
        for i, edge in enumerate(stream['Edges']):
            try:
                cur, nxt, weight = map(int, edge)
                graph.add_edge(cur, nxt, weight=weight)
            except:
                print "create graph.edge %d fail" %(i)
                raise

    @classmethod
    def _del_edges(cls, stream, graph):
        pass

    @classmethod
    def _valid_graph(cls, stream, graph):
        pass

    @classmethod
    def _start_to_run(cls, stream, graph):
        graph.set_start_to_run(0)
        graph.run()
        for i in graph.record:
            print json.dumps(dict(i['retval']), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)

    @classmethod
    def _is_ready_to_run(cls):
        pass

    @classmethod
    def _is_ready_to_join(cls):
        pass

    @classmethod
    def run(cls, path='./routers/table/TestTraderProfile.yaml'):
        #while True:
        cls.create_graphs(path)
            

# register at wsgi.py
m = Manager()
m.start()
#m.join()
