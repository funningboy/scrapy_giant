# -*- coding: utf-8 -*-

from __future__ import absolute_import

    'run_algorithm_service_twsedualema': {
        'task': 'bin.tasks.run_algorithm_service',
        'schedule': crontab(minute='*/1'),
        'args': (
            'twse',
            'dualema',
            datetime.utcnow() - timedelta(days=60),
            datetime.utcnow(),
            TwseIdDBQuery().get_stockids(debug),
            [],
            debug
        )
    },
    'run_algorithm_service_otcdualema': {
        'task': 'bin.tasks.run_algorithm_service',
        'schedule': crontab(minute='*/1'),
        'args': (
            'otc',
            'dualema',
            datetime.utcnow() - timedelta(days=60),
            datetime.utcnow(),
            OtcIdDBQuery().get_stockids(debug),
            [],
            debug
        )
    },
