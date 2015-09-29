
from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *
from zipline.finance.trading import SimulationParameters
from zipline.utils.factory import create_simulation_parameters

class TestAlgo(TradingAlgorithm):
    """
    This algorithm will send a specified number of orders, to allow unit tests
    to verify the orders sent/received, transactions created, and positions
    at the close of a simulation.
    """

    def __init__(self, *args, **kwargs):
        super(TestAlgo, self).__init__(*args, **kwargs)

    def initialize(self):                                                        
        #context.sid = 'AAPL'                                                        
        #context.amount = 100                                                        
        pass

    def handle_data(self, data):                                                    
        self.sid = 'AAPL'                                                         
        self.amount = 1000                                                    
        self.order(self.sid, self.amount)                                                                        


if __name__ == '__main__':
    from datetime import datetime
    import pytz
    from zipline.utils.factory import load_from_yahoo
    #from zipline.api import get_environment

    # Set the simulation start and end dates.
    start = datetime(2012, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2015, 9, 30, 0, 0, 0, 0, pytz.utc)

    # Load price data from yahoo.
    data = load_from_yahoo(stocks=['AAPL'], indexes={}, start=start,
                           end=end)

    sim_params = SimulationParameters(
        period_start=start,
        period_end=end,
        data_frequency='daily',
        emission_rate='daily'
    )
    # Create and run the algorithm.
    algo = TestAlgo(sim_params=sim_params) 
    results = algo.run(data)
    risks = algo.perf_tracker.handle_simulation_end()  
    print risks.keys
    #print get_environment
    #print results

