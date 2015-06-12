from main.table import default_tags

def hisstock_list_tags(**kwargs):
    return default_tags(**kwargs)

def hisstock_detail_tags(**kwargs):
    tags = default_tags(**kwargs)
    tags.update({
        'starttime': kwargs.pop('starttime', None),
        'endtime': kwargs.pop('endtime', None),
        'stockids': kwargs.pop('stockids', []),
        'traderids': kwargs.pop('traderids', []),
        'opt': kwargs.pop('opt', None),
        'algorithm': kwargs.pop('algorithm', None),
        'debug': kwargs.pop('debug', False)
    })
    return tags

def histrader_list_tags(**kwargs):
    tags = default_tags(**kwargs)
    tags.update({
        'starttime': kwargs.pop('starttime', None),
        'endtime': kwargs.pop('endtime', None),
        'opt': kwargs.pop('opt', None),
        'algorithm': kwargs.pop('algorithm', None),
        'debug': kwargs.pop('debug', False)
    })
    return tags

def histrader_detail_tags(**kwargs):
    return default_tags(**kwargs)