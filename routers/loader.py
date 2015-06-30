# -*- coding: utf-8 -*-

import yaml
import threading
import networkx as nx
from datetime import datetime, timedelta
from workers.gworker import GWorker
from workers.nodes import Node
from handler.tasks import collect_hisitem
from algorithm.tasks import collect_algitem

class Loader(threading.Thread):

    _waits = []
    _runs = []
    _max_tasks = 10
    _task_keys = ['kwargs', 'task', 'description']
    _graph_keys = ['Nodes', 'Edges']
    daemon = True
    _stop = threading.Event()

    def __init__(self, **kwargs):
        super(Loader, self).__init__()
        threading.Thread.__init__(self)

    def stop(self):
        self._stop.set()

    def stopped(cls):
        return self._stop.isSet()

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

    def _create_graph_methods(self):
        methods = [
            self._create_edges,
            self._create_nodes,
            self._valid_graph,
            self._set_start_to_run
        ]
        return methods

    def create_graph(self, path):
        with open(path, 'r') as stream:
            stream = yaml.load(stream)
            assert(set(stream.keys()) == set(self._graph_keys))
            graph = GWorker()
            for it in self._create_graph_methods():
                it(stream, graph)
            return graph

    def _delete_node(self, graph, node):
        if node in graph.nodes():
            graph.remove_node(node)

    def _add_node(self, graph, node, attr={'ptr': None}):
        if node not in graph.nodes():
            graph.add_node(node, attr)

    def _create_nodes(self, stream, graph):
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

    def _create_edges(self, stream, graph):
        assert(isinstance(stream['Edges'], list))
        for i, edge in enumerate(stream['Edges']):
            try:
                cur, nxt, weight = map(int, edge)
                graph.add_edge(cur, nxt, weight=weight)
            except:
                print "create graph.edge %d fail" %(i)
                raise

    def _add_edge(self, graph, u, v, weight=1):
        if (u,v) not in graph.edges():
            graph.add_edge(u, v, weight)

    def _delete_edge(self, graph, u, v):
        if (u,v) in graph.edges():
            graph.remove_edge(u, v)
    
    def _valid_graph(self, stream, graph):
        if not nx.is_directed_acyclic_graph(graph):
            print "cycles:"
            print list(nx.simple_cycles(graph))
            raise
  
    def _set_start_to_run(self, stream, graph):
        starts = nx.topological_sort(graph)
        for i in starts:
            if not nx.ancestors(graph, i):
                graph.set_start_to_run(i)
   
    def _create_task(self, graph, priority=1):
        task = {
            'priority': priority,
            'graph': graph,
        }
        return task
    
    def _start_to_run(self, task):
        task['graph'].start()
   
    def _join_to_run(self, task):
        task['graph'].join()
   
    def _add_runs(self, task):
        if task not in self._runs:
            self._runs.append(task)
    
    def _del_runs(self, task):
        if task in self._runs:
            self._runs.remove(task)
 
    def _add_waits(self, task):
        if task not in self._waits:
            self._waits.append(task)

    def _del_waits(self, task):
        if task in self._waits:
            self._waits.remove(task)

    def _find_ready_to_run(self):
        end = self._max_tasks - len(self._runs)
        for it in sorted(self._waits, key=lambda x: x['priority'])[:end]:
            yield it

    def _find_ready_to_join(self):
        for it in self._runs:
            if not it['graph'].isAlive():
                yield it

    def run(self):
        while True:

            for graph in self._find_ready_to_join():
                self._join_to_run(graph)
                self._del_runs(graph)

            for graph in self._find_ready_to_run():
                self._start_to_run(graph)
                self._add_runs(graph)
                self._del_waits(graph)

    def is_ready_to_stop(self):
        return sum([len(self._runs),  len(self._waits)]) == 0
