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
                "date": new Date("2014-11-27T00:00:00"),
                "stockopen": 9.01,
                "stockclose": 8.99,
                "stockhigh": 9.07,
                "stocklow": 8.96,
                "stockprice": 8.99,
                "stockvolume": 7563,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-26T00:00:00"),
                "stockopen": 9.1,
                "stockclose": 9.0,
                "stockhigh": 9.17,
                "stocklow": 9.0,
                "stockprice": 9.0,
                "stockvolume": 8111,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-25T00:00:00"),
                "stockopen": 9.19,
                "stockclose": 9.1,
                "stockhigh": 9.25,
                "stocklow": 9.1,
                "stockprice": 9.1,
                "stockvolume": 5874,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-24T00:00:00"),
                "stockopen": 9.1,
                "stockclose": 9.19,
                "stockhigh": 9.36,
                "stocklow": 9.1,
                "stockprice": 9.19,
                "stockvolume": 9962,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-21T00:00:00"),
                "stockopen": 9.29,
                "stockclose": 9.1,
                "stockhigh": 9.29,
                "stocklow": 9.1,
                "stockprice": 9.1,
                "stockvolume": 5504,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-20T00:00:00"),
                "stockopen": 9.0,
                "stockclose": 9.22,
                "stockhigh": 9.33,
                "stocklow": 8.97,
                "stockprice": 9.22,
                "stockvolume": 14127,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-19T00:00:00"),
                "stockopen": 8.92,
                "stockclose": 8.95,
                "stockhigh": 9.05,
                "stocklow": 8.9,
                "stockprice": 8.95,
                "stockvolume": 4696,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-18T00:00:00"),
                "stockopen": 9.0,
                "stockclose": 8.88,
                "stockhigh": 9.05,
                "stocklow": 8.86,
                "stockprice": 8.88,
                "stockvolume": 5323,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-17T00:00:00"),
                "stockopen": 9.11,
                "stockclose": 8.96,
                "stockhigh": 9.11,
                "stocklow": 8.96,
                "stockprice": 8.96,
                "stockvolume": 5499,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-14T00:00:00"),
                "stockopen": 9.02,
                "stockclose": 9.07,
                "stockhigh": 9.09,
                "stocklow": 9.01,
                "stockprice": 9.07,
                "stockvolume": 5666,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-13T00:00:00"),
                "stockopen": 9.06,
                "stockclose": 9.03,
                "stockhigh": 9.15,
                "stocklow": 9.01,
                "stockprice": 9.03,
                "stockvolume": 4957,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-12T00:00:00"),
                "stockopen": 9.1,
                "stockclose": 9.05,
                "stockhigh": 9.19,
                "stocklow": 9.03,
                "stockprice": 9.05,
                "stockvolume": 8945,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-11T00:00:00"),
                "stockopen": 9.5,
                "stockclose": 9.24,
                "stockhigh": 9.5,
                "stocklow": 9.24,
                "stockprice": 9.24,
                "stockvolume": 9103,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-10T00:00:00"),
                "stockopen": 9.35,
                "stockclose": 9.5,
                "stockhigh": 9.61,
                "stocklow": 9.3,
                "stockprice": 9.5,
                "stockvolume": 11378,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-07T00:00:00"),
                "stockopen": 9.27,
                "stockclose": 9.3,
                "stockhigh": 9.33,
                "stocklow": 9.22,
                "stockprice": 9.3,
                "stockvolume": 4537,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-06T00:00:00"),
                "stockopen": 9.41,
                "stockclose": 9.26,
                "stockhigh": 9.49,
                "stocklow": 9.25,
                "stockprice": 9.26,
                "stockvolume": 6997,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-05T00:00:00"),
                "stockopen": 9.55,
                "stockclose": 9.41,
                "stockhigh": 9.6,
                "stocklow": 9.41,
                "stockprice": 9.41,
                "stockvolume": 7522,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-04T00:00:00"),
                "stockopen": 9.76,
                "stockclose": 9.51,
                "stockhigh": 9.76,
                "stocklow": 9.5,
                "stockprice": 9.51,
                "stockvolume": 9547,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-03T00:00:00"),
                "stockopen": 9.7,
                "stockclose": 9.71,
                "stockhigh": 9.86,
                "stocklow": 9.6,
                "stockprice": 9.71,
                "stockvolume": 17806,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-31T00:00:00"),
                "stockopen": 9.15,
                "stockclose": 9.6,
                "stockhigh": 9.6,
                "stocklow": 9.13,
                "stockprice": 9.6,
                "stockvolume": 23341,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-30T00:00:00"),
                "stockopen": 9.05,
                "stockclose": 9.1,
                "stockhigh": 9.11,
                "stocklow": 9.0,
                "stockprice": 9.1,
                "stockvolume": 5647,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-29T00:00:00"),
                "stockopen": 8.98,
                "stockclose": 9.0,
                "stockhigh": 9.05,
                "stocklow": 8.94,
                "stockprice": 9.0,
                "stockvolume": 6881,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-28T00:00:00"),
                "stockopen": 8.99,
                "stockclose": 8.94,
                "stockhigh": 8.99,
                "stocklow": 8.9,
                "stockprice": 8.94,
                "stockvolume": 4036,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-27T00:00:00"),
                "stockopen": 8.93,
                "stockclose": 8.86,
                "stockhigh": 9.05,
                "stocklow": 8.86,
                "stockprice": 8.86,
                "stockvolume": 5507,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-24T00:00:00"),
                "stockopen": 8.88,
                "stockclose": 8.88,
                "stockhigh": 8.9,
                "stocklow": 8.7,
                "stockprice": 8.88,
                "stockvolume": 7253,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-23T00:00:00"),
                "stockopen": 9.0,
                "stockclose": 8.87,
                "stockhigh": 9.0,
                "stocklow": 8.86,
                "stockprice": 8.87,
                "stockvolume": 4190,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-22T00:00:00"),
                "stockopen": 9.06,
                "stockclose": 9.01,
                "stockhigh": 9.07,
                "stocklow": 8.97,
                "stockprice": 9.01,
                "stockvolume": 6898,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-21T00:00:00"),
                "stockopen": 9.09,
                "stockclose": 8.96,
                "stockhigh": 9.09,
                "stocklow": 8.96,
                "stockprice": 8.96,
                "stockvolume": 6001,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-20T00:00:00"),
                "stockopen": 9.14,
                "stockclose": 9.09,
                "stockhigh": 9.2,
                "stocklow": 9.01,
                "stockprice": 9.09,
                "stockvolume": 8681,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-17T00:00:00"),
                "stockopen": 9.18,
                "stockclose": 8.94,
                "stockhigh": 9.2,
                "stocklow": 8.9,
                "stockprice": 8.94,
                "stockvolume": 11083,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-16T00:00:00"),
                "stockopen": 8.54,
                "stockclose": 8.93,
                "stockhigh": 8.94,
                "stocklow": 8.54,
                "stockprice": 8.93,
                "stockvolume": 21865,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-15T00:00:00"),
                "stockopen": 9.06,
                "stockclose": 8.54,
                "stockhigh": 9.06,
                "stocklow": 8.48,
                "stockprice": 8.54,
                "stockvolume": 22385,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-14T00:00:00"),
                "stockopen": 8.8,
                "stockclose": 9.06,
                "stockhigh": 9.12,
                "stocklow": 8.8,
                "stockprice": 9.06,
                "stockvolume": 13984,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-13T00:00:00"),
                "stockopen": 9.4,
                "stockclose": 9.03,
                "stockhigh": 9.4,
                "stocklow": 9.0,
                "stockprice": 9.03,
                "stockvolume": 15025,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-09T00:00:00"),
                "stockopen": 9.9,
                "stockclose": 9.61,
                "stockhigh": 9.9,
                "stocklow": 9.61,
                "stockprice": 9.61,
                "stockvolume": 6267,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-08T00:00:00"),
                "stockopen": 9.65,
                "stockclose": 9.72,
                "stockhigh": 9.8,
                "stocklow": 9.61,
                "stockprice": 9.72,
                "stockvolume": 6117,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-07T00:00:00"),
                "stockopen": 9.95,
                "stockclose": 9.81,
                "stockhigh": 9.96,
                "stocklow": 9.8,
                "stockprice": 9.81,
                "stockvolume": 5011,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-06T00:00:00"),
                "stockopen": 10.05,
                "stockclose": 9.97,
                "stockhigh": 10.2,
                "stocklow": 9.97,
                "stockprice": 9.97,
                "stockvolume": 6788,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-03T00:00:00"),
                "stockopen": 9.94,
                "stockclose": 10.0,
                "stockhigh": 10.05,
                "stocklow": 9.94,
                "stockprice": 10.0,
                "stockvolume": 6624,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-02T00:00:00"),
                "stockopen": 9.75,
                "stockclose": 9.94,
                "stockhigh": 9.95,
                "stocklow": 9.73,
                "stockprice": 9.94,
                "stockvolume": 8425,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-01T00:00:00"),
                "stockopen": 9.52,
                "stockclose": 9.75,
                "stockhigh": 9.8,
                "stocklow": 9.52,
                "stockprice": 9.75,
                "stockvolume": 8976,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-30T00:00:00"),
                "stockopen": 10.05,
                "stockclose": 9.52,
                "stockhigh": 10.1,
                "stocklow": 9.3,
                "stockprice": 9.52,
                "stockvolume": 22226,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-29T00:00:00"),
                "stockopen": 9.97,
                "stockclose": 9.99,
                "stockhigh": 10.05,
                "stocklow": 9.97,
                "stockprice": 9.99,
                "stockvolume": 8082,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-26T00:00:00"),
                "stockopen": 10.2,
                "stockclose": 9.96,
                "stockhigh": 10.25,
                "stocklow": 9.94,
                "stockprice": 9.96,
                "stockvolume": 20017,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-25T00:00:00"),
                "stockopen": 10.45,
                "stockclose": 10.25,
                "stockhigh": 10.5,
                "stocklow": 10.2,
                "stockprice": 10.25,
                "stockvolume": 9580,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-24T00:00:00"),
                "stockopen": 10.5,
                "stockclose": 10.4,
                "stockhigh": 10.5,
                "stocklow": 10.35,
                "stockprice": 10.4,
                "stockvolume": 5334,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-23T00:00:00"),
                "stockopen": 10.45,
                "stockclose": 10.45,
                "stockhigh": 10.5,
                "stocklow": 10.4,
                "stockprice": 10.45,
                "stockvolume": 4121,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-22T00:00:00"),
                "stockopen": 10.55,
                "stockclose": 10.4,
                "stockhigh": 10.65,
                "stocklow": 10.4,
                "stockprice": 10.4,
                "stockvolume": 8049,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-19T00:00:00"),
                "stockopen": 10.4,
                "stockclose": 10.5,
                "stockhigh": 10.6,
                "stocklow": 10.4,
                "stockprice": 10.5,
                "stockvolume": 11048,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-18T00:00:00"),
                "stockopen": 10.45,
                "stockclose": 10.35,
                "stockhigh": 10.5,
                "stocklow": 10.35,
                "stockprice": 10.35,
                "stockvolume": 7496,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-17T00:00:00"),
                "stockopen": 10.45,
                "stockclose": 10.35,
                "stockhigh": 10.55,
                "stocklow": 10.35,
                "stockprice": 10.35,
                "stockvolume": 11389,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-16T00:00:00"),
                "stockopen": 10.55,
                "stockclose": 10.45,
                "stockhigh": 10.6,
                "stocklow": 10.4,
                "stockprice": 10.45,
                "stockvolume": 8187,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-15T00:00:00"),
                "stockopen": 10.65,
                "stockclose": 10.55,
                "stockhigh": 10.65,
                "stocklow": 10.5,
                "stockprice": 10.55,
                "stockvolume": 7085,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-12T00:00:00"),
                "stockopen": 10.6,
                "stockclose": 10.65,
                "stockhigh": 10.7,
                "stocklow": 10.55,
                "stockprice": 10.65,
                "stockvolume": 7947,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-11T00:00:00"),
                "stockopen": 10.75,
                "stockclose": 10.6,
                "stockhigh": 10.85,
                "stocklow": 10.6,
                "stockprice": 10.6,
                "stockvolume": 12862,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-10T00:00:00"),
                "stockopen": 10.5,
                "stockclose": 10.7,
                "stockhigh": 10.95,
                "stocklow": 10.5,
                "stockprice": 10.7,
                "stockvolume": 24333,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-09T00:00:00"),
                "stockopen": 10.55,
                "stockclose": 10.5,
                "stockhigh": 10.65,
                "stocklow": 10.5,
                "stockprice": 10.5,
                "stockvolume": 3943,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-05T00:00:00"),
                "stockopen": 10.65,
                "stockclose": 10.5,
                "stockhigh": 10.65,
                "stocklow": 10.5,
                "stockprice": 10.5,
                "stockvolume": 5378,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-04T00:00:00"),
                "stockopen": 10.6,
                "stockclose": 10.6,
                "stockhigh": 10.65,
                "stocklow": 10.55,
                "stockprice": 10.6,
                "stockvolume": 5538,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-03T00:00:00"),
                "stockopen": 10.65,
                "stockclose": 10.55,
                "stockhigh": 10.7,
                "stocklow": 10.55,
                "stockprice": 10.55,
                "stockvolume": 6468,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-02T00:00:00"),
                "stockopen": 10.6,
                "stockclose": 10.55,
                "stockhigh": 10.65,
                "stocklow": 10.55,
                "stockprice": 10.55,
                "stockvolume": 7366,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-01T00:00:00"),
                "stockopen": 10.7,
                "stockclose": 10.55,
                "stockhigh": 10.7,
                "stocklow": 10.5,
                "stockprice": 10.55,
                "stockvolume": 9449,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-29T00:00:00"),
                "stockopen": 10.65,
                "stockclose": 10.65,
                "stockhigh": 10.7,
                "stocklow": 10.55,
                "stockprice": 10.65,
                "stockvolume": 5335,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-28T00:00:00"),
                "stockopen": 10.7,
                "stockclose": 10.65,
                "stockhigh": 10.7,
                "stocklow": 10.6,
                "stockprice": 10.65,
                "stockvolume": 7213,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-27T00:00:00"),
                "stockopen": 10.75,
                "stockclose": 10.65,
                "stockhigh": 10.75,
                "stocklow": 10.6,
                "stockprice": 10.65,
                "stockvolume": 8590,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-26T00:00:00"),
                "stockopen": 10.6,
                "stockclose": 10.65,
                "stockhigh": 10.8,
                "stocklow": 10.55,
                "stockprice": 10.65,
                "stockvolume": 18688,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-25T00:00:00"),
                "stockopen": 10.55,
                "stockclose": 10.5,
                "stockhigh": 10.65,
                "stocklow": 10.5,
                "stockprice": 10.5,
                "stockvolume": 7899,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-22T00:00:00"),
                "stockopen": 10.55,
                "stockclose": 10.55,
                "stockhigh": 10.65,
                "stocklow": 10.45,
                "stockprice": 10.55,
                "stockvolume": 14106,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-21T00:00:00"),
                "stockopen": 10.35,
                "stockclose": 10.45,
                "stockhigh": 10.5,
                "stocklow": 10.35,
                "stockprice": 10.45,
                "stockvolume": 7493,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-20T00:00:00"),
                "stockopen": 10.55,
                "stockclose": 10.35,
                "stockhigh": 10.6,
                "stocklow": 10.35,
                "stockprice": 10.35,
                "stockvolume": 16447,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-19T00:00:00"),
                "stockopen": 10.6,
                "stockclose": 10.6,
                "stockhigh": 10.75,
                "stocklow": 10.6,
                "stockprice": 10.6,
                "stockvolume": 9469,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-18T00:00:00"),
                "stockopen": 10.6,
                "stockclose": 10.6,
                "stockhigh": 10.8,
                "stocklow": 10.6,
                "stockprice": 10.6,
                "stockvolume": 14740,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-15T00:00:00"),
                "stockopen": 10.6,
                "stockclose": 10.55,
                "stockhigh": 10.65,
                "stocklow": 10.5,
                "stockprice": 10.55,
                "stockvolume": 11724,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-14T00:00:00"),
                "stockopen": 10.75,
                "stockclose": 10.6,
                "stockhigh": 10.8,
                "stocklow": 10.6,
                "stockprice": 10.6,
                "stockvolume": 11728,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-13T00:00:00"),
                "stockopen": 10.65,
                "stockclose": 10.7,
                "stockhigh": 10.9,
                "stocklow": 10.65,
                "stockprice": 10.7,
                "stockvolume": 21122,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-12T00:00:00"),
                "stockopen": 10.85,
                "stockclose": 10.6,
                "stockhigh": 10.85,
                "stocklow": 10.6,
                "stockprice": 10.6,
                "stockvolume": 12684,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-11T00:00:00"),
                "stockopen": 10.95,
                "stockclose": 10.8,
                "stockhigh": 11.0,
                "stocklow": 10.8,
                "stockprice": 10.8,
                "stockvolume": 23559,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-08T00:00:00"),
                "stockopen": 10.6,
                "stockclose": 10.8,
                "stockhigh": 10.85,
                "stocklow": 10.4,
                "stockprice": 10.8,
                "stockvolume": 35300,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-07T00:00:00"),
                "stockopen": 10.25,
                "stockclose": 10.5,
                "stockhigh": 10.65,
                "stocklow": 10.25,
                "stockprice": 10.5,
                "stockvolume": 40019,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-06T00:00:00"),
                "stockopen": 10.9,
                "stockclose": 10.2,
                "stockhigh": 10.9,
                "stocklow": 10.2,
                "stockprice": 10.2,
                "stockvolume": 72364,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-05T00:00:00"),
                "stockopen": 10.35,
                "stockclose": 10.95,
                "stockhigh": 11.05,
                "stocklow": 10.35,
                "stockprice": 10.95,
                "stockvolume": 92179,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-04T00:00:00"),
                "stockopen": 10.95,
                "stockclose": 10.65,
                "stockhigh": 11.1,
                "stocklow": 10.65,
                "stockprice": 10.65,
                "stockvolume": 95453,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-01T00:00:00"),
                "stockopen": 11.4,
                "stockclose": 11.4,
                "stockhigh": 11.75,
                "stocklow": 11.4,
                "stockprice": 11.4,
                "stockvolume": 180540,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-31T00:00:00"),
                "stockopen": 12.5,
                "stockclose": 12.25,
                "stockhigh": 12.65,
                "stocklow": 12.2,
                "stockprice": 12.25,
                "stockvolume": 46570,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-30T00:00:00"),
                "stockopen": 11.95,
                "stockclose": 12.4,
                "stockhigh": 12.45,
                "stocklow": 11.9,
                "stockprice": 12.4,
                "stockvolume": 55517,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-29T00:00:00"),
                "stockopen": 12.1,
                "stockclose": 11.85,
                "stockhigh": 12.1,
                "stocklow": 11.85,
                "stockprice": 11.85,
                "stockvolume": 16851,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-28T00:00:00"),
                "stockopen": 11.9,
                "stockclose": 12.0,
                "stockhigh": 12.1,
                "stocklow": 11.8,
                "stockprice": 12.0,
                "stockvolume": 18950,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-25T00:00:00"),
                "stockopen": 11.85,
                "stockclose": 11.85,
                "stockhigh": 11.9,
                "stocklow": 11.75,
                "stockprice": 11.85,
                "stockvolume": 12200,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-24T00:00:00"),
                "stockopen": 11.95,
                "stockclose": 11.8,
                "stockhigh": 12.0,
                "stocklow": 11.8,
                "stockprice": 11.8,
                "stockvolume": 11730,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-22T00:00:00"),
                "stockopen": 11.9,
                "stockclose": 11.9,
                "stockhigh": 11.95,
                "stocklow": 11.8,
                "stockprice": 11.9,
                "stockvolume": 7054,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-21T00:00:00"),
                "stockopen": 12.0,
                "stockclose": 11.85,
                "stockhigh": 12.05,
                "stocklow": 11.85,
                "stockprice": 11.85,
                "stockvolume": 10492,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-18T00:00:00"),
                "stockopen": 11.9,
                "stockclose": 11.95,
                "stockhigh": 12.15,
                "stocklow": 11.9,
                "stockprice": 11.95,
                "stockvolume": 18342,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-17T00:00:00"),
                "stockopen": 11.8,
                "stockclose": 11.85,
                "stockhigh": 11.95,
                "stocklow": 11.8,
                "stockprice": 11.85,
                "stockvolume": 8421,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-16T00:00:00"),
                "stockopen": 12.0,
                "stockclose": 11.8,
                "stockhigh": 12.1,
                "stocklow": 11.8,
                "stockprice": 11.8,
                "stockvolume": 16302,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-15T00:00:00"),
                "stockopen": 11.95,
                "stockclose": 12.0,
                "stockhigh": 12.1,
                "stocklow": 11.85,
                "stockprice": 12.0,
                "stockvolume": 23863,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-14T00:00:00"),
                "stockopen": 11.8,
                "stockclose": 11.8,
                "stockhigh": 12.0,
                "stocklow": 11.8,
                "stockprice": 11.8,
                "stockvolume": 11629,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-11T00:00:00"),
                "stockopen": 11.9,
                "stockclose": 11.8,
                "stockhigh": 12.1,
                "stocklow": 11.8,
                "stockprice": 11.8,
                "stockvolume": 19258,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-10T00:00:00"),
                "stockopen": 12.0,
                "stockclose": 11.9,
                "stockhigh": 12.1,
                "stocklow": 11.9,
                "stockprice": 11.9,
                "stockvolume": 15292,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
    
    // populate trader data as update
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 9.0;
                result[0].traderbuyvolume = 284;
                result[0].tradersellvolume = 2010;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "1520-瑞士信貸",
            "stockidnm": "1314-中石化",
            "tradervolume": "2294",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 9.0;
                result[0].traderbuyvolume = 321;
                result[0].tradersellvolume = 39;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "8843-None",
            "stockidnm": "1314-中石化",
            "tradervolume": "360",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 9.0;
                result[0].traderbuyvolume = 0;
                result[0].tradersellvolume = 1220;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "9800-None",
            "stockidnm": "1314-中石化",
            "tradervolume": "1220",
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

