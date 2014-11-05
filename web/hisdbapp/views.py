
from .models import

def hisdb_stock_query(request, hisdb, stockid, starttime=, endtime=):
    try:
        data = run_hisdb_query.async(
            hisdb=hisdb,
            starttime=starttime,
            endtime=endtime,
            stockids=[stockid],
            traderids=[],
            debug=False).get()
    except Exception:
        return HttpResponseRedirect('/')
    return render(request, '')

def hisdb_trader_query(request, traderid):
