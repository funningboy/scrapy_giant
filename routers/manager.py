# -*- coding: utf-8 -*-

import yaml
import threading
import json
import networkx as nx
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

    _task_keys = ['kwargs', 'task', 'description']
    _graph_keys = ['Nodes', 'Edges']

    def __init__(self):
        threading.Thread.__init__(self)

    @classmethod
    def _parse_kwargs_all(cls):
        methods = [
            (cls._parse_kwargs, 'opt'),
            (cls._parse_kwargs, 'targets'),
            (cls._parse_kwargs, 'starttime'),
            (cls._parse_kwargs, 'endtime'),
            (cls._parse_kwargs, 'stockids'),
            (cls._parse_kwargs, 'traderids'),
            (cls._parse_kwargs, 'base'),
            (cls._parse_kwargs, 'order'),
            (cls._parse_kwargs, 'callback'),
            (cls._parse_kwargs, 'limit'),
            (cls._parse_kwargs, 'cfg'),
            (cls._parse_kwargs, 'debug'),
        ] 
        return methods

    @classmethod
    def parse_task(cls, path, kwargs={}):
        with open(path) as stream:
            try:
                stream = yaml.load(stream)
                assert(set(stream.keys()) == set(cls._task_keys))
            except:
                print "loading %s fail" %(path)
                raise
        
            for p, t in cls._parse_kwargs_all():
                p(t, stream['kwargs'], kwargs)        
            return stream

    @classmethod
    def _parse_kwargs(cls, token, okwargs, nkwargs={}):
        try:
            if token in okwargs:
                if token in nkwargs:
                    try:
                        okwargs.update({token: eval(nkwargs[token])})
                    except:
                        okwargs.update({token: nkwargs[token]})
                        pass
                else:
                    try:
                        okwargs.update({token: eval(okwargs[token])})
                    except:
                        okwargs.update({token: okwargs[token]})
                        pass
        except:
            print "parse %s fail" %(token)
            raise

    @classmethod
    def _create_methods(cls):
        methods = [
            cls._create_edges,
            cls._create_nodes,
            cls._valid_graph,
            cls._start_to_run
        ]
        return methods

    @classmethod
    def create_graphs(cls, path, priority=1):
        with open(path, 'r') as stream:
            stream = yaml.load(stream)
            assert(set(stream.keys()) == set(cls._graph_keys))

            G = GiantWorker()
            for it in cls._create_methods():
                it(stream, G)

            task = cls._create_task()
            cls._add_wait_queue(task)

    @classmethod
    def _delete_nodes(cls, graph, n):
        graph.remove_node(n)

    @classmethod
    def _create_nodes(cls, stream, graph):
        assert(isinstance(stream['Nodes'], list))
        for i, node in enumerate(stream['Nodes']):
            try:
                node = eval(node)
                task = eval(node['task'])
                n = Node(func=task, kwargs=node['kwargs'])
                graph.add_node(i, {'ptr': n})
                graph.node[i]['ptr'].run()
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
    def _delete_edges(cls, graph, u, v):
        graph.remove_edges(u, v)

    @classmethod
    def _valid_graph(cls, stream, graph):
        if not nx.is_directed_acyclic_graph(graph):
            print "find cycle/loop at router table"
            raise

    @classmethod
    def _start_to_run(cls, stream, graph):
        starts = nx.topological_sort(graph)
        for i in starts:
            if not nx.ancestors(graph, i):
                graph.set_start_to_run(i)

    @classmethod
    def _create_task(cls, graph, priority=1):
        task = {
            'priority': priority,
            'graph': graph,
        }
        return task

    @classmethod
    def _run_task(cls, task):
        task['graph'].run()

    @classmethod
    def _add_wait_queue(cls, task):
        if task not in cls._wait_queue:
            cls._wait_queue.append(task)

    @classmethod
    def _del_wait_queue(cls, task):
        if task in cls._wait_queue:
            cls._wait_queue.remove(task)

    @classmethod
    def _add_run_queue(cls, task):
        if task not in cls._run_queue:
            cls._run_queue.append(task)

  @classmethod
    def _del_run_queue(cls, task):
        if task in cls._run_queue:
            cls._run_queue.remove(task)

    @classmethod
    def _find_ready_to_run(cls):
        limit = cls._max_concurrent - len(cls._run_queue)
        for it in sorted(cls._wait_queue, key=lambda x: x['priority'])[:limit]:
            yield it

    @classmethod
    def _find_ready_to_join(cls):
        for it in cls._run_queue:
            yield it

    @classmethod
    def run(cls):
        while True:
            for it in cls._find_ready_to_run():
                cls._add_run_queue(it)
                cls._del_wait_queue(it)

            for it in cls._find_ready_to_join():
                cls._run_task(it)
                cls._del_run_queue(it)
            
            

# register at wsgi.py
m = Manager()
m.start()
m.join()
