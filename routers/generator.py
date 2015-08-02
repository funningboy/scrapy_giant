# https://networkx.github.io/documentation/latest/reference/generators.html

import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
import time
from datetime import datetime, timedelta
from routers.loader import Loader
from workers.nodes import Node
from workers.gworker import GWorker
from handler.tasks import *
from algorithm.tasks import *

class Constraint(object):

    @classmethod
    def _parse_kwargs_all(cls):
        methods = [
            (cls._parse_kwargs, 'opt'),
            (cls._parse_kwargs, 'fromtime'),
            (cls._parse_kwargs, 'totime'),
            (cls._parse_kwargs, 'period'),
            (cls._parse_kwargs, 'Nodes'),
            (cls._parse_kwargs, 'Edges'),
            (cls._parse_kwargs, 'start_tasks'),
            (cls._parse_kwargs, 'middle_tasks'),
            (cls._parse_kwargs, 'end_tasks')
        ]
        return methods

    @classmethod
    def _parse_kwargs(cls, token, kwargs={}):
        try:
            if token in kwargs:
                try:
                    kwargs.update({token: eval(kwargs[token])})
                except:
                    kwargs.update({token: kwargs[token]})
                    pass
        except:
            print "parse %s fail" %(token)
            raise

    @classmethod
    def load(cls, path):    
        with open(path, 'r') as stream:
            try:
                kwargs = yaml.load(stream)
            except:
                print "loading %s fail" %(path)
                raise
            for p, t in cls._parse_kwargs_all():
                p(t, kwargs)
            return kwargs


class Generator(object):

    def __init__(self, cst, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._maxtry = kwargs.pop('maxtry', 100)
        self._maxrun = kwargs.pop('maxrun', 100)
        self._cst = cst
        self._graph = None
        self._run = []

    def _sample_hisitem_tasks(self, nkwargs={}):
        samples = [
            (Loader.parse_task, ['./routers/tasks/HisStock.yaml', nkwargs]),
            (Loader.parse_task, ['./routers/tasks/HisCredit.yaml', nkwargs]),
            (Loader.parse_task, ['./routers/tasks/HisFuture.yaml', nkwargs]),
            (Loader.parse_task, ['./routers/tasks/HisTrader.yaml', nkwargs])
        ]
        return samples

    def _sample_algitem_tasks(self, nkwargs={}):
        samples = [
            (Loader.parse_task, ['./routers/tasks/AlgDualema.yaml', nkwargs]),
            (Loader.parse_task, ['./routers/tasks/AlgBBands.yaml', nkwargs]),
            (Loader.parse_task, ['./routers/tasks/AlgBTrader.yaml', nkwargs]),
            #(Loader.parse_task, ['./routers/tasks/AlgRForest.yaml', nkwargs]),
            #(Loader.parse_task, ['./routers/tasks/AlgKmeans.yaml', nkwargs])
        ]
        return samples

    def _report_algitem_tasks(self, nkwargs={}):
        reports = {
            'dualema': (Loader.parse_task, ['./routers/tasks/RptDualema.yaml', nkwargs]),
            'bbands':  (Loader.parse_task, ['./routers/tasks/RptBBands.yaml', nkwargs]),
            'btrader': (Loader.parse_task, ['./routers/tasks/RptBTrader.yaml', nkwargs]),
            #'rforest': (Loader.parse_task, ['./routers/tasks/RptRForest.yaml', nkwargs]),
            #'kmeans':  (Loader.parse_task, ['./routers/tasks/RptKmeans.yaml', nkwargs])
        }
        return reports

    def _bind_start_task(self, graph, node, nkwargs={}, init=False, callback=None):
        if self._cst['start_tasks']:
            stream = self._cst['start_tasks'].pop(0)
        else:
            tasks = self._sample_hisitem_tasks(nkwargs)
            ptr, args = random.sample(tasks, 1)[0]
            stream = ptr(*args)

        task, kwargs = eval(stream['task']), stream['kwargs']
        graph.node[node]['ptr'] = Node(func=task, kwargs=kwargs)

        if init:
            self._update_init_task(graph, node)
        if callback:
            callback(graph, node)

    def _update_init_task(self, graph, node):
        ptr = graph.node[node]['ptr']
        days = (ptr.kwargs['endtime'] - ptr.kwargs['starttime']).days
        ptr.kwargs.update({
           'starttime': self._cst['fromtime'] - timedelta(days=days),
           'endtime': self._cst['fromtime']
        })

    def _update_start_task(self, graph, node):
        ptr = graph.node[node]['ptr']
        ptr.kwargs.update({
            'starttime': ptr.kwargs['starttime'] - timedelta(days=self._cst['period']),
            'endtime': ptr.kwargs['endtime'] - timedelta(days=self._cst['period']),
            'stockids': ptr.kwargs['stockids'] if ptr.kwargs['stockids'] else [i for i in iddb_task[self._cst['opt']].stock.get_ids()],
            'traderids': ptr.kwargs['traderids'] if ptr.kwargs['traderids'] else [i for i in iddb_task[self._cst['opt']].trader.get_ids()],
            'callback': None,
            'debug': self._debug
        })
        
    def _bind_middle_task(self, graph, node, init=False, nkwargs={}, callback=None):
        if self._cst['middle_tasks']:
            stream = self._cst['middle_tasks'].pop(0)
        else:
            tasks = self._sample_hisitem_tasks(nkwargs) + self._sample_algitem_tasks(nkwargs)
            ptr, args = random.sample(tasks, 1)[0]
            stream = ptr(*args)

        task, kwargs = eval(stream['task']), stream['kwargs']
        graph.node[node]['ptr'] = Node(func=task, kwargs=kwargs)

        if init:
            self._update_init_task(graph, node)
        if callback:
            callback(graph, node)

    def _update_middle_task(self, graph, node):
        ptr = graph.node[node]['ptr']
        ptr.kwargs.update({
            'starttime': ptr.kwargs['starttime'] - timedelta(days=self._cst['period']),
            'endtime': ptr.kwargs['endtime'] - timedelta(days=self._cst['period']),
            'stockids': ptr.kwargs['stockids'] if ptr.kwargs['stockids'] else [],
            'traderids': ptr.kwargs['traderids'] if ptr.kwargs['traderids'] else [],
            'callback': None,
            'debug': self._debug
        }) 

    def _bind_end_task(self, graph, node, init=False, nkwargs={}, callback=None):
        if self._cst['end_tasks']:
            stream = self._cst['end_tasks'].pop(0)
        else:
            tasks = self._sample_algitem_tasks(nkwargs)
            ptr, args = random.sample(tasks, 1)[0]
            stream = ptr(*args)

        task, kwargs = eval(stream['task']), stream['kwargs']
        graph.node[node]['ptr'] = Node(func=task, kwargs=kwargs)

        if init:
            self._update_init_task(graph, node)
        if callback:
            callback(graph, node)

    def _update_end_task(self, graph, node):
        ptr = graph.node[node]['ptr']
        ptr.kwargs.update({
            'starttime': ptr.kwargs['starttime'] - timedelta(days=self._cst['period']),
            'endtime': ptr.kwargs['endtime'] - timedelta(days=self._cst['period']),
            'stockids': ptr.kwargs['stockids'] if ptr.kwargs['stockids'] else [],
            'traderids': ptr.kwargs['traderids'] if ptr.kwargs['traderids'] else [],
            'callback': 'insert_summary',
            'debug': self._debug
        }) 

    def _bind_report_task(self, graph, node, init=False, nkwargs={}, callback=None):
        ptr = graph.node[node]['ptr']
        _report_algitem_tasks

    def _update_report_task(self):
        pass

    def run(self):
        graph = self._generate_graph()
        graph = self._populate_graph(graph, True)
        if self._debug:
            nx.draw(graph)
            plt.savefig("generator.png")

        while self._cst['fromtime'] <= self._cst['totime']:
            if len(self._run) < self._maxrun:
                self._cst['fromtime'] += timedelta(days=self._cst['period'])
                graph = self._populate_graph(graph, False)
                worker = self._transfer_graph_as_worker(graph)
                worker.start()
                self._run.append(worker)
            else:
                comp = [it for it in self._run if not it.isAlive()]
                for it in comp:
                    it.join()
                    del it
                    self._run.remove(it)
                time.sleep(1)

            if self._debug:
                print "run tasks %d" %(len(self._runs))

        self._graph = graph

    def report(self):
        pass

    def export(self):
        pass

    def _generate_graph(self):
        samples = [
            nx.gnm_random_graph(self._cstarrt['Nodes'], self._cst['Edges'], directed=True),
        ]

        while self._maxtry:
            self._maxtry -= 1
            graph = random.sample(samples, 1)[0]
            if self._is_valid_graph(graph):
                return graph
        print "can't generate DAG worker graph"
        raise

    def _is_valid_graph(self, graph):
        rules = [
            nx.is_directed_acyclic_graph(graph),
            len([node for node in graph.nodes() if not graph.predecessors(node)]) >= len(self._start_tasks),
            len([node for node in graph.nodes() if not graph.successors(node)]) >= len(self._end_tasks),
            len([node for node in graph.nodes() if len(graph.predecessors(node)) > 0 and len(grpah.successors(node)) > 0]) >= len(self._middle_tasks)
        ]
        for rule in rules:
            if not rule:
                return False
        return True

    def _populate_graph(self, graph, init=False):
        for node in nx.topological_sort(graph):
            if not graph.predecessors(node):    
                self._bind_start_task(graph, node, init, self._update_start_task)
            elif not graph.successors(node): 
                self._bind_end_task(graph, node, init, self._update_end_task)
            else:
                self._bind_middle_node(graph, node, init, self._update_middle_task)
        return graph

    def _transfer_graph_as_worker(self, graph):
        worker = GWorker(debug=self._debug, priority=1)
        for node in graph.nodes():
            worker.add_node(node, {'ptr': graph.node[node]['ptr']})
            if not nx.ancestors(graph, node):
                worker.set_start_to_run(node)
        for edge in graph.edges():
            u, v = edge
            worker.add_edge(u, v, weight=1)
        return worker