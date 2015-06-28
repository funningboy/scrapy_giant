# -*- coding: utf-8 -*-

import yaml
import threading
import json
from bson import json_util
from datetime import datetime, timedelta
from workers.gworker import GiantWorker
from workers.nodes import Node
from handler.tasks import collect_hisitem
from algorithm.tasks import collect_algitem
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
                cls._parse_targets,
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

            [
            ]
            for it in parse_kwargs:
                it(stream['kwargs'], kwargs)        
            return stream

    @classmethod
    def _parse_opt(cls, okwargs, nkwargs={}):
        try:
            if 'opt' in okwargs:
                if 'opt' in nkwargs:
                    okwargs.update({'opt': nkwargs['opt']})
                else:
                    okwargs.update({'opt': okwargs['opt']})
        except:
            print "parse opt fail"
            raise

    @classmethod
    def _parse_targets(cls, okwargs, nkwargs={}):
        try:
            if 'targets' in okwargs:
                if 'targets' in nkwargs:
                    okwargs.update({'targets': nkwargs['targets']})
                else:
                    okwargs.update({'targets': okwargs['targets']})
        except:
            print "parse targets fail"
            raise

    @classmethod
    def _parse_starttime(cls, okwargs, nkwargs={}):
        try:
            if 'starttime' in okwargs:
                if 'starttime' in nkwargs:
                    okwargs.update({'starttime': eval(nkwargs['starttime'])})
                else:
                    okwargs.update({'starttime': eval(okwargs['starttime'])})
        except:
            print "parse starttime fail"
            pass

    @classmethod
    def _parse_endtime(cls, okwargs, nkwargs={}):
        try:
            if 'endtime' in okwargs:
                if 'endtime' in nkwargs:
                    okwargs.update({'endtime': eval(nkwargs['endtime'])})
                else:
                    okwargs.update({'endtime': eval(nkwargs['endtime'])})
        except:
            print "parse endtime fail"
            raise

    @classmethod
    def _parse_stockids(cls, okwargs, nkwargs={}):
        try:
            if 'stockids' in okwargs:
                if 'stockids' in nkwargs:
                    okwargs.update({'stockids': nkwargs['stockids']})
                else:
                    okwargs.update({'stockids': okwargs['stockids']})
        except:
            print "parse stockids fail"
            raise

    @classmethod
    def _parse_traderids(cls, okwargs, nkwargs={}):
        try:
            if 'traderids' in okwargs:
                if 'traderids' in nkwargs:
                    okwargs.update({'traderids': nkwargs['traderids']})
                else:
                    okwargs.update({'traderids': okwargs['traderids']})
        except:
            print "parse traderids fail"
            raise

    @classmethod
    def _parse_base(cls, okwargs, nkwargs={}):
        try:
            if 'base' in okwargs:
                if 'base' in nkwargs:
                    okwargs.update({'base': nkwargs['base']})
                else:
                    okwargs.update({'base': okwargs['base']})
        except:
            print "parse base fail"
            raise

    @classmethod
    def _parse_order(cls, okwargs, nkwargs={}):
        try:
            if 'order' in okwargs:
                if 'order' in nkwargs:
                    okwargs.update({'order': nkwargs['order']})
                else:
                    okwargs.update({'order': okwargs['order']})
        except:
            print "parse order fail"
            raise

    @classmethod
    def _parse_callback(cls, okwargs, nkwargs={}):
        pass

    @classmethod
    def _parse_limit(cls, okwargs, nkwargs={}):
        try:
            if 'limit' in okwargs:
                if 'limit' in nkwargs:
                    okwargs.update({'limit': nkwargs['limit']})
                else:
                    okwargs.update({'limit': okwargs['limit']})
        except:
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
        try:
            if 'cfg' in okwargs:
                if 'cfg' in nkwargs:
                    okwargs.update({'cfg': nkwargs['cfg']})
                else:
                    okwargs.update({'cfg': okwargs['cfg']})
        except:
            print "parse cfg fail"
            raise

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
    def run(cls, path='./routers/table/TestPortfolio.yaml'):
        #while True:
        paths = [
            './routers/table/TestStockProfile.yaml',
            './routers/table/TestTraderProfile.yaml',
            './routers/table/TestPortfolio.yaml'
        ]
        for path in paths:
            cls.create_graphs(path)
            

# register at wsgi.py
m = Manager()
m.start()
m.join()
