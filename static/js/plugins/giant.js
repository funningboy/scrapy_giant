// http://www.amcharts.com/tips/syncing-zoom-across-several-date-based-serial-charts/

var giant = function(){
	ptr = {};
	ptr.version = '0.1.6';
	ptr.status = null;

	ptr.start = function() {};
	ptr.close = function() {};
	
	return ptr;
};

function yyyymmdd(date) {
    var yyyy = date.getFullYear().toString()
    var mm = (date.getMonth()+1).toString();
    var dd  = date.getDate().toString();
    return yyyy + '/' + (mm[1]?mm:"0"+mm[0]) + '/' + (dd[1]?dd:"0"+dd[0]);
};
/*

    ptr.credit = {
        jQptr: $("credit_columnchart"),
        chart: {},
        timeout: 30*1000,

        _load: function(data){
            var stockitem = data.stockitem;  
            var credititem = data.credititem;
            var item = [];

            $.each(stockitem[0].datalist, function(d_idx, d_it) {
                var date = new Date(d_it.date);
                item.push({
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

            item = $.extend(true, [], item);
            $.each(credititem[0].datalist, function(d_idx, d_it) {
                var date = new Date(d_it.date);
                var rst = $.grep(item, function(e){ return e.date == yyyymmdd(date); });
                if (rst.length != 0) {
                    rst[0].finaremain = parseFloat(d_it.financeremain.toFixed(2));
                    rst[0].bearremain = parseFloat(d_it.bearishremain.toFixed(2));
                    rst[0].finabuyvolume = parseInt(d_it.financebuyvolume.toFixed());
                    rst[0].finasellvolume = parseInt(d_it.financesellvolume.toFixed());
                    rst[0].bearbuyvolume = parseInt(d_it.bearishbuyvolume.toFixed());
                    rst[0].bearsellvolume = parseInt(d_it.bearishsellvolume.toFixed());
                }
            });

            return item;
        },

        _plot: function(cdata) {
            var chart = AmCharts.makeChart("credit_columnchart", {
                "type": "serial",
                "theme": "dark",
                "colors": ["#5F9EA0", "#7FFFD4", "#20B2AA", "#E0FFFF", "#008080", "#000000"],
                "path": "http://www.amcharts.com/lib/3/",
                "pathToImages": "http://www.amcharts.com/lib/3/images/",    
                "dataProvider": cdata,  
                "legend": {
                    "horizontalGap": 10,
                    "maxColumns": 1,
                    "position": "left",
                    "useGraphSettings": true,
                    "markerSize": 10,
                    "equalWidths": false
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
            return chart;
        },

        sync: function() {
            if (ptr.status != 'success') {
                if (ptr.status == 'error') {
                    return;
                }
                setTimeout(ptr.credit.sync, ptr.credit.timeout);
            } else {
                var item;
                item = ptr.credit._load(ptr.data);
                ptr.credit.chart = ptr.credit._plot(item);
            }
        }
    };

*/