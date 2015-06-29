# -*- coding: utf-8 -*-

from main.models import ALG_CHOICES

DETAIL_LIMIT = 10
LIST_LIMIT = 50

def StockProfileUp0(collect):
    pass

def StockProfileDown0(collect):
    if collect['algorithm'] == ALG_CHOICES[1][1]:
        pass


def StockProfileUp1(collect):
    if collect['algorithm'] == ALG_CHOICES[2][1]:
        pass

def StockProfileDown1(collect):
    if collect['algorithm'] == ALG_CHOICES[3][1]:
        pass

def TraderProfileUp0(collect):
    if collect['algorithm'] == ALG_CHOICES[4][1]:
        pass

def TraderProfileDown0(collect):
    if collect['algorithm'] == ALG_CHOICES[5][1]:
        pass
 
