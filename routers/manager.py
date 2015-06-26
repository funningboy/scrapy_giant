# -*- coding: utf-8 -*-

import yaml
from datetime import datetime, timedelta
from workers.gworker import GiantWorker
from workers.nodes import Node
from handler.tasks import collect_hisitem
import threading
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
                cls._parse_debug
            ]        
            for it in parse_kwargs:
                it(stream['kwargs'], kwargs)        
            return stream

    @classmethod
    def _parse_opt(cls, okwargs, nkwargs={}):
        try:
            assert('opt' in okwargs)
            okwargs['opt'] = nkwargs['opt'] if 'opt' in nkwargs else okwargs['opt']
            assert(okwargs['opt'] in ['twse', 'otc'])
        except:
            print "parse opt fail"
            raise

    @classmethod
    def _parse_target(cls, okwargs, nkwargs={}):
        pass

    @classmethod
    def _parse_starttime(cls, okwargs, nkwargs={}):
        try:
            assert('starttime' in okwargs)
            starttime = eval(nkwargs['starttime']) if 'starttime' in nkwargs else eval(okwargs['starttime'])
            okwargs['starttime'] = starttime if isinstance(starttime, datetime) else datetime.utcnow() - timedelta(days=30)
        except:
            print "parse starttime fail"
            raise

    @classmethod
    def _parse_endtime(cls, okwargs, nkwargs={}):
        try:
            assert('endtime' in okwargs)
            endtime = eval(nkwargs['endtime']) if 'endtime' in nkwargs else eval(okwargs['endtime'])
            okwargs['endtime'] = endtime if isinstance(endtime, datetime) else datetime.utcnow()
        except:
            print "parse endtime fail"
            raise

    @classmethod
    def _parse_stockids(cls, okwargs, nkwargs={}):
        try:
            assert('stockids' in okwargs)
            stockids = nkwargs['stockids'] if 'stockids' in nkwargs else okwargs['stockids']
            okwargs['stockids'] = stockids  if isinstance(stockids, list) else []
        except:
            print "parse stockids fail"
            raise

    @classmethod
    def _parse_traderids(cls, okwargs, nkwargs={}):
        pass

    @classmethod
    def _parse_base(cls, okwargs, nkwargs={}):
        pass

    @classmethod
    def _parse_order(cls, okwargs, nkwargs={}):
        pass

    @classmethod
    def _parse_callback(cls, okwargs, nkwargs={}):
        pass

    @classmethod
    def _parse_limit(cls, okwargs, nkwargs={}):
        pass

    @classmethod
    def _parse_debug(cls, okwargs, nkwargs={}):
        try:
            okwargs['debug'] = True
        except:
            print "parse debug fail"
            raise

    @classmethod
    def create_graphs(cls, path, priority=0):
        with open(path, 'r') as stream:
            stream = yaml.load(stream)
            assert(set(stream.keys()) == set(['Nodes', 'Edges']))
            G = GiantWorker()
            create_methods = [
                cls._create_edges,
                cls._create_nodes,
                #cls._valid_graph,
                cls._start_to_run
            ]
            for it in create_methods:
                it(stream, G)

            task = {
                'priority': priority,
                'graph': G,
            }
            #cls._wait_queue.append(task)

    @classmethod
    def update_graphs(cls, stream, graph):
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
    def _start_to_run(cls, stream, graph):
        graph.set_start_to_run(0)
        graph.run()
        print graph.record

    @classmethod
    def _is_ready_to_run(cls):
        pass

    @classmethod
    def _is_ready_to_join(cls):
        pass

    @classmethod
    def run(cls, path='./routers/table/StockProfileUp0.yaml'):
        while True:
            cls.create_graphs(path)
            

# register at wsgi.py
m = Manager()
m.start()
#m.run()
m.join()
