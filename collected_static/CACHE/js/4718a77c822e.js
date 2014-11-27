//<![CDATA[ 
window.onload=function(){
AmCharts.ready(function () {
    generateChartData();
    checkChartData();
    generateCollectiveData();
    createPieChart();
    createColumnChart();
    callbackPieChart();
});

var pieChart;
var stockChart;
var chartData = [];
var collectiveData = [];

function generateChartData() {
    var data = [];
    // populate stock data as init
    
        
		    data.unshift({
                "date": new Date("2014-11-26T00:00:00"),
                "stockopen": 11.0,
                "stockclose": 11.0,
                "stockhigh": 11.5,
                "stocklow": 10.85,
                "stockprice": 11.0,
                "stockvolume": 7076,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-25T00:00:00"),
                "stockopen": 11.65,
                "stockclose": 11.65,
                "stockhigh": 11.65,
                "stocklow": 11.65,
                "stockprice": 11.65,
                "stockvolume": 2342,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-24T00:00:00"),
                "stockopen": 12.5,
                "stockclose": 12.5,
                "stockhigh": 12.5,
                "stocklow": 12.5,
                "stockprice": 12.5,
                "stockvolume": 414,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-21T00:00:00"),
                "stockopen": 13.4,
                "stockclose": 13.4,
                "stockhigh": 13.4,
                "stocklow": 13.4,
                "stockprice": 13.4,
                "stockvolume": 106,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-20T00:00:00"),
                "stockopen": 14.4,
                "stockclose": 14.4,
                "stockhigh": 14.4,
                "stocklow": 14.4,
                "stockprice": 14.4,
                "stockvolume": 54,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-19T00:00:00"),
                "stockopen": 15.45,
                "stockclose": 15.45,
                "stockhigh": 15.45,
                "stocklow": 15.45,
                "stockprice": 15.45,
                "stockvolume": 128,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-18T00:00:00"),
                "stockopen": 16.6,
                "stockclose": 16.6,
                "stockhigh": 16.6,
                "stocklow": 16.6,
                "stockprice": 16.6,
                "stockvolume": 466,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-17T00:00:00"),
                "stockopen": 18.2,
                "stockclose": 17.8,
                "stockhigh": 18.2,
                "stocklow": 17.65,
                "stockprice": 17.8,
                "stockvolume": 361,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-14T00:00:00"),
                "stockopen": 18.0,
                "stockclose": 17.8,
                "stockhigh": 18.1,
                "stocklow": 17.65,
                "stockprice": 17.8,
                "stockvolume": 454,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-13T00:00:00"),
                "stockopen": 17.5,
                "stockclose": 18.1,
                "stockhigh": 18.2,
                "stocklow": 17.35,
                "stockprice": 18.1,
                "stockvolume": 377,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-12T00:00:00"),
                "stockopen": 17.8,
                "stockclose": 18.2,
                "stockhigh": 18.4,
                "stocklow": 17.8,
                "stockprice": 18.2,
                "stockvolume": 554,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-11T00:00:00"),
                "stockopen": 18.0,
                "stockclose": 17.8,
                "stockhigh": 18.4,
                "stocklow": 17.8,
                "stockprice": 17.8,
                "stockvolume": 539,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-10T00:00:00"),
                "stockopen": 18.1,
                "stockclose": 18.15,
                "stockhigh": 18.4,
                "stocklow": 18.0,
                "stockprice": 18.15,
                "stockvolume": 281,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-07T00:00:00"),
                "stockopen": 18.25,
                "stockclose": 18.1,
                "stockhigh": 18.4,
                "stocklow": 18.0,
                "stockprice": 18.1,
                "stockvolume": 404,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-06T00:00:00"),
                "stockopen": 18.9,
                "stockclose": 18.15,
                "stockhigh": 18.9,
                "stocklow": 18.05,
                "stockprice": 18.15,
                "stockvolume": 757,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-05T00:00:00"),
                "stockopen": 18.4,
                "stockclose": 18.5,
                "stockhigh": 18.75,
                "stocklow": 18.4,
                "stockprice": 18.5,
                "stockvolume": 769,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-04T00:00:00"),
                "stockopen": 18.95,
                "stockclose": 18.65,
                "stockhigh": 18.95,
                "stocklow": 18.35,
                "stockprice": 18.65,
                "stockvolume": 2107,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-03T00:00:00"),
                "stockopen": 19.3,
                "stockclose": 19.3,
                "stockhigh": 19.3,
                "stocklow": 19.3,
                "stockprice": 19.3,
                "stockvolume": 1726,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-31T00:00:00"),
                "stockopen": 17.0,
                "stockclose": 18.05,
                "stockhigh": 18.05,
                "stocklow": 16.9,
                "stockprice": 18.05,
                "stockvolume": 1712,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-30T00:00:00"),
                "stockopen": 17.25,
                "stockclose": 16.9,
                "stockhigh": 17.25,
                "stocklow": 16.75,
                "stockprice": 16.9,
                "stockvolume": 691,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-29T00:00:00"),
                "stockopen": 17.4,
                "stockclose": 17.25,
                "stockhigh": 17.4,
                "stocklow": 17.05,
                "stockprice": 17.25,
                "stockvolume": 446,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-28T00:00:00"),
                "stockopen": 16.7,
                "stockclose": 17.05,
                "stockhigh": 17.1,
                "stocklow": 16.7,
                "stockprice": 17.05,
                "stockvolume": 377,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-27T00:00:00"),
                "stockopen": 17.0,
                "stockclose": 16.55,
                "stockhigh": 17.05,
                "stocklow": 16.5,
                "stockprice": 16.55,
                "stockvolume": 412,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-24T00:00:00"),
                "stockopen": 17.0,
                "stockclose": 16.85,
                "stockhigh": 17.0,
                "stocklow": 16.8,
                "stockprice": 16.85,
                "stockvolume": 508,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-23T00:00:00"),
                "stockopen": 17.0,
                "stockclose": 16.85,
                "stockhigh": 17.05,
                "stocklow": 16.8,
                "stockprice": 16.85,
                "stockvolume": 280,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-22T00:00:00"),
                "stockopen": 17.5,
                "stockclose": 17.15,
                "stockhigh": 17.5,
                "stocklow": 17.05,
                "stockprice": 17.15,
                "stockvolume": 748,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-21T00:00:00"),
                "stockopen": 17.0,
                "stockclose": 17.05,
                "stockhigh": 17.3,
                "stocklow": 16.8,
                "stockprice": 17.05,
                "stockvolume": 807,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-20T00:00:00"),
                "stockopen": 16.85,
                "stockclose": 17.0,
                "stockhigh": 17.0,
                "stocklow": 16.15,
                "stockprice": 17.0,
                "stockvolume": 1148,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-17T00:00:00"),
                "stockopen": 17.4,
                "stockclose": 16.2,
                "stockhigh": 17.7,
                "stocklow": 16.2,
                "stockprice": 16.2,
                "stockvolume": 1835,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-16T00:00:00"),
                "stockopen": 17.6,
                "stockclose": 17.4,
                "stockhigh": 17.9,
                "stocklow": 16.95,
                "stockprice": 17.4,
                "stockvolume": 746,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-15T00:00:00"),
                "stockopen": 18.3,
                "stockclose": 17.9,
                "stockhigh": 18.3,
                "stocklow": 17.9,
                "stockprice": 17.9,
                "stockvolume": 569,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-14T00:00:00"),
                "stockopen": 18.0,
                "stockclose": 18.3,
                "stockhigh": 18.5,
                "stocklow": 18.0,
                "stockprice": 18.3,
                "stockvolume": 656,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-13T00:00:00"),
                "stockopen": 19.0,
                "stockclose": 18.6,
                "stockhigh": 19.45,
                "stocklow": 18.5,
                "stockprice": 18.6,
                "stockvolume": 1123,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-09T00:00:00"),
                "stockopen": 20.25,
                "stockclose": 19.85,
                "stockhigh": 20.5,
                "stocklow": 19.85,
                "stockprice": 19.85,
                "stockvolume": 655,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-08T00:00:00"),
                "stockopen": 20.5,
                "stockclose": 20.15,
                "stockhigh": 20.5,
                "stocklow": 20.15,
                "stockprice": 20.15,
                "stockvolume": 685,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-07T00:00:00"),
                "stockopen": 20.8,
                "stockclose": 20.55,
                "stockhigh": 20.8,
                "stocklow": 20.5,
                "stockprice": 20.55,
                "stockvolume": 653,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-06T00:00:00"),
                "stockopen": 20.5,
                "stockclose": 20.95,
                "stockhigh": 21.4,
                "stocklow": 20.5,
                "stockprice": 20.95,
                "stockvolume": 1282,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-03T00:00:00"),
                "stockopen": 20.45,
                "stockclose": 20.55,
                "stockhigh": 20.75,
                "stocklow": 20.4,
                "stockprice": 20.55,
                "stockvolume": 702,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-02T00:00:00"),
                "stockopen": 21.0,
                "stockclose": 20.6,
                "stockhigh": 21.0,
                "stocklow": 20.25,
                "stockprice": 20.6,
                "stockvolume": 1494,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-01T00:00:00"),
                "stockopen": 21.55,
                "stockclose": 21.2,
                "stockhigh": 21.6,
                "stocklow": 21.05,
                "stockprice": 21.2,
                "stockvolume": 699,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-30T00:00:00"),
                "stockopen": 21.6,
                "stockclose": 21.4,
                "stockhigh": 21.6,
                "stocklow": 21.0,
                "stockprice": 21.4,
                "stockvolume": 997,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-29T00:00:00"),
                "stockopen": 21.45,
                "stockclose": 21.05,
                "stockhigh": 21.45,
                "stocklow": 20.95,
                "stockprice": 21.05,
                "stockvolume": 906,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-26T00:00:00"),
                "stockopen": 21.3,
                "stockclose": 21.45,
                "stockhigh": 22.0,
                "stocklow": 21.3,
                "stockprice": 21.45,
                "stockvolume": 4313,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-25T00:00:00"),
                "stockopen": 23.6,
                "stockclose": 22.85,
                "stockhigh": 23.6,
                "stocklow": 22.5,
                "stockprice": 22.85,
                "stockvolume": 5275,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-24T00:00:00"),
                "stockopen": 20.9,
                "stockclose": 22.35,
                "stockhigh": 22.35,
                "stocklow": 20.9,
                "stockprice": 22.35,
                "stockvolume": 3876,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-23T00:00:00"),
                "stockopen": 20.8,
                "stockclose": 20.9,
                "stockhigh": 21.15,
                "stocklow": 20.8,
                "stockprice": 20.9,
                "stockvolume": 544,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-22T00:00:00"),
                "stockopen": 21.2,
                "stockclose": 20.9,
                "stockhigh": 21.2,
                "stocklow": 20.8,
                "stockprice": 20.9,
                "stockvolume": 315,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-19T00:00:00"),
                "stockopen": 21.2,
                "stockclose": 21.2,
                "stockhigh": 21.25,
                "stocklow": 20.85,
                "stockprice": 21.2,
                "stockvolume": 502,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-18T00:00:00"),
                "stockopen": 21.3,
                "stockclose": 20.75,
                "stockhigh": 21.3,
                "stocklow": 20.7,
                "stockprice": 20.75,
                "stockvolume": 255,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-17T00:00:00"),
                "stockopen": 20.8,
                "stockclose": 20.9,
                "stockhigh": 21.15,
                "stocklow": 20.6,
                "stockprice": 20.9,
                "stockvolume": 636,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-16T00:00:00"),
                "stockopen": 21.0,
                "stockclose": 20.5,
                "stockhigh": 21.2,
                "stocklow": 20.5,
                "stockprice": 20.5,
                "stockvolume": 450,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-15T00:00:00"),
                "stockopen": 20.65,
                "stockclose": 21.0,
                "stockhigh": 21.3,
                "stocklow": 20.55,
                "stockprice": 21.0,
                "stockvolume": 1017,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-12T00:00:00"),
                "stockopen": 19.9,
                "stockclose": 20.7,
                "stockhigh": 20.7,
                "stocklow": 19.8,
                "stockprice": 20.7,
                "stockvolume": 657,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-11T00:00:00"),
                "stockopen": 20.25,
                "stockclose": 19.95,
                "stockhigh": 20.45,
                "stocklow": 19.95,
                "stockprice": 19.95,
                "stockvolume": 369,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-10T00:00:00"),
                "stockopen": 20.3,
                "stockclose": 20.2,
                "stockhigh": 20.4,
                "stocklow": 20.0,
                "stockprice": 20.2,
                "stockvolume": 287,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-09T00:00:00"),
                "stockopen": 20.2,
                "stockclose": 20.3,
                "stockhigh": 20.5,
                "stocklow": 20.2,
                "stockprice": 20.3,
                "stockvolume": 206,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-05T00:00:00"),
                "stockopen": 20.4,
                "stockclose": 20.1,
                "stockhigh": 20.4,
                "stocklow": 20.1,
                "stockprice": 20.1,
                "stockvolume": 227,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-04T00:00:00"),
                "stockopen": 20.25,
                "stockclose": 20.2,
                "stockhigh": 20.5,
                "stocklow": 20.2,
                "stockprice": 20.2,
                "stockvolume": 309,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-03T00:00:00"),
                "stockopen": 20.35,
                "stockclose": 20.25,
                "stockhigh": 20.6,
                "stocklow": 20.2,
                "stockprice": 20.25,
                "stockvolume": 294,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-02T00:00:00"),
                "stockopen": 20.5,
                "stockclose": 20.25,
                "stockhigh": 20.5,
                "stocklow": 20.25,
                "stockprice": 20.25,
                "stockvolume": 366,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-01T00:00:00"),
                "stockopen": 20.65,
                "stockclose": 20.55,
                "stockhigh": 20.8,
                "stocklow": 20.45,
                "stockprice": 20.55,
                "stockvolume": 326,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-29T00:00:00"),
                "stockopen": 20.4,
                "stockclose": 20.65,
                "stockhigh": 20.7,
                "stocklow": 20.3,
                "stockprice": 20.65,
                "stockvolume": 611,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-28T00:00:00"),
                "stockopen": 20.2,
                "stockclose": 20.5,
                "stockhigh": 20.5,
                "stocklow": 20.2,
                "stockprice": 20.5,
                "stockvolume": 462,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-27T00:00:00"),
                "stockopen": 20.15,
                "stockclose": 20.2,
                "stockhigh": 20.45,
                "stocklow": 20.1,
                "stockprice": 20.2,
                "stockvolume": 457,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-26T00:00:00"),
                "stockopen": 20.4,
                "stockclose": 20.05,
                "stockhigh": 20.6,
                "stocklow": 20.05,
                "stockprice": 20.05,
                "stockvolume": 685,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-25T00:00:00"),
                "stockopen": 19.25,
                "stockclose": 20.45,
                "stockhigh": 20.55,
                "stocklow": 19.25,
                "stockprice": 20.45,
                "stockvolume": 829,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-22T00:00:00"),
                "stockopen": 19.0,
                "stockclose": 19.4,
                "stockhigh": 19.6,
                "stocklow": 19.0,
                "stockprice": 19.4,
                "stockvolume": 524,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-21T00:00:00"),
                "stockopen": 19.25,
                "stockclose": 19.05,
                "stockhigh": 19.45,
                "stocklow": 19.0,
                "stockprice": 19.05,
                "stockvolume": 448,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-20T00:00:00"),
                "stockopen": 19.65,
                "stockclose": 19.2,
                "stockhigh": 19.75,
                "stocklow": 19.1,
                "stockprice": 19.2,
                "stockvolume": 428,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-19T00:00:00"),
                "stockopen": 19.35,
                "stockclose": 19.45,
                "stockhigh": 19.6,
                "stocklow": 19.35,
                "stockprice": 19.45,
                "stockvolume": 327,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-18T00:00:00"),
                "stockopen": 19.9,
                "stockclose": 19.3,
                "stockhigh": 19.9,
                "stocklow": 19.1,
                "stockprice": 19.3,
                "stockvolume": 759,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-15T00:00:00"),
                "stockopen": 20.5,
                "stockclose": 19.9,
                "stockhigh": 20.5,
                "stocklow": 19.5,
                "stockprice": 19.9,
                "stockvolume": 851,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-14T00:00:00"),
                "stockopen": 20.5,
                "stockclose": 20.4,
                "stockhigh": 20.8,
                "stocklow": 20.25,
                "stockprice": 20.4,
                "stockvolume": 438,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-13T00:00:00"),
                "stockopen": 20.55,
                "stockclose": 20.6,
                "stockhigh": 20.7,
                "stocklow": 20.45,
                "stockprice": 20.6,
                "stockvolume": 246,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-12T00:00:00"),
                "stockopen": 20.8,
                "stockclose": 20.55,
                "stockhigh": 20.8,
                "stocklow": 20.55,
                "stockprice": 20.55,
                "stockvolume": 259,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-11T00:00:00"),
                "stockopen": 20.6,
                "stockclose": 20.6,
                "stockhigh": 20.75,
                "stocklow": 20.45,
                "stockprice": 20.6,
                "stockvolume": 342,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-08T00:00:00"),
                "stockopen": 20.75,
                "stockclose": 20.4,
                "stockhigh": 20.75,
                "stocklow": 20.15,
                "stockprice": 20.4,
                "stockvolume": 820,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-07T00:00:00"),
                "stockopen": 20.7,
                "stockclose": 20.85,
                "stockhigh": 21.1,
                "stocklow": 20.5,
                "stockprice": 20.85,
                "stockvolume": 696,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-06T00:00:00"),
                "stockopen": 21.7,
                "stockclose": 20.8,
                "stockhigh": 22.1,
                "stocklow": 20.5,
                "stockprice": 20.8,
                "stockvolume": 1304,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-05T00:00:00"),
                "stockopen": 22.25,
                "stockclose": 21.7,
                "stockhigh": 22.25,
                "stocklow": 21.65,
                "stockprice": 21.7,
                "stockvolume": 961,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-04T00:00:00"),
                "stockopen": 22.45,
                "stockclose": 22.25,
                "stockhigh": 22.7,
                "stocklow": 22.25,
                "stockprice": 22.25,
                "stockvolume": 590,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-01T00:00:00"),
                "stockopen": 22.5,
                "stockclose": 22.5,
                "stockhigh": 22.6,
                "stocklow": 22.3,
                "stockprice": 22.5,
                "stockvolume": 621,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-31T00:00:00"),
                "stockopen": 22.55,
                "stockclose": 22.65,
                "stockhigh": 22.95,
                "stocklow": 22.5,
                "stockprice": 22.65,
                "stockvolume": 718,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-30T00:00:00"),
                "stockopen": 22.6,
                "stockclose": 22.5,
                "stockhigh": 22.7,
                "stocklow": 22.4,
                "stockprice": 22.5,
                "stockvolume": 469,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-29T00:00:00"),
                "stockopen": 23.1,
                "stockclose": 22.35,
                "stockhigh": 23.1,
                "stocklow": 22.2,
                "stockprice": 22.35,
                "stockvolume": 1043,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-28T00:00:00"),
                "stockopen": 22.7,
                "stockclose": 22.55,
                "stockhigh": 22.85,
                "stocklow": 22.55,
                "stockprice": 22.55,
                "stockvolume": 584,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-25T00:00:00"),
                "stockopen": 23.0,
                "stockclose": 22.7,
                "stockhigh": 23.1,
                "stocklow": 22.7,
                "stockprice": 22.7,
                "stockvolume": 788,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-24T00:00:00"),
                "stockopen": 23.2,
                "stockclose": 22.95,
                "stockhigh": 23.3,
                "stocklow": 22.9,
                "stockprice": 22.95,
                "stockvolume": 582,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-22T00:00:00"),
                "stockopen": 23.0,
                "stockclose": 23.2,
                "stockhigh": 23.3,
                "stocklow": 22.8,
                "stockprice": 23.2,
                "stockvolume": 727,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-21T00:00:00"),
                "stockopen": 22.85,
                "stockclose": 22.95,
                "stockhigh": 23.3,
                "stocklow": 22.85,
                "stockprice": 22.95,
                "stockvolume": 490,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-18T00:00:00"),
                "stockopen": 22.7,
                "stockclose": 22.85,
                "stockhigh": 22.95,
                "stocklow": 22.65,
                "stockprice": 22.85,
                "stockvolume": 449,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-17T00:00:00"),
                "stockopen": 22.7,
                "stockclose": 22.75,
                "stockhigh": 23.15,
                "stocklow": 22.7,
                "stockprice": 22.75,
                "stockvolume": 938,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-16T00:00:00"),
                "stockopen": 22.8,
                "stockclose": 22.65,
                "stockhigh": 22.95,
                "stocklow": 22.6,
                "stockprice": 22.65,
                "stockvolume": 813,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-15T00:00:00"),
                "stockopen": 23.1,
                "stockclose": 22.95,
                "stockhigh": 23.2,
                "stocklow": 22.9,
                "stockprice": 22.95,
                "stockvolume": 660,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-14T00:00:00"),
                "stockopen": 23.3,
                "stockclose": 22.9,
                "stockhigh": 23.35,
                "stocklow": 22.9,
                "stockprice": 22.9,
                "stockvolume": 742,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-11T00:00:00"),
                "stockopen": 23.5,
                "stockclose": 22.8,
                "stockhigh": 23.65,
                "stocklow": 22.6,
                "stockprice": 22.8,
                "stockvolume": 1394,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-10T00:00:00"),
                "stockopen": 23.9,
                "stockclose": 23.65,
                "stockhigh": 24.2,
                "stocklow": 23.65,
                "stockprice": 23.65,
                "stockvolume": 1165,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
    
    // populate trader data as update
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 10.0;
                result[0].traderbuyvolume = 0;
                result[0].tradersellvolume = 157;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "1520-瑞士信貸",
            "stockidnm": "2388-威盛",
            "tradervolume": "157",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 11.0;
                result[0].traderbuyvolume = 270;
                result[0].tradersellvolume = 3;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "585L-統一豐原",
            "stockidnm": "2388-威盛",
            "tradervolume": "273",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 11.0;
                result[0].traderbuyvolume = 0;
                result[0].tradersellvolume = 130;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "700G-兆豐麻豆",
            "stockidnm": "2388-威盛",
            "tradervolume": "130",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 11.0;
                result[0].traderbuyvolume = 78;
                result[0].tradersellvolume = 216;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "8440-摩根大通",
            "stockidnm": "2388-威盛",
            "tradervolume": "294",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 10.0;
                result[0].traderbuyvolume = 100;
                result[0].tradersellvolume = 0;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "8770-大鼎",
            "stockidnm": "2388-威盛",
            "tradervolume": "100",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 11.0;
                result[0].traderbuyvolume = 149;
                result[0].tradersellvolume = 1;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "9138-群益中港",
            "stockidnm": "2388-威盛",
            "tradervolume": "150",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 11.0;
                result[0].traderbuyvolume = 445;
                result[0].tradersellvolume = 0;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "9215-凱基三民",
            "stockidnm": "2388-威盛",
            "tradervolume": "445",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 10.0;
                result[0].traderbuyvolume = 100;
                result[0].tradersellvolume = 1;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "9332-華南楠梓",
            "stockidnm": "2388-威盛",
            "tradervolume": "101",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 11.0;
                result[0].traderbuyvolume = 150;
                result[0].tradersellvolume = 2;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "9608-富邦台東",
            "stockidnm": "2388-威盛",
            "tradervolume": "152",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 11.0;
                result[0].traderbuyvolume = 150;
                result[0].tradersellvolume = 2;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "9867-元大北成",
            "stockidnm": "2388-威盛",
            "tradervolume": "152",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
}

function checkChartData(){
    // check created data is ok

}

function generateCollectiveData(){
// aggregate collective data
for (var x in chartData) {
    var dataPoint = chartData[x];
    if ( 0 == x ) {
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
    }
    else {
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
}

function createPieChart(){
// create pie chart
    pieChart = AmCharts.makeChart("chartdiv1", {
    "type": "pie",
    "dataProvider": chartData,
    "valueField": "tradervolume",
    "titleField": "traderidnm",
    "labelText": "[[title]]: [[value]]",
     "legend": {
        "markerType": "circle",
        "position": "right",
        "marginRight": 80, 
        "autoMargins": false
    },
    "pullOutOnlyOne": true
});
}

function createColumnChart(){
// create column chart
    stockChart = AmCharts.makeChart("chartdiv2", {
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
        "title": "traderprice",
        "fillAlphas": 0,
        "valueField": "traderprice",
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
}

function callbackPieChart(){
    pieChart.addListener("pullOutSlice", function (event) {
    stockChart.dataProvider = event.dataItem.dataContext.data;
    stockChart.validateData();
    stockChart.animateAgain();
});

    pieChart.addListener("pullInSlice", function (event) {
    stockChart.dataProvider = collectiveData;
    stockChart.validateData();
    stockChart.animateAgain();
});
}

}//]]>  

