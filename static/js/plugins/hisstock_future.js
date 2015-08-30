

function plotFutureData(result){
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
    
    createFutureColumnChart(ndata);
    //console.log(cdata);
}

function createFutureColumnChart(cdata) {
    var chart = AmCharts.makeChart("future_columnchart", {
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
}
