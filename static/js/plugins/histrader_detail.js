function loadChartData(settings) {
    // host:port ...
    var URL = "http://127.0.0.1:8000/handler/api/histrader_detail/?";
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
            // auto refresh after time out
            setTimeout(loadChartData, 10*60*1000); 
        },

        success: function (result) {
            //
            generateChartData(result);
        },

        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
            $("#topbuy_piechart").hide();
            $("#topsell_piechart").hide();
        }
    });
}

function generateChartData(result) {
    var traderitem = result.traderitem;
    var index = 0;
    var pdata = [];

    // populate traderitem
    $.each(traderitem, function(t_idx, t_it) {
         var unit = {
              "index": index++,
              "traderidnm": t_it.traderid + "-" + t_it.tradernm,
              "stockidnm": t_it.stockid + "-" + t_it.stocknm,
              "totalbuyvolume": parseInt(t_it.totalbuyvolume.toFixed()),
              "totalsellvolume": parseInt(t_it.totalsellvolume.toFixed()),
              "description": ""
        }
        pdata.push(unit);
    });

    bchart = createTopBuyPieChart(pdata);
    schart = createTopSellPieChart(pdata);
    //createCallBackListener(bchart, schart, mchart, cdata);
}

function createTopBuyPieChart(pdata) {
    var chart = AmCharts.makeChart("topbuy_piechart", {
        "type": "pie",
        "theme": "dark",
        "path": "http://www.amcharts.com/lib/3/",
        "out": false,
        "dataProvider": pdata,
        "valueField": "totalbuyvolume",
        "titleField": "stockidnm",
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
        "titleField": "stockidnm",
        "labelText": "[[title]]: [[value]]",
        "pullOutOnlyOne": true,
         "export": {
                 "enabled": true
          }
    });
    return chart;
}