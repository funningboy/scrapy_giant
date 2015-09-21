

function plotCreditData(result){
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

    // try except
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
    
    createCreditColumnChart(ndata);
    //console.log(cdata);
}

function createCreditColumnChart(cdata) {
    var chart = AmCharts.makeChart("credit_columnchart", {
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
}