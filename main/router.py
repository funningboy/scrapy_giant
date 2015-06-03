# -*- coding: utf-8 -*-

from main.models import ALG_CHOICES

def _StockProfile0_buy(**collect):
    # StockProfile0+
    if collect['algorithm'] == ALG_CHOICES[0][1]:
        collect['frame']['hisstock']update({
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

def _StockProfile0_sell(**collect):
    # StockProfile0-
    if collect['algorithm'] == ALG_CHOICES[1][1]:
        collect['frame']['hisstock'].update({
            'order': ['-totaldiff', '-totalsellvolume', '+totalbuyvolume'],
            'priority': 0
        })
                'hiscredit': {
                    'order': ['-bearishused', '-financeused'],
                    'priority': 1
                },
                'histrader': {
                    'order': ['-totalvolume'],
                    'priority': 2
                }
            }
        })

def _StockProfile1_buy(**collect):
    # StockProfile1+
    if collect['algorithm'] == ALG_CHOICES[2][1]:
        collect.update({
            'frame': {
                'hisstock': {
                    'order': ['-totalbuyvolume', '+totalsellvolume', '+totaldiff'],
                    'priority': 0
                },
                'hiscredit': {
                    'order': ['+bearishused', '+financeused'],
                    'priority': 1
                },
                'histrader': {
                    'order': ['-totalvolume'],
                    'priority': 2
                }
            }
        })

def _StockProfile1_sell(**collect):
    # StockProfile1-
    if collect['algorithm'] == ALG_CHOICES[3][1]:
        collect.update({
            'frame': {
                'hisstock': {
                    'order': ['-totalsellvolume', '+totalbuyvolume', '-totaldiff'],
                    'priority': 0
                },
                'hiscredit': {
                    'order': ['-bearishused', '-financeused'],
                    'priority': 1
                },
                'histrader': {
                    'order': ['-totalvolume'],
                    'priority': 2
                }
            }
        })

def _TraderProfile0_buy(**collect):
    # TraderProfile0+
    if collect['algorithm'] == ALG_CHOICES[4][1]:
        collect.update({
            'frame': {
                'histrader': {
                    'order': ['-totalbuyvolume', '+totalsellvolume'],
                    'priority': 0
                },
                'hisstock': {
                    'order': ['-totalvolume', '-totaldiff'],
                    'priority': 1
                },
                'hiscredit': {
                    'order': ['+financeused', '+bearishused'],
                    'priority': 2
                }
            }
        })

def _TraderProfile0_sell(**collect):
    # TraderProfile0-
    if collect['algorithm'] == ALG_CHOICES[5][1]:
        collect.update({
            'frame': {
                'histrader': {
                    'order': ['-totalsellvolume', '+totalbuyvolume'],
                    'priority': 0
                },
                'hisstock': {
                    'order': ['-totalvolume', '-totaldiff'],
                    'priority': 1
                },
                'hiscredit': {
                    'order': ['-bearishused', '-financeused'],
                    'priority': 2
                }
            }
        })

def _DualemaProfile(**collect):
    pass

