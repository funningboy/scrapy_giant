
//csrf_token
function loadChartData() {
     // host:port ...
    var URL = "http://127.0.0.1:8000/handler/api/hisstock_detail/?";
    $.each(settings, function(k, v) {
        if (k == "stockids" || k == "traderids") {
            v = v.join();
        }
        URL = URL + k + "=" + v +"&"
    });
    // csrf_token
    $.ajax({
        url: encodeURI(URL),
        data: {},
        type: "GET",
        dataType: "json",
        cache: false,

        beforeSend: function() {
        },

        complete: function() {
           // auto refresh after time out
            setTimeout(loadChartData, 10*60*1000); 
        },

        success: function (result) {
            //
            generateTableData(result);
        },

        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
}

function generateTableData(result){
    var stockitem = result.stockitem;
    var credititem = result.credititem;
    var data = [];

    // try iter to fill all fields
    // populate stockitem 
    console.log(result);

    $.each(stockitem, function(s_idx, s_it) {
        var d_idx = s_it.datalist.length -1;
        var d_it = s_it.datalist[d_idx];
        var stockidnm = s_it.stockid + '-' + s_it.stocknm;
        var date = new Date(d_it.date);
        data.push({
            "date": yyyymmdd(date),
            "stockidnm": stockidnm,
            "open": parseFloat(d_it.open.toFixed(2)),
            "high": parseFloat(d_it.high.toFixed(2)),
            "low": parseFloat(d_it.low.toFixed(2)),
            "close": parseFloat(d_it.close.toFixed(2)),
            "volume": parseInt(d_it.volume.toFixed()),
            "financeused" : 0.00,
            "bearishused": 0.00,
        });
    });

    // populate credititem
    var ndata = $.extend(true, [], data);
    $.each(credititem, function(c_idx, c_it) {
        var d_idx = c_it.datalist.length -1;
        var d_it = c_it.datalist[d_idx];
        var date = new Date(d_it.date);
        var stockidnm = c_it.stockid + '-' + c_it.stocknm;
        var rst = $.grep(ndata, function(e){ return e.date == yyyymmdd(date) && e.stockidnm == stockidnm; });
        if (rst.length != 0) {
            rst[0].financeused = parseFloat(d_it.financeused.toFixed(2));
            rst[0].bearishused = parseFloat(d_it.bearishused.toFixed(2));
        }
    });

    $('#stockdetail_table').dynatable({
        dataset: {
            records: ndata
        }
    });

    // debug
    console.log(data);
}

