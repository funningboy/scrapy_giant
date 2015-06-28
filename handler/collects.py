# -*- coding: utf-8 -*-

def create_hiscollect(**kwargs):
    """ as context event """
    starttime = kwargs.pop('starttime', None)
    endtime = kwargs.pop('endtime', None)
    stockids =  kwargs.pop('stockids', [])
    traderids = kwargs.pop('traderids', [])
    opt = kwargs.pop('opt', None)
    algorithm = kwargs.pop('algorithm', None)
    debug = kwargs.pop('debug', False)
    method = kwargs.pop('method', None)

def create_relcollect(**kwargs):
    collect = {}
    return collect