# https://networkx.github.io/documentation/latest/reference/generators.html

import networkx as nx
import random
from routers.loader import Loader
from workers.nodes import Node
from workers.gworker import GWorker
from handler.tasks import *
from algorithm.tasks import *

from datetime import datetime, timedelta 

class Generator(object):

    def __init__(self, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._nodes = kwargs.pop('nodes', 6)
        self._edges = kwargs.pop('edges', 5)
        self._try_runs = kwargs.pop('try_runs', 10)
        self._visited = []

    #@classmethod
    #def 

    def _create_hisitem_tasks(self, kwargs={}):
        # register hisitem tasks
        methods = [
            (Loader.parse_task, ['./routers/tasks/HisStock.yaml', kwargs]),
            (Loader.parse_task, ['./routers/tasks/HisCredit.yaml', kwargs]),
            (Loader.parse_task, ['./routers/tasks/HisFuture.yaml', kwargs]),
            (Loader.parse_task, ['./routers/tasks/HisTrader.yaml', kwargs])
        ]
        return methods

    def _create_algitem_tasks(self, kwargs={}):
        # register algitem tasks
        methods = [
            (Loader.parse_task, ['./routers/tasks/AlgDualema.yaml', kwargs]),
            (Loader.parse_task, ['./routers/tasks/AlgBBands.yaml', kwargs]),
            (Loader.parse_task, ['./routers/tasks/AlgBTrader.yaml', kwargs]),
        ]
        return methods

    def _create_random_kwargs(self):
        kwargs = {
            'opt': 'twse',
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': [],
            'traderids': [],
            'debug': True
        }
        return kwargs

    def _update_start_kwargs(self, kwargs={}):
        opt, debug = kwargs['opt'], kwargs['debug']
        kwargs.update({
            'stockids':  [i for i in iddb_tasks[opt](debug=debug).stock.get_ids()],
            'traderids': [i for i in iddb_tasks[opt](debug=debug).trader.get_ids()],
            'callback': None
        })
        return kwargs

    def _update_end_kwargs(self, kwargs={}):
        kwargs.update({
            'callback': 'insert_summary'
        })
        return kwargs

    def _update_middle_kwargs(self, kwargs={}):
        kwargs.update({
            'callback': None
        })
        return kwargs

    def _bind_start_node(self, kwargs={}):
        tasks = self._create_hisitem_tasks(kwargs)
        ptr, args = random.sample(tasks, 1)[0]
        stream = ptr(*args)
        task = eval(stream['task'])
        node = Node(func=task, kwargs=stream['kwargs'])
        return node

    def _bind_middle_node(self, kwargs={}):
        tasks = self._create_hisitem_tasks(kwargs) + self._create_algitem_tasks(kwargs)
        ptr, args = random.sample(tasks, 1)[0]
        stream = ptr(*args)
        task = eval(stream['task'])
        node = Node(func=task, kwargs=stream['kwargs'])
        return node

    def _bind_end_node(self, kwargs={}):
        tasks = self._create_algitem_tasks(kwargs)
        ptr, args = random.sample(tasks, 1)[0]
        stream = ptr(*args)
        task = eval(stream['task'])
        node = Node(func=task, kwargs=stream['kwargs'])
        return node

    def _create_graph_methods(self):
        methods = [
            self._generate_random_graph,
            self._reassign_random_graph,
            self._populate_random_graph,
            self._set_start_to_run
        ]
        return methods

    def _generate_random_graph(self, *args):
        runs = [
            nx.gnm_random_graph(self._nodes, self._edges, directed=True),
        ]

        while self._try_runs:
            self._try_runs -= 1
            graph = random.sample(runs, 1)[0]
            if nx.is_directed_acyclic_graph(graph):
                return graph
        print "can't generate DAG graph at Nodes(%d), Edges(%d)" %(self._nodes, self._edges)
        raise

    def _reassign_random_graph(self, graph):
        # ???
        ngraph = GWorker(**kwargs)
        for node in graph.nodes():
            ngraph.add_node(node, {'ptr': None})
        for edge in graph.edges():
            u, v = edge
            ngraph.add_edge(u, v, weight=1)
        return ngraph

    def _populate_random_graph(self, graph):
        for node in nx.topological_sort(graph):
            kwargs = self._create_random_kwargs(constrain) #???
            if not graph.predecessors(node):    
                ptr = self._bind_start_node(
                    self._update_start_kwargs(kwargs))
            elif not graph.successors(node): 
                ptr = self._bind_end_node(
                    self._update_end_kwargs(kwargs))
            else:
                ptr = self._bind_middle_node(
                    self._update_middle_kwargs(kwargs))
            graph.node[node]['ptr'] = ptr


    #def 
    #    for node in nx.topological_sort(ngraph):
    #        if not nx.ancestors(ngraph, node):
    #            ngraph.set_start_to_run(node)

    def create_random_graph(self, constrain):
        pass




        return ngraph

