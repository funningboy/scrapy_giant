# -*- coding: utf-8 -*-

from main.models import ALG_CHOICES

def StockProfile0_buy(**collect):
    # StockProfile0+
    if collect['algorithm'] == ALG_CHOICES[0][1]:
        collect['frame']['hisstock'].update({
            'order': ['+totaldiff', '-totalbuyvolume', '+totalsellvolume'],
            'priority': 0
        })
        collect['frame']['hiscredit'].update({
            'order': ['+financeused', '+bearishused'],
            'priority': 1
        })
        collect['frame']['histrader'].update({
            'order': ['-totalvolume'],
            'priority': 2
        })

def StockProfile0_sell(**collect):
    # StockProfile0-
    if collect['algorithm'] == ALG_CHOICES[1][1]:
        collect['frame']['hisstock'].update({
            'order': ['-totaldiff', '-totalsellvolume', '+totalbuyvolume'],
            'priority': 0
        })
        collect['frame']['hiscredit'].update({
            'order': ['-bearishused', '-financeused'],
            'priority': 1
        })
        collect['frame']['histrader'].update({
            'order': ['-totalvolume'],
            'priority': 2
        })

def StockProfile1_buy(**collect):
    # StockProfile1+
    if collect['algorithm'] == ALG_CHOICES[2][1]:
        collect['frame']['hisstock'].update({
            'order': ['-totalbuyvolume', '+totalsellvolume', '+totaldiff'],
            'priority': 0
        })
        collect['frame']['hiscredit'].update({
            'order': ['+bearishused', '+financeused'],
            'priority': 1
        })
        collect['frame']['histrader'].update({
            'order': ['-totalvolume'],
            'priority': 2
        })

def StockProfile1_sell(**collect):
    # StockProfile1-
    if collect['algorithm'] == ALG_CHOICES[3][1]:
        collect['frame']['hisstock'].update({
            'order': ['-totalsellvolume', '+totalbuyvolume', '-totaldiff'],
            'priority': 0
        })
        collect['frame']['hiscredit'].update({
            'order': ['-bearishused', '-financeused'],
            'priority': 1
        })
        collect['frame']['histrader'].update({
            'order': ['-totalvolume'],
            'priority': 2
        })

def TraderProfile0_buy(**collect):
    # TraderProfile0+
    if collect['algorithm'] == ALG_CHOICES[4][1]:
        collect['frame']['histrader'].update({
            'order': ['-totalbuyvolume', '+totalsellvolume'],
            'priority': 0
        })
        collect['frame']['hisstock'].update({
            'order': ['-totalvolume', '-totaldiff'],
            'priority': 1
        })
        collect['frame']['hiscredit'].update({
            'order': ['+financeused', '+bearishused'],
            'priority': 2
        })

def TraderProfile0_sell(**collect):
    # TraderProfile0-
    if collect['algorithm'] == ALG_CHOICES[5][1]:
        collect['frame']['histrader'].update({
            'order': ['-totalsellvolume', '+totalbuyvolume'],
            'priority': 0
        })
        collect['frame']['hisstock'].update({
            'order': ['-totalvolume', '-totaldiff'],
            'priority': 1
        })
        collect['frame']['hiscredit'].update({
            'order': ['-bearishused', '-financeused'],
            'priority': 2
        })

def DualemaProfile(**collect):
    pass

