# scrapy tasks map
scrapy_tasks = {
    'twseid': {
        'kwargs': {
            'spider': 'twseid',
            'loglevel': 'INFO',
            'logfile': "./log/%s_%s.log" % (datetime.today().strftime("%Y%m%d_%H%M"), 'twseid'),
            'logen': True,
            'debug': False
        }
    },
    'otcid': {
        'kwargs': {
            'spider': 'otcid',
            'loglevel': 'INFO',
            'logfile': "./log/%s_%s.log" % (datetime.today().strftime("%Y%m%d_%H%M"), 'otcid'),
            'logen': True,
            'debug': False
        }
   },
    'twsehistrader': {
        'kwargs': {
            'spider': 'twsehistrader',
            'loglevel': 'INFO',
            'logfile': "./log/%s_%s.log" % (datetime.today().strftime("%Y%m%d_%H%M"), 'twsehistrader'),
            'logen': True,
            'debug': False
        }
    },
    'twsehisstock': {
         'kwargs': {
            'spider': 'twsehisstock',
            'loglevel': 'INFO',
            'logfile': "./log/%s_%s.log" % (datetime.today().strftime("%Y%m%d_%H%M"), 'twsehisstock'),
            'logen': True,
            'debug': False
        }
    },
    'otchistrader': {
        'kwargs': {
            'spider': 'otchistrader',
            'loglevel': 'INFO',
            'logfile': "./log/%s_%s.log" % (datetime.today().strftime("%Y%m%d_%H%M"), 'otchistrader'),
            'logen': True,
            'debug': False
        }
    },
    'otchisstock': {
        'kwargs': {
            'spider': 'otchisstock',
            'loglevel': 'INFO',
            'logfile': "./log/%s_%s.log" %(datetime.today().strftime("%Y%m%d_%H%M"), 'otchisstock'),
            'logen': True,
            'debug': False
        }
    }
}

# algorithm tasks map as, callfunc , args ...
# import module lib
algorithm_tasks = {
    'DualEMATaLib': {
    },
    'SuperManAlgorithm': {
        'kwargs': {
            'starttime': datetime.utcnow() - timedelta(days=60),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'traderids': []
    }
    ZombieAlgorithm,
]

# hisdb query tasks map
query_db_tasks = [
    'TwseHisDBQuery': {
        'kwargs': {
            'starttime': datetime.utcnow() - timedelta(days=60),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'traderids': []
        }
    },
    'OtcHisDBQuery': {
        'kwargs': {
            'starttime': datetime.utcnow() - timedelta(days=60),
            'endtime': datetime.utcnow(),

        }
    }

}

query_alg_tasks =


