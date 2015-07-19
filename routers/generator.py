# https://networkx.github.io/documentation/latest/reference/generators.html

import networkx as nx
import random
import itertools
from datetime import datetime, timedelta
from routers.loader import Loader
from workers.nodes import Node
from workers.gworker import GWorker
from handler.tasks import *
from algorithm.tasks import *

class Constraint(object):

    def __init__(self):
        pass

    def _parse_kwargs_all(self):
        methods = [
            (self._parse_kwargs, 'opt'),
            (self._parse_kwargs, 'Nodes'),
            (self._parse_kwargs, 'Edges'),
            (self._parse_kwargs, 'start_tasks'),
            (self._parse_kwargs, 'middle_tasks'),
            (self._parse_kwargs, 'end_tasks')
        ]
        return methods

    def _parse_kwargs(self, token, kwargs={}):
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

    def load(self, path):    
        with open(path, 'r') as stream:
            try:
                kwargs = yaml.load(stream)
            except:
                print "loading %s fail" %(path)
                raise
            for p, t in self._parse_kwargs_all()
                p(t, kwargs)
            return kwargs

    def shit_next_timeit(kwargs={}):
        pass

    def update_start_kwargs(self, kwargs={}):
        period = (kwargs['endtime'] - kwargs['starttime']).days
        kwargs.update({
            'starttime': - period
            'endtime': self._curtime
            'stockids':  [i for i in iddb_tasks[opt]().stock.get_ids()],
            'traderids': [i for i in iddb_tasks[opt]().trader.get_ids()],
            'callback': None
        })


    def update_end_kwargs(self, kwargs={}):
        period = (kwargs['endtime'] - kwargs['starttime']).days
        kwargs.update({
            'starttime': self._curtime - period
            'endtime': self._curtime
            'callback': 'insert_summary'
        })


    def update_middle_kwargs(self, kwargs={}):
        kwargs.update({
            'callback': None
        })



class Generator(object):

    def __init__(self, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._cst = Constraint()
        self._cstattr = self._cst.load(kwargs.pop('path', None))

    def _create_hisitem_tasks(self, kwargs={}):
        methods = [
            (Loader.parse_task, ['./routers/tasks/HisStock.yaml', kwargs]),
            (Loader.parse_task, ['./routers/tasks/HisCredit.yaml', kwargs]),
            (Loader.parse_task, ['./routers/tasks/HisFuture.yaml', kwargs]),
            (Loader.parse_task, ['./routers/tasks/HisTrader.yaml', kwargs])
        ]
        return methods

    def _create_algitem_tasks(self, kwargs={}):
        methods = [
            (Loader.parse_task, ['./routers/tasks/AlgDualema.yaml', kwargs]),
            (Loader.parse_task, ['./routers/tasks/AlgBBands.yaml', kwargs]),
            (Loader.parse_task, ['./routers/tasks/AlgBTrader.yaml', kwargs]),
        ]
        return methods

    def _bind_start_task(self, kwargs={}):
        if self._cstattr['start_tasks']:
            stream = self._cstattr['start_tasks'].pop(0)
        else:
            tasks = self._create_hisitem_tasks(kwargs)
            ptr, args = random.sample(tasks, 1)[0]
            stream = ptr(*args)
        task, kwargs = eval(stream['task']), self._cst.update_start_kwargs(stream['kwargs'])
        node = Node(func=task, kwargs=kwargs)
        return node

    def _bind_middle_task(self, kwargs={}):
        if self._cstattr['middle_tasks']:
            stream = self._cstattr['middle_tasks'].pop(0)
        else:
            tasks = self._create_hisitem_tasks(kwargs) + self._create_algitem_tasks(kwargs)
            ptr, args = random.sample(tasks, 1)[0]
            stream = ptr(*args)
        task, kwargs = eval(stream['task']), self._cst.update_middle_kwargs(stream['kwargs'])
        node = Node(func=task, kwargs=kwargs)
        return node

    def _bind_end_task(self, kwargs={}):
        if self._cstattr['']:

        else:
            tasks = self._create_algitem_tasks(kwargs)
            ptr, args = random.sample(tasks, 1)[0]
            stream = ptr(*args)
        task = eval(stream['task'])
        node = Node(func=task, kwargs=stream['kwargs'])
        return node

    def _create_graph_methods(self):
        methods = [
            self._generate_graph,
            self._reassign_graph,
            self._populate_graph,
            self._set_start_to_run
        ]
        return methods

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

    def _generate_basic_graph(self):
        runs = [
            nx.gnm_random_graph(self._nodes, self._edges, directed=True),
        ]

        while self._try_runs:
            self._try_runs -= 1
            graph = random.sample(runs, 1)[0]
            if self._is_valid_graph(graph):
                return graph
        print "can't generate DAG graph at timeout"
        raise

    def _reassign_graph(self, graph):
        # ???
        ngraph = GWorker(debug=self._debug, priority=1)
        for node in graph.nodes():
            ngraph.add_node(node, {'ptr': None})
        for edge in graph.edges():
            u, v = edge
            ngraph.add_edge(u, v, weight=1)
        return ngraph

    def _populate_basic_graph(self, graph):
        for node in nx.topological_sort(graph):
            kwargs =  #???

            if not graph.predecessors(node):    
                ptr = self._bind_start_task()
                node, ptr['kwargs']

            elif not graph.successors(node): 
                ptr = self._bind_end_task(self._update_end_kwargs(kwargs))

            else:
                ptr = self._bind_middle_node(
                    self._update_middle_kwargs(kwargs))
            graph.node[node]['ptr'] = ptr


    def _set_start_to_run(self):
        for node in nx.topological_sort(graph):
            if not nx.ancestors(graph, node):
                graph.set_start_to_run(node)

    def create_random_graph(self, constrain):
        pass
        return ngraph

