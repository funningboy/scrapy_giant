
from routers.loader import Loader
from datetime import datetime, timedelta
from main.models import *

def schedule_autocmp_tasks(**collect):
    opt = collect.pop('opt', 'twse')
    debug = collect.pop('debug', False)
    ends = autocmp['AllIdAutoCmp'][1][opt][0]
    tmps = autocmp['AllIdAutoCmp'][1]['otc'] if opt == 'twse' else autocmp['AllIdAutoCmp'][1]['twse']
    cuts = []
    map(lambda x: cuts.extend(x), tmps)

    loader = Loader()
    graph = loader.create_graph(autocmp['AllIdAutoCmp'][0], priority=1, debug=debug)

    for n in cuts:
        graph.remove_node(n)

    loader.finalize(graph)
    graph.start()
    graph.join()

    nodes = filter(lambda x: x['node'] == ends[0], graph.record)
    return nodes[0]['retval']


def schedule_router_tasks(**collect):
    opt = collect.pop('opt', 'twse')
    algorithm = collect.pop('algorithm', 'StockProfileUp0')
    starttime = collect.pop('starttime', datetime.utcnow() - timedelta(days=20))
    endtime = collect.pop('endtime', datetime.utcnow())
    stockids = collect.pop('stockids', [])
    traderids = collect.pop('traderids', [])
    debug = collect.pop('debug', False)

    starts = routers[algorithm][1][opt][0]
    middles = routers[algorithm][1][opt][1]
    ends = routers[algorithm][1][opt][2]
    tmps = routers[algorithm][1]['otc'] if opt == 'twse' else routers[algorithm][1]['twse']
    cuts = []
    map(lambda x: cuts.extend(x), tmps)

    loader = Loader()
    graph = loader.create_graph(routers[algorithm][0], priority=1, debug=debug)

    for n in starts:
        ptr = graph.node[n]['ptr']
        win = ptr.kwargs['endtime'] - ptr.kwargs['starttime']
        ptr.kwargs.update({
            'starttime': endtime - win,
            'endtime': endtime,
            'stockids': stockids if stockids else ptr.kwargs['stockids'],
            'traderids': traderids if traderids else ptr.kwargs['traderids'],
            'debug': debug
        })
    for n in middles:
        ptr = graph.node[n]['ptr']
        win = ptr.kwargs['endtime'] - ptr.kwargs['starttime']
        ptr.kwargs.update({
            'starttime': endtime - win,
            'endtime': endtime,
            'debug': debug
        })
    for n in ends:
        ptr = graph.node[n]['ptr']
        ptr.kwargs.update({
            'starttime': starttime,
            'endtime': endtime,
            'debug': debug
        })
    for n in cuts:
        graph.remove_node(n)

    loader.finalize(graph)
    graph.start()
    graph.join()

    nodes = filter(lambda x: x['node'] == ends[0], graph.record)
    return nodes[0]['retval']
