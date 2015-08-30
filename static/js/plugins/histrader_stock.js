
function plotStockData(result) {
    var traderitem = result.traderitem;
    var index = 0;
    var pdata = [];

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

    cdata = generateCollectiveData(pdata);
    bchart = createTopBuyPieChart(pdata);
    schart = createTopSellPieChart(pdata);
    //createCallBackListener(bchart, schart, mchart, cdata);
}

function generateCollectiveData(pdata){
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