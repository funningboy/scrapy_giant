
var histraderdetail = function() {
    ptr.version = '0.1.6';
    ptr.status = null;

        console.log(encodeURI(URL));
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

                setTimeout(ptr.loadChartData, 10*60*1000); 
            },

            success: function (result) {
                try {
                    ptr.plotStockData(result);
                } catch(err) {
                    console.log("plotStockData fail");
                }
                try {
                    ptr.plotlTableData(result);
                } catch(err) {
                    console.log("plotlTableData fail");
                }
            },

            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);

            }
        });

        ptr.plotStockData = function(result) {
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
                data = $.extend(true, [], data);
                $.each(t_it.datalist, function(d_idx, d_it) {
                    var date = new Date(d_it.date);
                    var rst = $.grep(data, function(e){ return e.date.getTime() == date.getTime(); });
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
                      "data": data
                }
                pdata.push(unit);
            });

            cdata = generateCollectiveData(pdata);
            bchart = createTopBuyPieChart(pdata);
            schart = createTopSellPieChart(pdata);
            mchart = createTopMapColumnChart(cdata);
            createCallBackListener(bchart, schart, mchart, cdata);
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
            return cdata;
        };

        ptr.createTopBuyPieChart = function(pdata) {
            var chart = AmCharts.makeChart("topbuy_piechart", {
                "type": "pie",
                "theme": "dark",
                "path": "http://www.amcharts.com/lib/3/",
                "out": false,
                "dataProvider": pdata,
                "valueField": "totalbuyvolume",
                "titleField": "stockidnm",
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
                "path": "http://www.amcharts.com/lib/3/",
                "out": false,
                "dataProvider": pdata,
                "valueField": "totalsellvolume",
                "titleField": "stockidnm",
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


    function plotTableData(result){
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
                    "buy": 0.00,
                    "sell": 0.00,
                    "topbuy0": "",
                    "topbuy1": "",
                    "topbuy2": "",
                    "topsell0": "",
                    
                    "expect": "",
                    "accuracy": "",
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

    return ptr;
};




