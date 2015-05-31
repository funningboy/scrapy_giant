# -*- coding: utf-8 -*-

def router_search(**cmd):
    """ register to router search table """
    pass
#    is_hisstock_detail, hisstock_detail_html(**cmds),
#    is_hisstock_list, hisstock_list_html

idhandler = {
    'twse': iddb_tasks['twse'](**kwargs),
    'otc': iddb_tasks['otc'](**kwargs)
}

def is_hisstock_detail(**cmd):
    if cmds['algorithm'] not in [
        '0+', 'StockProfile0-',
        'StockProfile1+', 'StockProfile1-']:
        return False
    if cmds['starttime'] >= cmds['endtime'] or len(cmds['stockids']) != 1:
        return False
    return True

def is_hisstock_list(**cmd):
    if cmds[algorithm] not in [
        'StockProfile0+', 'StockProfile0-',
        'StockProfile1+', 'StockProfile1-']:
        return False
    if cmds['starttime'] >= cmds['endtime']:
        return False
    return True



