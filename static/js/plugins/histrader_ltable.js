function plotlTableData(result){
    var stockitem = result.stockitem;
    var credititem = result.credititem;
    var futureitem = result.futureitem;
    var traderitem = result.traderitem;
    var data = [];

    try {
        $.each(stockitem, function(s_idx, s_it) {
            var d_idx = s_it.datalist.length -1;
            var d_it = s_it.datalist[d_idx];
            var stockidnm = s_it.stockid + '-' + s_it.stocknm;
            var date = new Date(d_it.date);
            data.push({
                "date": yyyymmdd(date),
                "stockidnm": stockidnm,
                "traderidnm": "",
                "buyrat": 0.00,
                "sellrat": 0.00,
                "open": parseFloat(d_it.open.toFixed(2)),
                "close": parseFloat(d_it.close.toFixed(2)),
                "volume": parseInt(d_it.volume.toFixed()),
                "finarmn" : 0.00,
                "bearrmn": 0.00,
                "bfratio": 0.00,
                "fopen": 0.00,
                "fclose": 0.00,
                "fvolume": 0,
                "event": ""
            });
        });
    } catch(err) {
        console.log("stockidnm None");
    }

    try {
        data = $.extend(true, [], data);
        $.each(traderitem, function(t_idx, t_it) {
            var d_idx = t_it.datalist.length -1;
            var d_it = t_it.datalist[d_idx];
            var date = new Date(d_it.date);
            var stockidnm = t_it.stockid + '-' + t_it.stocknm;
            var traderidnm = t_it.traderid + '-' + t_it.tradernm;
            var rst = $.grep(data, function(e){ return e.date == yyyymmdd(date) && e.stockidnm == stockidnm; });
            if (rst.length != 0) {
                rst[0].traderidnm = traderidnm;
                rst[0].buyrat = parseFloat(d_it.buyratio.toFixed(2));
                rst[0].sellrat = parseFloat(d_it.sellratio.toFixed(2));
            }
        });
    } catch(err) {
        console.log("traderitem None");
    }

    try {
        data = $.extend(true, [], data);
        $.each(credititem, function(c_idx, c_it) {
            var d_idx = c_it.datalist.length -1;
            var d_it = c_it.datalist[d_idx];
            var date = new Date(d_it.date);
            var stockidnm = c_it.stockid + '-' + c_it.stocknm;
            var rst = $.grep(data, function(e){ return e.date == yyyymmdd(date) && e.stockidnm == stockidnm; });
            if (rst.length != 0) {
                rst[0].finarmn = parseFloat(d_it.financeremain.toFixed(2));
                rst[0].bearrmn = parseFloat(d_it.bearishremain.toFixed(2));
                rst[0].bfratio = parseFloat(d_it.bearfinaratio.toFixed(2));
            }
        });
    } catch(err) {
        console.log("credititem None");
    }

    try {
        data = $.extend(true, [], data);
        $.each(futureitem, function(f_idx, f_it) {
            var d_idx = f_it.datalist.length -1;
            var d_it = f_it.datalist[d_idx];
            var date = new Date(d_it.date);
            var stockidnm = f_it.stockid + '-' + f_it.stocknm;
            var rst = $.grep(data, function(e){ return e.date == yyyymmdd(date) && e.stockidnm == stockidnm; });
            if (rst.length != 0) {
                rst[0].fopen = parseFloat(d_it.fopen.toFixed(2));
                rst[0].fclose = parseFloat(d_it.fclose.toFixed(2));
                rst[0].fvolume = parseInt(d_it.fvolume.toFixed());
            }
        });
    } catch(err) {
        console.log("futureitem None");
    }
    
    $('#traderlist_table').dynatable({
        dataset: {
            records: data
        }
    });

    //console.log(data);
}
