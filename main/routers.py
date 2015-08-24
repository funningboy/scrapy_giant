# -*- coding: utf-8 -*-

from main.rules import *

def is_hisstock_detail(collect):
    collect.update({'method': 'detail'})
    return True

def is_hisstock_list(collect):
    return True

def is_histrader_detail(collect):
    return True

def is_histrader_list(collect):
    return True

