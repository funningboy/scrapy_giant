
function loadChartData(settings) {
    // host:port ...
    var URL = "http://127.0.0.1:8000/handler/api/hisstock_detail/?";
    $.each(settings, function(k, v) {
        if (k == "stockids" || k == "traderids") {
            v = v.join();
        }
        URL = URL + k + "=" + v +"&"
    });
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
            $("#topbuy_piechart").show();
            $("#topsell_piechart").show();
            $("#topmap_columnchart").show();
            // auto refresh after time out
            setTimeout(loadChartData, 10*60*1000); 
        },

        success: function (result) {
            //
            generateChartData(result);
            generateTableData(result);
        },

        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
            $("#topbuy_piechart").hide();
            $("#topsell_piechart").hide();
            $("#topmap_columnchart").hide();
        }
    });
}

function generateChartData(result) {
    var stockitem = result.stockitem;  
    var traderitem = result.traderitem;
    var index = 0;
    var data = [];
    var pdata = [];
    var cdata;

    // populate stockitem 
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

    // populate traderitem
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

    cdata = generateCollectiveData(pdata);
    bchart = createTopBuyPieChart(pdata);
    schart = createTopSellPieChart(pdata);
    mchart = createTopMapColumnChart(cdata);
    createCallBackListener(bchart, schart, mchart, cdata);

    // console.log(pdata);
    // console.log(cdata);
}

function generateCollectiveData(pdata){
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
}

function createTopBuyPieChart(pdata) {
    var chart = AmCharts.makeChart("topbuy_piechart", {
        "type": "pie",
        "theme": "dark",
        "path": "http://www.amcharts.com/lib/3/",
        "out": false,
        "dataProvider": pdata,
        "valueField": "totalbuyvolume",
        "titleField": "traderidnm",
        "labelText": "[[title]]: [[value]]",
        "pullOutOnlyOne": true,
         "export": {
                 "enabled": true
          }
    });
    return chart;
}

function createTopSellPieChart(pdata) {
    var chart = AmCharts.makeChart("topsell_piechart", {
        "type": "pie",
        "theme": "dark",
        "path": "http://www.amcharts.com/lib/3/",
        "out": false,
        "dataProvider": pdata,
        "valueField": "totalsellvolume",
        "titleField": "traderidnm",
        "labelText": "[[title]]: [[value]]",
        "pullOutOnlyOne": true,
         "export": {
                 "enabled": true
          }
    });
    return chart;
}

function createTopMapColumnChart(cdata) {
    // create column chart
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
            "gridCount": 50
        },
        "export": {
            "enabled": true
        },
        "chartScrollbar": {},  
        "chartCursor": {
            "cursorPosition": "mouse"
        }
    });
return chart;
}

// bug index not align when buy/sell traders not tuple match
function createCallBackListener(bchart, schart, mchart, cdata){
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
}

function generateTableData(result){
    var stockitem = result.stockitem;
    var credititem = result.credititem;
    var data = [];

    // try iter to fill all fields
    // populate stockitem 
    $.each(stockitem[0].datalist, function(d_idx, d_it) {
        var date = new Date(d_it.date);
        data.push({
            "date": yyyymmdd(date),
            "open": d_it.open.toFixed(2),
            "close": d_it.close.toFixed(2),
            "high": d_it.high.toFixed(2),
            "low": d_it.low.toFixed(2),
            "volume": d_it.volume.toFixed(),
            "finaused" : 0.00,
            "bearused": 0.00,
            "future": 0.00,
            "event": ""
        });
    });

    // populate credititem
    var ndata = $.extend(true, [], data);
    $.each(credititem[0].datalist, function(d_idx, d_it) {
        var date = new Date(d_it.date);
        var rst = $.grep(ndata, function(e){ return e.date == yyyymmdd(date); });
        if (rst.length != 0) {
            rst[0].finaused = d_it.financeused.toFixed(2);
            rst[0].bearused = d_it.bearishused.toFixed(2);
        }
    });

    // populate futureitem

    $('#stockdetail_table').dynatable({
        dataset: {
            records: ndata
        }
    });

    //console.log(data);
}

