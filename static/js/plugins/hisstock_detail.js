

 var hisstockdetail = function() {
    var ptr = {};
    ptr.version = '0.1.6';
    ptr.status = null;

    ptr.start = function() {};
    ptr.close = function() {};
    
    ptr.loadChartData = function(settings) {
        // setting.host, port ...
        var URL = "http://127.0.0.1:8000/handler/api/hisstock_detail/?opt=twse&starttime=2015/10/01&endtime=2015/10/10&stockids=2330&traderids=&algorithm=StockProfileRaw";
        /*var URL = "http://127.0.0.1:8000/handler/api/hisstock_detail/?";
        $.each(settings, function(k, v) {
            if (k == "stockids" || k == "traderids") {
                v = v.join();
            }
            URL = URL + k + "=" + v +"&"
        });
        */
        console.log(encodeURI(URL));
        $.ajax({
            url: encodeURI(URL),
            data: {},
            type: "GET",
            dataType: "json",
            cache: false,

            beforeSend: function() {
            },

            complete: function() {
                $("#topbuy_piechart").show();
                $("#topsell_piechart").show();
                $("#topmap_columnchart").show();
                $("#credit_columnchart").show();
                $("#future_columnchar").show();
                // auto refresh after time out
                setTimeout(ptr.loadChartData, 10*60*1000); 
            },

            success: function (result) { 
                try {
                    ptr.plotTraderData(result);
                } catch(err) {
                    console.log("plotTraderData fail");
                }
                try {
                    ptr.plotCreditData(result);
                } catch(err) {
                    console.log("plotCreditData fail");
                }
                try {
                    ptr.plotFutureData(result);
                } catch(err) {
                    console.log("plotFutureData fail");
                }
                try {
                    ptr.plotTableData(result);
                } catch(err) {
                    console.log("plotTableData fail");
                }
            },

            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
                $("#topbuy_piechart").hide();
                $("#topsell_piechart").hide();
                $("#topmap_columnchart").hide();
                $("#credit_columnchart").hide();
                $("future_columnchart").hide();
            }
        });
    };   

    ptr.plotCreditData = function(result){
        var stockitem = result.stockitem;  
        var credititem = result.credititem;
        var data = [];

        $.each(stockitem[0].datalist, function(d_idx, d_it) {
            var date = new Date(d_it.date);
            data.push({
                "date": yyyymmdd(date),
                "stockopen": parseFloat(d_it.open.toFixed(2)),
                "stockclose": parseFloat(d_it.close.toFixed(2)),
                "stockhigh": parseFloat(d_it.high.toFixed(2)),
                "stocklow": parseFloat(d_it.low.toFixed(2)),
                "stockprice": parseFloat(d_it.close.toFixed(2)),
                "stockvolume": parseInt(d_it.volume.toFixed()),
                "finaremain": 0.00,
                "finabuyvolume": 0.00,
                "finasellvolume": 0.00,
                "bearremain": 0.00,
                "bearbuyvolume": 0.00,
                "bearsellvolume": 0.00
            });
        });

        var ndata = $.extend(true, [], data);
        $.each(credititem[0].datalist, function(d_idx, d_it) {
            var date = new Date(d_it.date);
            var rst = $.grep(ndata, function(e){ return e.date == yyyymmdd(date); });
            if (rst.length != 0) {
                rst[0].finaremain = parseFloat(d_it.financeremain.toFixed(2));
                rst[0].bearremain = parseFloat(d_it.bearishremain.toFixed(2));
                rst[0].finabuyvolume = parseInt(d_it.financebuyvolume.toFixed());
                rst[0].finasellvolume = parseInt(d_it.financesellvolume.toFixed());
                rst[0].bearbuyvolume = parseInt(d_it.bearishbuyvolume.toFixed());
                rst[0].bearsellvolume = parseInt(d_it.bearishsellvolume.toFixed());
            }
        });
        
        ptr.createCreditColumnChart(ndata);
        //console.log(cdata);
    };

    ptr.createCreditColumnChart = function(cdata) {
        var chart = AmCharts.makeChart("credit_columnchart", {
            "type": "serial",
            "theme": "dark",
            "colors": ["#5F9EA0", "#7FFFD4", "#20B2AA", "#E0FFFF", "#008080", "#000000"],
            "path": "http://www.amcharts.com/lib/3/",
            "pathToImages": "http://www.amcharts.com/lib/3/images/",    
            "dataProvider": cdata,  
            "legend": {
                "equalWidths": false,
                "useGraphSettings": true
            },
            "valueAxes": [{
                "id": "volumeAxis",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position": "left",
                "title": "credit",        
                "stackType": "regular"
            }, 
            {
                "id": "priceAxis",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "inside": true,
                "position": "right",
                "title": "price"
            }],
            "graphs": [{
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "finabuyvolume",
                "type": "column",
                "valueField": "finabuyvolume",
                "valueAxis": "volumeAxis"
            },
            {
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "bearsellvolume",
                "type": "column",
                "valueField": "bearsellvolume",
                "valueAxis": "volumeAxis"
            }, 
            {
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "bearbuyvolume",
                "type": "column",
                "newStack": true,
                "valueField": "bearbuyvolume",
                "valueAxis": "volumeAxis"
            },
            {
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "finasellvolume",
                "type": "column",
                "valueField": "finasellvolume",
                "valueAxis": "volumeAxis"
            }, 
            {
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "stockvolume",
                "type": "column",
                "newStack": true, 
                "valueField": "stockvolume",
                "valueAxis": "volumeAxis"
            },      
            {
                "balloonText": "p: [[value]]",
                "bullet": "round",
                "bulletBorderAlpha": 1,
                "useLineColorForBulletBorder": true,
                "bulletColor": "#FFFFFF",
                "bulletSizeField": "townSize",
                "dashLengthField": "dashLength",
                "descriptionField": "event",
                "labelPosition": "right",
                "labelText": "[[event]]",
                "legendValueText": "p: [[value]]",
                "title": "stockprice",
                "fillAlphas": 0,
                "valueField": "stockprice",
                "valueAxis": "priceAxis"
            }], 
            "chartCursor": {
                "categoryBalloonDateFormat": "WW",
                "cursorAlpha": 0.1,
                "cursorColor":"#000000",
                "fullWidth":true,
                "valueBalloonsEnabled": false,
                "zoomable": false
            },
            "dataDateFormat": "YYYY-MM-DD", 
            "categoryField": "date",
            "categoryAxis": {
                "dateFormats": [{
                    "period": "DD",
                    "format": "DD"
                }, {
                    "period": "WW",
                    "format": "MMM DD"
                }, {
                    "period": "MM",
                    "format": "MMM"
                }, {
                    "period": "YYYY",
                    "format": "YYYY"
                }],
                "parseDates": true,
                "autoGridCount": false,
                "axisColor": "#555555",
                "gridAlpha": 0.1,
                "gridColor": "#FFFFFF",
                "gridCount": 50,
                "equalSpacing": true
            },
            "connect": false,
            "export": {
                "enabled": true
            },
            "chartScrollbar": {},  
            "chartCursor": {
                "cursorPosition": "mouse"
            }
        });
    };


    ptr.plotFutureData = function(result){
        var stockitem = result.stockitem;  
        var futureitem = result.futureitem;
        var data = [];

        $.each(stockitem[0].datalist, function(d_idx, d_it) {
            var date = new Date(d_it.date);
            data.push({
                "date": yyyymmdd(date),
                "stockopen": parseFloat(d_it.open.toFixed(2)),
                "stockclose": parseFloat(d_it.close.toFixed(2)),
                "stockhigh": parseFloat(d_it.high.toFixed(2)),
                "stocklow": parseFloat(d_it.low.toFixed(2)),
                "stockprice": parseFloat(d_it.close.toFixed(2)),
                "stockvolume": parseInt(d_it.volume.toFixed()),
                "futureopen": 0.00,
                "futureclose": 0.00,
                "futurehigh": 0.00,
                "futurelow": 0.00,
                "futureprice": 0.00,
                "futurevolume": 0
            });
        });

        var ndata = $.extend(true, [], data);
        $.each(futureitem[0].datalist, function(d_idx, d_it) {
            var date = new Date(d_it.date);
            var rst = $.grep(ndata, function(e){ return e.date == yyyymmdd(date); });
            if (rst.length != 0) {
                rst[0].futureopen = parseFloat(d_it.fopen.toFixed(2));
                rst[0].futureclose = parseFloat(d_it.fclose.toFixed(2));
                rst[0].futurehigh = parseFloat(d_it.fhigh.toFixed(2));
                rst[0].futureclose = parseFloat(d_it.fclose.toFixed(2));
                rst[0].futureprice = parseFloat(d_it.fclose.toFixed(2));
                rst[0].futurevolume = parseInt(d_it.fvolume.toFixed());
            }
        });
        
        ptr.createFutureColumnChart(ndata);
        //console.log(cdata);
    };

    ptr.createFutureColumnChart = function(cdata) {
        var chart = AmCharts.makeChart("future_columnchart", {
            "type": "serial",
            "theme": "dark",
            "colors": ["#7FFFD4", "#008080", "#000080", "#000000"],
            "path": "http://www.amcharts.com/lib/3/",
            "pathToImages": "http://www.amcharts.com/lib/3/images/",    
            "dataProvider": cdata,  
            "legend": {
                "equalWidths": false,
                "useGraphSettings": true
            },
            "valueAxes": [{
                "id": "volumeAxis",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position": "left",
                "title": "volume",        
                "stackType": "regular"
            }, 
            {
                "id": "priceAxis",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "inside": true,
                "position": "right",
                "title": "price"
            }],
            "graphs": [{
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "futurevolume",
                "type": "column",
                "valueField": "futurevolume",
                "valueAxis": "volumeAxis"
            }, 
            {
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "stockvolume",
                "type": "column",
                "newStack": true, 
                "valueField": "stockvolume",
                "valueAxis": "volumeAxis"
            },    
            {
                "balloonText": "p: [[value]]",
                "bullet": "round",
                "bulletBorderAlpha": 1,
                "useLineColorForBulletBorder": true,
                "bulletColor": "#FFFFFF",
                "bulletSizeField": "townSize",
                "dashLengthField": "dashLength",
                "descriptionField": "event",
                "labelPosition": "right",
                "labelText": "[[event]]",
                "legendValueText": "p: [[value]]",
                "title": "futureprice",
                "fillAlphas": 0,
                "valueField": "futureprice",
                "valueAxis": "priceAxis"
            },  
            {
                "balloonText": "p: [[value]]",
                "bullet": "round",
                "bulletBorderAlpha": 1,
                "useLineColorForBulletBorder": true,
                "bulletColor": "#FFFFFF",
                "bulletSizeField": "townSize",
                "dashLengthField": "dashLength",
                "descriptionField": "event",
                "labelPosition": "right",
                "labelText": "[[event]]",
                "legendValueText": "p: [[value]]",
                "title": "stockprice",
                "fillAlphas": 0,
                "valueField": "stockprice",
                "valueAxis": "priceAxis"
            }], 
            "chartCursor": {
                "categoryBalloonDateFormat": "WW",
                "cursorAlpha": 0.1,
                "cursorColor":"#000000",
                "fullWidth":true,
                "valueBalloonsEnabled": false,
                "zoomable": false
            },
            "dataDateFormat": "YYYY-MM-DD", 
            "categoryField": "date",
            "categoryAxis": {
                "dateFormats": [{
                    "period": "DD",
                    "format": "DD"
                }, {
                    "period": "WW",
                    "format": "MMM DD"
                }, {
                    "period": "MM",
                    "format": "MMM"
                }, {
                    "period": "YYYY",
                    "format": "YYYY"
                }],
                "parseDates": true,
                "autoGridCount": false,
                "axisColor": "#555555",
                "gridAlpha": 0.1,
                "gridColor": "#FFFFFF",
                "gridCount": 50,
                "equalSpacing": true
            },
            "connect": false,
            "export": {
                "enabled": true
            },
            "chartScrollbar": {},  
            "chartCursor": {
                "cursorPosition": "mouse"
            }
        });
    };


    ptr.plotFutureData = function(result){
        var stockitem = result.stockitem;  
        var futureitem = result.futureitem;
        var data = [];

        $.each(stockitem[0].datalist, function(d_idx, d_it) {
            var date = new Date(d_it.date);
            data.push({
                "date": yyyymmdd(date),
                "stockopen": parseFloat(d_it.open.toFixed(2)),
                "stockclose": parseFloat(d_it.close.toFixed(2)),
                "stockhigh": parseFloat(d_it.high.toFixed(2)),
                "stocklow": parseFloat(d_it.low.toFixed(2)),
                "stockprice": parseFloat(d_it.close.toFixed(2)),
                "stockvolume": parseInt(d_it.volume.toFixed()),
                "futureopen": 0.00,
                "futureclose": 0.00,
                "futurehigh": 0.00,
                "futurelow": 0.00,
                "futureprice": 0.00,
                "futurevolume": 0
            });
        });

        var ndata = $.extend(true, [], data);
        $.each(futureitem[0].datalist, function(d_idx, d_it) {
            var date = new Date(d_it.date);
            var rst = $.grep(ndata, function(e){ return e.date == yyyymmdd(date); });
            if (rst.length != 0) {
                rst[0].futureopen = parseFloat(d_it.fopen.toFixed(2));
                rst[0].futureclose = parseFloat(d_it.fclose.toFixed(2));
                rst[0].futurehigh = parseFloat(d_it.fhigh.toFixed(2));
                rst[0].futureclose = parseFloat(d_it.fclose.toFixed(2));
                rst[0].futureprice = parseFloat(d_it.fclose.toFixed(2));
                rst[0].futurevolume = parseInt(d_it.fvolume.toFixed());
            }
        });
        
        ptr.createFutureColumnChart(ndata);
        //console.log(cdata);
    };

    ptr.createFutureColumnChart = function(cdata) {
        var chart = AmCharts.makeChart("future_columnchart", {
            "type": "serial",
            "theme": "dark",
            "colors": ["#7FFFD4", "#008080", "#000080", "#000000"],
            "path": "http://www.amcharts.com/lib/3/",
            "pathToImages": "http://www.amcharts.com/lib/3/images/",    
            "dataProvider": cdata,  
            "legend": {
                "equalWidths": false,
                "useGraphSettings": true
            },
            "valueAxes": [{
                "id": "volumeAxis",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position": "left",
                "title": "volume",        
                "stackType": "regular"
            }, 
            {
                "id": "priceAxis",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "inside": true,
                "position": "right",
                "title": "price"
            }],
            "graphs": [{
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "futurevolume",
                "type": "column",
                "valueField": "futurevolume",
                "valueAxis": "volumeAxis"
            }, 
            {
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "stockvolume",
                "type": "column",
                "newStack": true, 
                "valueField": "stockvolume",
                "valueAxis": "volumeAxis"
            },    
            {
                "balloonText": "p: [[value]]",
                "bullet": "round",
                "bulletBorderAlpha": 1,
                "useLineColorForBulletBorder": true,
                "bulletColor": "#FFFFFF",
                "bulletSizeField": "townSize",
                "dashLengthField": "dashLength",
                "descriptionField": "event",
                "labelPosition": "right",
                "labelText": "[[event]]",
                "legendValueText": "p: [[value]]",
                "title": "futureprice",
                "fillAlphas": 0,
                "valueField": "futureprice",
                "valueAxis": "priceAxis"
            },  
            {
                "balloonText": "p: [[value]]",
                "bullet": "round",
                "bulletBorderAlpha": 1,
                "useLineColorForBulletBorder": true,
                "bulletColor": "#FFFFFF",
                "bulletSizeField": "townSize",
                "dashLengthField": "dashLength",
                "descriptionField": "event",
                "labelPosition": "right",
                "labelText": "[[event]]",
                "legendValueText": "p: [[value]]",
                "title": "stockprice",
                "fillAlphas": 0,
                "valueField": "stockprice",
                "valueAxis": "priceAxis"
            }], 
            "chartCursor": {
                "categoryBalloonDateFormat": "WW",
                "cursorAlpha": 0.1,
                "cursorColor":"#000000",
                "fullWidth":true,
                "valueBalloonsEnabled": false,
                "zoomable": false
            },
            "dataDateFormat": "YYYY-MM-DD", 
            "categoryField": "date",
            "categoryAxis": {
                "dateFormats": [{
                    "period": "DD",
                    "format": "DD"
                }, {
                    "period": "WW",
                    "format": "MMM DD"
                }, {
                    "period": "MM",
                    "format": "MMM"
                }, {
                    "period": "YYYY",
                    "format": "YYYY"
                }],
                "parseDates": true,
                "autoGridCount": false,
                "axisColor": "#555555",
                "gridAlpha": 0.1,
                "gridColor": "#FFFFFF",
                "gridCount": 50,
                "equalSpacing": true
            },
            "connect": false,
            "export": {
                "enabled": true
            },
            "chartScrollbar": {},  
            "chartCursor": {
                "cursorPosition": "mouse"
            }
        });
    };


// http://www.amcharts.com/tips/syncing-multiple-pie-charts-with-shared-legend/

    ptr.plotTraderData = function(result) {
        var stockitem = result.stockitem;  
        var traderitem = result.traderitem;
        var index = 0;
        var data = [];
        var pdata = [];
        var cdata;

        $.each(stockitem[0].datalist, function(d_idx, d_it) {
            data.push({
                "date": new Date(d_it.date),
                "stockopen": parseFloat(d_it.open.toFixed(2)),
                "stockclose": parseFloat(d_it.close.toFixed(2)),
                "stockhigh": parseFloat(d_it.high.toFixed(2)),
                "stocklow": parseFloat(d_it.low.toFixed(2)),
                "stockprice": parseFloat(d_it.close.toFixed(2)),
                "stockvolume": parseInt(d_it.volume.toFixed()),
                "traderavgbuyprice": 0.00,
                "traderavgsellprice": 0.00,
                "traderbuyvolume": 0.00,
                "tradersellvolume": 0.00,
                "event": ""
            });
        });

        $.each(traderitem, function(t_idx, t_it) {
            var ndata = $.extend(true, [], data);
            $.each(t_it.datalist, function(d_idx, d_it) {
                var date = new Date(d_it.date);
                var rst = $.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
                if (rst.length != 0) {
                    rst[0].traderavgbuyprice = parseFloat(d_it.avgbuyprice.toFixed(2));
                    rst[0].traderavgsellprice = parseFloat(d_it.avgsellprice.toFixed(2));
                    rst[0].traderbuyvolume = parseInt(d_it.buyvolume.toFixed());
                    rst[0].tradersellvolume = parseInt(d_it.sellvolume.toFixed());
                }
            });

            var unit = {
                  "index": index++,
                  "traderidnm": t_it.traderid + "-" + t_it.tradernm,
                  "stockidnm": t_it.stockid + "-" + t_it.stocknm,
                  "totalbuyvolume": parseInt(t_it.totalbuyvolume.toFixed()),
                  "totalsellvolume": parseInt(t_it.totalsellvolume.toFixed()),
                  "description": "",
                  "data": ndata
            }
            pdata.push(unit);
        });

        cdata = ptr.generateCollectiveData(pdata);
        bchart = ptr.createTopBuyPieChart(pdata);
        schart = ptr.createTopSellPieChart(pdata);
        mchart = ptr.createTopMapColumnChart(cdata);
        ptr.createCallBackListener(bchart, schart, mchart, cdata);
        // console.log(pdata);
        // console.log(cdata);
    };

    ptr.generateCollectiveData = function(pdata){
        // aggregate collective data
        var cdata = []
        for (var x in pdata) {
            var dp = pdata[x];
            if ( 0 == x ) {
                for (var y in dp.data) {
                    cdata.push({
                        "date": dp.data[y].date,
                        "traderbuyvolume": dp.data[y].traderbuyvolume,
                        "tradersellvolume": dp.data[y].tradersellvolume,
                        "traderavgbuyprice": dp.data[y].traderavgbuyprice * dp.data[y].traderbuyvolume,
                        "traderavgsellprice": dp.data[y].traderavgsellprice * dp.data[y].tradersellvolume,
                        "stockvolume": dp.data[y].stockvolume,
                        "stockprice": dp.data[y].stockprice
                    });
                }
            }
            else {
                for (var y in dp.data) {
                    cdata[y].traderbuyvolume += dp.data[y].traderbuyvolume;
                    cdata[y].tradersellvolume += dp.data[y].tradersellvolume;
                    cdata[y].traderavgbuyprice += dp.data[y].traderavgbuyprice * dp.data[y].traderbuyvolume;
                    cdata[y].traderavgsellprice += dp.data[y].traderavgsellprice * dp.data[y].tradersellvolume
                }
            }
        }
        for (var x in cdata) {
            cdata[x].traderavgbuyprice = Math.floor(cdata[x].traderavgbuyprice / cdata[x].traderbuyvolume);
            cdata[x].traderavgsellprice = Math.floor(cdata[x].traderavgsellprice / cdata[x].tradersellvolume);
        }
        return cdata
    };

    ptr.createTopBuyPieChart = function(pdata) {
        var chart = AmCharts.makeChart("topbuy_piechart", {
            "type": "pie",
            "theme": "dark",
            "colors": ["#006400", "#008000", "#228B22", "#2E8B57", "#3CB371", 
                       "#8FBC8F", "#98FB98", "#90EE90", "#00FA9A", "#00FF7F",
                       "#ADFF2F", "#7FFF00", "#7CFC00", "#00FF00", "#32CD32", 
                       "#9ACD32", "#6B8123", "#808000", "#556B2F", "#008B8B"],
            "path": "http://www.amcharts.com/lib/3/",
            "out": false,
            "dataProvider": pdata,
            "valueField": "totalbuyvolume",
            "titleField": "traderidnm",
            "labelText": "[[title]]: \n[[value]]",
            "pullOutOnlyOne": true,
             "export": {
                     "enabled": true
              }
        });
        return chart;
    };

    ptr.createTopSellPieChart = function(pdata) {
        var chart = AmCharts.makeChart("topsell_piechart", {
            "type": "pie",
            "theme": "dark",
            "colors": ["#FF0000", "#8B0000", "#B22222", "#DC143C", "#CD5C5C", 
                       "#F08080", "#E98072", "#FRA07A", "#C71585", "#DB7093", 
                       "#FF1493", "#FF69B4", "#FFB6C1", "#FFC0CB", "#FFA500", 
                       "#FFA500", "#FF8C00", "#FF7F50", "#FF6347", "#FF4500"],
            "path": "http://www.amcharts.com/lib/3/",
            "out": false,
            "dataProvider": pdata,
            "valueField": "totalsellvolume",
            "titleField": "traderidnm",
            "labelText": "[[title]]: \n[[value]]",
            "pullOutOnlyOne": true,
             "export": {
                     "enabled": true
              }
        });
        return chart;
    };

    ptr.createTopMapColumnChart = function(cdata) {
        var chart = AmCharts.makeChart("topmap_columnchart", {
            "type": "serial",
            "theme": "dark",
            "colors": ["#5F9EA0", "#7FFFD4", "#008080", "#000080", "#800080", "#000000"],
            "path": "http://www.amcharts.com/lib/3/",
            "pathToImages": "http://www.amcharts.com/lib/3/images/",    
            "dataProvider": cdata,  
            "legend": {
                "equalWidths": false,
                "useGraphSettings": true
            },
            "valueAxes": [{
                "id": "volumeAxis",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position": "left",
                "title": "volume",        
                "stackType": "regular"
            }, 
            {
                "id": "priceAxis",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "inside": true,
                "position": "right",
                "title": "price"
            }],
            "graphs": [{
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "traderbuyvolume",
                "type": "column",
                "valueField": "traderbuyvolume",
                "valueAxis": "volumeAxis"
            },
            {
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "tradersellvolume",
                "type": "column",
                "valueField": "tradersellvolume",
                "valueAxis": "volumeAxis"
            },  
            {
                "balloonText": "[[value]]",
                "dashLengthField": "dashLength",
                "fillAlphas": 0.7,
                "legendPeriodValueText": "[[value]]",
                "legendValueText": "v: [[value]]",
                "title": "stockvolume",
                "type": "column",
                "newStack": true,
                "valueField": "stockvolume",
                "valueAxis": "volumeAxis"
            },             
            {
                "balloonText": "p:[[value]]",
                "bullet": "round",
                "bulletBorderAlpha": 1,
                "useLineColorForBulletBorder": true,
                "bulletColor": "#FFFFFF",
                "bulletSizeField": "townSize",
                "dashLengthField": "dashLength",
                "descriptionField": "event",
                "labelPosition": "right",
                "labelText": "[[event]]",
                "legendValueText": "p: [[value]]",
                "title": "traderavgbuyprice",
                "fillAlphas": 0,
                "valueField": "traderavgbuyprice",
                "valueAxis": "priceAxis"
            },
            {
                "balloonText": "p:[[value]]",
                "bullet": "round",
                "bulletBorderAlpha": 1,
                "useLineColorForBulletBorder": true,
                "bulletColor": "#FFFFFF",
                "bulletSizeField": "townSize",
                "dashLengthField": "dashLength",
                "descriptionField": "event",
                "labelPosition": "right",
                "labelText": "[[event]]",
                "legendValueText": "p: [[value]]",
                "title": "traderavgsellprice",
                "fillAlphas": 0,
                "valueField": "traderavgsellprice",
                "valueAxis": "priceAxis"
            },
            {
                "balloonText": "p: [[value]]",
                "bullet": "round",
                "bulletBorderAlpha": 1,
                "useLineColorForBulletBorder": true,
                "bulletColor": "#FFFFFF",
                "bulletSizeField": "townSize",
                "dashLengthField": "dashLength",
                "descriptionField": "event",
                "labelPosition": "right",
                "labelText": "[[event]]",
                "legendValueText": "p: [[value]]",
                "title": "stockprice",
                "fillAlphas": 0,
                "valueField": "stockprice",
                "valueAxis": "priceAxis"
            }], 
            "chartCursor": {
                "categoryBalloonDateFormat": "WW",
                "cursorAlpha": 0.1,
                "cursorColor":"#000000",
                "fullWidth":true,
                "valueBalloonsEnabled": false,
                "zoomable": false
            },
            "dataDateFormat": "YYYY-MM-DD", 
            "categoryField": "date",
            "categoryAxis": {
                "dateFormats": [{
                    "period": "DD",
                    "format": "DD"
                }, {
                    "period": "WW",
                    "format": "MMM DD"
                }, {
                    "period": "MM",
                    "format": "MMM"
                }, {
                    "period": "YYYY",
                    "format": "YYYY"
                }],
                "parseDates": true,
                "autoGridCount": false,
                "axisColor": "#555555",
                "gridAlpha": 0.1,
                "gridColor": "#FFFFFF",
                "gridCount": 50,
                "equalSpacing": true
            },
            "connect": false,
            "export": {
                "enabled": true
            },
            "chartScrollbar": {},  
            "chartCursor": {
                "cursorPosition": "mouse"
            }
        });
    return chart;
    };

    // bug index not align when buy/sell traders not tuple match
    ptr.createCallBackListener = function(bchart, schart, mchart, cdata){
        bchart.addListener("pullOutSlice", function (event) {
            if (bchart.out == true) { 
                return;
            }
            index = event.dataItem.dataContext.index;
            mchart.dataProvider = event.dataItem.dataContext.data;
            mchart.validateData();
            mchart.animateAgain();
            if (schart.out == false) {
                schart.out = true;
                schart.clickSlice(index);
            }
            bchart.out = true;
        });
        bchart.addListener("pullInSlice", function (event) {
            if (bchart.out == false) {
                return;
            }
            index = event.dataItem.dataContext.index;
            mchart.dataProvider = cdata;
            mchart.validateData();
            mchart.animateAgain();
            if  (schart.out == true){
                schart.out = false;
                schart.clickSlice(index);
            }
            bchart.out = false;
        });
        schart.addListener("pullOutSlice", function (event) {
            if (schart.out == true) {
                return;
            }
            index = event.dataItem.dataContext.index;
            mchart.dataProvider = event.dataItem.dataContext.data;
            mchart.validateData();
            mchart.animateAgain();
            if (bchart.out == false) {
                bchart.out = true;
                bchart.clickSlice(index);
            }
            schart.out = true;
        });
        schart.addListener("pullInSlice", function (event) {
            if (schart.out == false) {
                return;
            }
            index = event.dataItem.dataContext.index;
            mchart.dataProvider = cdata;
            mchart.validateData();
            mchart.animateAgain();
            if (bchart.out == true){
                bchart.out = false;
                bchart.clickSlice(index);
            }
            schart.out = false;
        });
    };
    
    ptr.plotTableData = function(result){
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
    };

    return ptr;
};
