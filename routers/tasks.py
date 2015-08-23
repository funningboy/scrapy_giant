
from routers.loader import Loader
import tempfile
import os

def collect_histrader_list(**collect):
    pass

def collect_hisstock_list(**collect):
    # mode StockProfileUp0 as default
    f = tempfile.NamedTemporaryFile(delete=False)
    stmt = '''
    Edges:
        [
            [0,1,1],
            [1,2,1],
            [2,3,1]
        ]
    Nodes: 
        [
        # 0
        'Loader.parse_task(
            "./routers/tasks/HisCredit.yaml",
            kwargs = {{
                "opt": {opt},
                "targets": ["credit"],
                "starttime": {credit_starttime},
                "endtime": {credit_endtime},
                "stockids": {credit_stockids} ,
                "base": "stock",
                "order": {credit_order},
                "limit": {credit_limit},
                "debug" {all_debug}
            }}
        )',

        # 1
        'Loader.parse_task(
            "./routers/tasks/HisFuture.yaml",
            kwargs = {{
                "opt": {opt},
                "targets":  ["future"],
                "starttime": {future_starttime},
                "endtime": {future_endtime},
                "stockids": {future_stockids},
                "base": "stock",
                "order": {future_order},
                "limit": {future_limit},
                "debug": {all_debug}
            }}
        )',

        # 2
        'Loader.parse_task(
            "./routers/tasks/HisStock.yaml", 
            kwargs = {{
                "opt": {,
                "targets": ["stock"],
                "starttime": {stock_starttime},
                "endtime": {stock_endtime},
                "stockids": {stock_stockids},
                "base": "stock",
                "order": {stock_order},
                "limit": {stock_limit},
                "debug": {all_debug}
            }}
        )',

        # 3
        'Loader.parse_task(
            "./routers/tasks/HisTrader.yaml",
            kwargs = {{
                "opt": {opt},
                "targets": ["trader"],
                "starttime": {trader_starttime},
                "endtime": {trader_endtime},
                "stockids": {trader_stockids},
                "traderids": {trader_traderids},
                "base": "stock",
                "order": {trader_order},
                "limit": {trader_limit},
                "debug": {all_debug}
            }}
        )',

        # 4
        'Loader.parse_task(
            "./routers/tasks/HisItemAll.yaml",
            kwargs = {{
                "opt": {opt},
                "targets": ["stock", "trader", "credit", "future"],
                "starttime": {all_starttime},
                "endtime": {all_endtime},
                "stockids": [],
                "traderids": [],
                "base": "stock",
                "order": [],
                "limit": {all_limit},
                "debug": {all_debug}
            }})'
        ]'''.format(
            all_opt=collect.pop('all_opt', '"twse"'),
            stock_starttime=collect.pop('stock_starttime', '""'),
            stock_endtime=collect.pop('stock_endtime', '""'),
            credit_starttime=collect.pop('credit_starttime', '""'),
            credit_endtime=collect.pop('credit_endtime', ''),
            future_starttime=collect.pop('future_starttime', ''),
            future_endtime=collect.pop('future_endtime', ''),
            trader_starttime=collect.pop('trader_starttime', ''),
            trader_endtime=collect.pop('trader_endtime', ''),
            all_starttime=collect.pop('all_starttime', ''),
            all_endtime=collect.pop('all_endtime', ''),
            stock_stockids=collect.pop('stock_stockids', '[]'),
            credit_stockids=collect.pop('credit_stockids', '[]'),
            future_stockids=collect.pop('future_stockids', '[]'),
            trader_stockids=collect.pop('trader_stockids', '[]'),
            trader_traderids=collect.pop('trader_traderids', '[]'),
            stock_order=collect.pop('stock_order', '["-totalvolume", "-totaldiff"]'),
            credit_order=collect.pop('credit_order', '["+bearishused", "+financeused"]'),
            future_order=collect.pop('future_order', '["-totalvolume", "-totaldiff"]'),
            trader_order=collect.pop('trader_order', '["-totalvolume", "-totalbuyvolume", "-totalsellvolume"]'),
            stock_limit=collect.pop('stock_limit', 30),
            credit_limit=collect.pop('credit_limit', 30),
            future_limit=collect.pop('future_limit', 30),
            trader_limit=collect.pop('trader_limit', 30),
            all_limit=collect.pop('all_limit', 30),
            all_debug=collect.pop('all_debug', False)
        )
    f.write(stmt) 
    f.close()
    loader = Loader()
    G = loader.create_graph(f.name, priority=1, debug=False)
    G.start()
    G.join()
    os.remove(f.name)
    return G.record[4]['retval']


def collect_hisstock_detail(**collect):
    f = tempfile.NamedTemporaryFile(delete=False)
    stmt = '''
    Edges: 
        [
            [0,1,1]
        ]
    Nodes:
        [
        # 0 
        'Loader.parse_task(
            "./routers/tasks/HisTrader.yaml",
            kwargs = {{
                "opt": {all_opt},
                "targets": ["trader"],
                "starttime": {all_starttime},
                "endtime": {all_endtime},
                "stockids": {all_stockids},
                "traderids": {all_traderids},
                "base": "stock",
                "order": {trader_order},
                "limit": {all_limit},
                "debug": {all_debug}
            }})',

        # 1
        'Loader.parse_task(
            "./routers/tasks/HisItemAll.yaml",
            kwargs = {{
                "opt": {all_opt},
                "targets": ["stock", "trader", "credit", "future"],
                "starttime": {all_starttime},
                "endtime": {all_endtime},
                "stockids": [],
                "traderids": [],
                "base": "stock",
                "order": [],
                "limit": {all_limit},
                "debug": {all_debug}
            }})'
        ]
    '''.format(
        all_opt=collect.pop('all_opt', '"twse"'),
        all_starttime=collect.pop('all_starttime', '"datetime.utcnow() - timedelta(days=30)"'),
        all_endtime=collect.pop('all_endtime', '"datetime.utcnow()"'),
        all_stockids=collect.pop('all_stockids', '[]'),
        all_traderids=collect.pop('all_traderids', '[]'),
        trader_order=collect.pop('trader_order', '["-totalvolume", "-totalbuyvolume", "-totalsellvolume"]'),
        all_limit=collect.pop('all_limit', 20),
        all_debug=collect.pop('all_debug', False)
    )
    f.write(stmt) 
    f.close()
    loader = Loader()
    G = loader.create_graph(f.name, priority=1, debug=False)
    G.start()
    G.join()
    os.remove(f.name)
    return G.record[1]['retval']


def collect_histrader_detail(**collect):
    f = tempfile.NamedTemporaryFile(delete=False)
    stmt = '''
    Edges: 
        [
            [0,1,1]
        ]
    Nodes:
        [
        # 0 
        'Loader.parse_task(
            "./routers/tasks/HisTrader.yaml",
            kwargs = {{
                "opt": {all_opt},
                "targets": ["trader"],
                "starttime": {all_starttime},
                "endtime": {all_endtime},
                "stockids": {all_stockids},
                "traderids": {all_traderids},
                "base": "trader",
                "order": {trader_order},
                "limit": {all_limit},
                "debug": {all_debug}
            }})',

        # 1
        'Loader.parse_task(
            "./routers/tasks/HisItemAll.yaml",
            kwargs = {{
                "opt": {all_opt},
                "targets": ["stock", "trader", "credit", "future"],
                "starttime": {all_starttime},
                "endtime": {all_endtime},
                "stockids": [],
                "traderids": [],
                "base": "stock",
                "order": [],
                "limit": {all_limit},
                "debug": {all_debug}
            }})'
        ]
    '''.format(
        all_opt=collect.pop('all_opt', '"twse"'),
        all_starttime=collect.pop('all_starttime', '"datetime.utcnow() - timedelta(days=30)"'),
        all_endtime=collect.pop('all_endtime', '"datetime.utcnow()"'),
        all_stockids=collect.pop('all_stockids', '[]'),
        all_traderids=collect.pop('all_traderids', '[]'),
        trader_order=collect.pop('trader_order', '["-totalvolume", "-totalbuyvolume", "-totalsellvolume"]'),
        all_limit=collect.pop('all_limit', 20),
        all_debug=collect.pop('all_debug', False)
    )
    f.write(stmt) 
    f.close()
    loader = Loader()
    G = loader.create_graph(f.name, priority=1, debug=False)
    G.start()
    G.join()
    os.remove(f.name)
    return G.record[1]['retval']