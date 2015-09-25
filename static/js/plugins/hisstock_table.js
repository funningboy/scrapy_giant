
function plotTableData(result){
    var stockitem = result.stockitem;
    var credititem = result.credititem;
    var futureitem = result.futureitem;
    var data = [];

    try {
        $.each(stockitem[0].datalist, function(d_idx, d_it) {
            var date = new Date(d_it.date);
            data.push({
                "date": yyyymmdd(date),
                "open": parseFloat(d_it.open.toFixed(2)),
                "close": parseFloat(d_it.close.toFixed(2)),
                "high": parseFloat(d_it.high.toFixed(2)),
                "low": parseFloat(d_it.low.toFixed(2)),
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
        console.log("stockitem None");
    }

    try {
        var ndata = $.extend(true, [], data);
        $.each(credititem[0].datalist, function(d_idx, d_it) {
            var date = new Date(d_it.date);
            var rst = $.grep(ndata, function(e){ return e.date == yyyymmdd(date); });
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
        var fdata = $.extend(true, [], ndata);
        $.each(futureitem[0].datalist, function(d_idx, d_it) {
            var date = new Date(d_it.date);
            var rst = $.grep(fdata, function(e){ return e.date == yyyymmdd(date); });
            if (rst.length != 0) {
                rst[0].fopen = parseFloat(d_it.fopen.toFixed(2));
                rst[0].fclose = parseFloat(d_it.fclose.toFixed(2));
                rst[0].fvolume = parseInt(d_it.fvolume.toFixed());
            }
        });
    } catch(err) {
        console.log("futureitem None");
    }

    $('#stockdetail_table').dynatable({
        dataset: {
            records: fdata
        }
    });

    //console.log(data);
}
