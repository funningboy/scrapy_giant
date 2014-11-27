var chartData = [{
    "traderid": "中國信託",
        "stockid": "2330",
        "tradervolume": 200, // sum volume during this time period 2012-01-01/2012-01-02
    "url": "#",
        "description": "trader:1111 vs stock: 2330",
        "data": [{
        "date": new Date("2012-01-01"),
            "traderprice": 100,
            "traderbuyvolume": 100,
            "tradersellvolume": 100,
            "tradersumvolume": 200,
            "stockprice": 101,
            "stockvolume": 1000,
            "event": "call"
    }, {
        "date": new Date("2012-01-02"),
            "traderprice": 99,
            "traderbuyvolume": 100,
            "tradersellvolume": 100,
            "tradersumvolume": 200,
            "stockprice": 102,
            "stockvolume": 500,
            "event": "put"
    }]
}, {
    "traderid": "2222",
        "stockid": "2330",
        "tradervolume": 400,
        "url": "#",
        "description": "trader:2222 vs stock:2330",
        "data": [{
        "date": new Date("2012-01-01"),
            "traderprice": 98,
            "traderbuyvolume": 200,
            "tradersellvolume": 200,
            "tradersumvolume": 400,
            "stockprice": 101,
            "stockvolume": 1000,
            "event": "put"
    }, {
        "date": new Date("2012-01-02"),
            "traderprice": 97,
            "traderbuyvolume": 200,
            "tradersellvolume": 200,
            "tradersumvolume": 400,
            "stockprice": 102,
            "stockvolume": 500,
            "event": "call"
    }]
}];

// aggregate collective data
var collectiveData = [];
for (var x in chartData) {
    var dataPoint = chartData[x];
    if (0 == x) {
        for (var y in dataPoint.data) {
            collectiveData.push({
                "date": dataPoint.data[y].date,
                    "traderbuyvolume": dataPoint.data[y].traderbuyvolume,
                    "tradersellvolume": dataPoint.data[y].tradersellvolume,
                    "tradersumvolume": dataPoint.data[y].tradersumvolume,
                    "traderprice": dataPoint.data[y].traderprice * dataPoint.data[y].tradersumvolume,
                    "stockvolume": dataPoint.data[y].stockvolume,
                    "stockprice": dataPoint.data[y].stockprice
            });
        }
    } else {
        for (var y in dataPoint.data) {
            collectiveData[y].traderbuyvolume += dataPoint.data[y].traderbuyvolume;
            collectiveData[y].tradersellvolume += dataPoint.data[y].tradersellvolume;
            collectiveData[y].tradersumvolume += dataPoint.data[y].tradersumvolume;
            collectiveData[y].traderprice += dataPoint.data[y].traderprice * dataPoint.data[y].tradersumvolume;
        }
    }
}
for (var x in collectiveData) {
    collectiveData[x].traderprice = Math.floor(collectiveData[x].traderprice / collectiveData[x].tradersumvolume);
}


// create pie chart
var chart = AmCharts.makeChart("chartdiv1", {
    "type": "pie",
        "dataProvider": chartData,
        "valueField": "tradervolume",
        "titleField": "traderid",
        "labelText": "[[title]]: [[value]]",
        "legend": {
        "markerType": "circle",
            "position": "right",
            "marginRight": 80,
            "autoMargins": false
    },
        "pullOutOnlyOne": true
});

// create column chart
var chart2 = AmCharts.makeChart("chartdiv2", {
    "type": "serial",
        "theme": "none",
        "pathToImages": "http://www.amcharts.com/lib/3/images/",
        "dataProvider": collectiveData,
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
    }, {
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
    }, {
        "balloonText": "[[value]]",
            "dashLengthField": "dashLength",
            "fillAlphas": 0.7,
            "legendPeriodValueText": "[[value]]",
            "legendValueText": "v: [[value]]",
            "title": "tradersellvolume",
            "type": "column",
            "valueField": "tradersellvolume",
            "valueAxis": "volumeAxis"
    }, {
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
    }, {
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
            "title": "traderprice",
            "fillAlphas": 0,
            "valueField": "traderprice",
            "valueAxis": "priceAxis"
    }, {
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
            "cursorColor": "#000000",
            "fullWidth": true,
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
        "exportConfig": {
        "menuBottom": "20px",
            "menuRight": "22px",
            "menuItems": [{
            "icon": 'http://www.amcharts.com/lib/3/images/export.png',
                "format": 'png'
        }]
    },
        "chartScrollbar": {},
        "chartCursor": {
        "cursorPosition": "mouse"
    },
});

chart.addListener("pullOutSlice", function (event) {
    chart2.dataProvider = event.dataItem.dataContext.data;
    //    chart2.titles[0].text = event.dataItem.dataContext.department;
    chart2.validateData();
    chart2.animateAgain();
    
//    chart3.dataProvider = event.dataItem.dataContext.data;
});

chart.addListener("pullInSlice", function (event) {
    chart2.dataProvider = collectiveData;
    //    chart2.titles[0].text = "All departments";
    chart2.validateData();
    chart2.animateAgain();
});
