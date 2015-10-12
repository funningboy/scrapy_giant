
//csrf_token
var hisstocklist = function(){
    ptr = {};
    ptr.version = '0.1.6';
    ptr.status = null;

    ptr.start = function() {};
    ptr.close = function() {};

    ptr.loadChartData = function(settings) {
        // host:port ...
        var URL = "http://127.0.0.1:8000/handler/api/hisstock_list/?opt=twse&starttime=2015/10/01&endtime=2015/10/10&stockids=&traderids=&algorithm=StockProfileRaw";
        /*var URL = "http://127.0.0.1:8000/handler/api/hisstock_list/?";
        $.each(settings, function(k, v) {
            if (k == "stockids" || k == "traderids") {
                v = v.join();
            }
            URL = URL + k + "=" + v +"&"
        });
        */
        console.log(encodeURI(URL));
        // csrf_token
        $.ajax({
            url: encodeURI(URL),
            data: {},
            type: "GET",
            dataType: "json",
            cache: false,
            //csrfmiddlewaretoken: settings...
            
            beforeSend: function() {
            },

            complete: function() {
               // auto refresh after time out
                setTimeout(ptr.loadChartData, 10*60*1000); 
            },

            success: function (result) {
                try {
                    ptr.plotlTableData(result);
                } catch(err) {
                    console.log("plotTableData fail");
                }
            },

            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        });
    };

    ptr.plotlTableData = function(result){
        var stockitem = result.stockitem;
        var credititem = result.credititem;
        var futureitem = result.futureitem;
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
                    "open": parseFloat(d_it.open.toFixed(2)),
                    "high": parseFloat(d_it.high.toFixed(2)),
                    "low": parseFloat(d_it.low.toFixed(2)),
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
            console.log("stockitem None");
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

        // encode stockidnm raw profile url link
        function tbodyWriter(id, item) {
            var stockidnm = item.stockidnm;
            var row = '<tr>' 
            + '<th>' + item.date + '</th>'
            + '<th>' 
            + `<class="bpop" id="${item.stockidnm}">`
            + item.stockidnm
            + `<div class="bpopup" id="${item.stockidnm}_popup" style="display:none">Content of popup`
            + '<span class="button b-close"><span>X</span></span>'
            + 'If you can\'t get it up use<br/>'
            + '<span class="logo">bPopup</span>'
            + '<span class="button b-close"><span>X</span></span>'
            + '    <div class="panel-body">'
            + '       <ul id="credit_columnchart"></ul>'
            + '    </div>'
            +  '</div>'
            + '</th>'
            + '<th>' + item.open + '</th>'
            + '<th>' + item.high + '</th>'
            + '<th>' + item.low + '</th>'
            + '<th>' + item.close + '</th>'
            + '<th>' + item.volume + '</th>'
            + '<th>' + item.finarmn + '</th>'
            + '<th>' + item.bearrmn + '</th>'
            + '<th>' + item.bfratio + '</th>'
            + '<th>' + item.fopen + '</th>'
            + '<th>' + item.fclose + '</th>'
            + '<th>' + item.fvolume + '</th>'
            + '<th>' + item.expect + '</th>'
            + '<th>' + item.accuracy + '</th>'
            + '<th>' + item.event + '</th>'
            + '</tr>';
          return row;
        }

        $('#stocklist_table').dynatable({
            dataset: {
                records: data
            },
            writers: {
                _rowWriter: tbodyWriter
                }
        });
        
        $.each(data, function(s_idx, s_it) {
            var stockidnm = s_it.stockidnm;
            $(`#${stockidnm}`).click(function(e) {
                e.preventDefault();
                $(`#${stockidnm}_popup`).bPopup({
                    contentContainer:'.content',
                    //loadUrl: "handler/hisstock_detail.html"
                    //onOpen: function() { }, 
                    //onClose: function() { }
                });
            });
        });
    };

    return ptr;
};