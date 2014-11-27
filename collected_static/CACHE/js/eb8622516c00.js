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
                "stockopen": 45.8,
                "stockclose": 45.3,
                "stockhigh": 45.8,
                "stocklow": 45.3,
                "stockprice": 45.3,
                "stockvolume": 5327,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-25T00:00:00"),
                "stockopen": 46.15,
                "stockclose": 45.5,
                "stockhigh": 46.2,
                "stocklow": 45.5,
                "stockprice": 45.5,
                "stockvolume": 5408,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-24T00:00:00"),
                "stockopen": 45.6,
                "stockclose": 46.15,
                "stockhigh": 46.4,
                "stocklow": 45.55,
                "stockprice": 46.15,
                "stockvolume": 8462,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-21T00:00:00"),
                "stockopen": 45.95,
                "stockclose": 45.3,
                "stockhigh": 46.0,
                "stocklow": 45.25,
                "stockprice": 45.3,
                "stockvolume": 8145,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-20T00:00:00"),
                "stockopen": 45.4,
                "stockclose": 46.0,
                "stockhigh": 46.05,
                "stocklow": 45.05,
                "stockprice": 46.0,
                "stockvolume": 5258,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-19T00:00:00"),
                "stockopen": 45.5,
                "stockclose": 44.8,
                "stockhigh": 45.6,
                "stocklow": 44.8,
                "stockprice": 44.8,
                "stockvolume": 10007,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-18T00:00:00"),
                "stockopen": 44.6,
                "stockclose": 44.95,
                "stockhigh": 45.2,
                "stocklow": 44.5,
                "stockprice": 44.95,
                "stockvolume": 8446,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-17T00:00:00"),
                "stockopen": 45.4,
                "stockclose": 44.6,
                "stockhigh": 45.4,
                "stocklow": 44.4,
                "stockprice": 44.6,
                "stockvolume": 5596,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-14T00:00:00"),
                "stockopen": 45.5,
                "stockclose": 45.0,
                "stockhigh": 45.5,
                "stocklow": 45.0,
                "stockprice": 45.0,
                "stockvolume": 7020,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-13T00:00:00"),
                "stockopen": 45.7,
                "stockclose": 45.65,
                "stockhigh": 45.7,
                "stocklow": 45.4,
                "stockprice": 45.65,
                "stockvolume": 4101,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-12T00:00:00"),
                "stockopen": 45.4,
                "stockclose": 45.65,
                "stockhigh": 45.9,
                "stocklow": 45.4,
                "stockprice": 45.65,
                "stockvolume": 6571,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-11T00:00:00"),
                "stockopen": 46.6,
                "stockclose": 45.95,
                "stockhigh": 46.85,
                "stocklow": 45.95,
                "stockprice": 45.95,
                "stockvolume": 6021,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-10T00:00:00"),
                "stockopen": 45.6,
                "stockclose": 46.2,
                "stockhigh": 46.65,
                "stocklow": 45.55,
                "stockprice": 46.2,
                "stockvolume": 5583,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-07T00:00:00"),
                "stockopen": 46.05,
                "stockclose": 45.65,
                "stockhigh": 46.3,
                "stocklow": 45.6,
                "stockprice": 45.65,
                "stockvolume": 6423,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-06T00:00:00"),
                "stockopen": 46.4,
                "stockclose": 46.05,
                "stockhigh": 46.65,
                "stocklow": 46.0,
                "stockprice": 46.05,
                "stockvolume": 4266,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-05T00:00:00"),
                "stockopen": 46.65,
                "stockclose": 46.3,
                "stockhigh": 46.65,
                "stocklow": 46.1,
                "stockprice": 46.3,
                "stockvolume": 3456,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-04T00:00:00"),
                "stockopen": 46.95,
                "stockclose": 46.3,
                "stockhigh": 47.2,
                "stocklow": 46.3,
                "stockprice": 46.3,
                "stockvolume": 3989,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-03T00:00:00"),
                "stockopen": 46.9,
                "stockclose": 46.8,
                "stockhigh": 46.95,
                "stocklow": 46.3,
                "stockprice": 46.8,
                "stockvolume": 2826,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-31T00:00:00"),
                "stockopen": 46.6,
                "stockclose": 46.45,
                "stockhigh": 46.9,
                "stocklow": 46.1,
                "stockprice": 46.45,
                "stockvolume": 3737,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-30T00:00:00"),
                "stockopen": 46.55,
                "stockclose": 46.45,
                "stockhigh": 46.65,
                "stocklow": 46.2,
                "stockprice": 46.45,
                "stockvolume": 5094,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-29T00:00:00"),
                "stockopen": 47.2,
                "stockclose": 46.75,
                "stockhigh": 47.2,
                "stocklow": 46.2,
                "stockprice": 46.75,
                "stockvolume": 4864,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-28T00:00:00"),
                "stockopen": 46.2,
                "stockclose": 47.1,
                "stockhigh": 47.25,
                "stocklow": 46.2,
                "stockprice": 47.1,
                "stockvolume": 7571,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-27T00:00:00"),
                "stockopen": 45.9,
                "stockclose": 45.85,
                "stockhigh": 46.0,
                "stocklow": 45.7,
                "stockprice": 45.85,
                "stockvolume": 2728,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-24T00:00:00"),
                "stockopen": 46.0,
                "stockclose": 45.75,
                "stockhigh": 46.05,
                "stocklow": 45.5,
                "stockprice": 45.75,
                "stockvolume": 2492,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-23T00:00:00"),
                "stockopen": 45.55,
                "stockclose": 45.75,
                "stockhigh": 45.85,
                "stocklow": 45.5,
                "stockprice": 45.75,
                "stockvolume": 2951,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-22T00:00:00"),
                "stockopen": 45.8,
                "stockclose": 45.55,
                "stockhigh": 45.95,
                "stocklow": 45.5,
                "stockprice": 45.55,
                "stockvolume": 4032,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-21T00:00:00"),
                "stockopen": 45.8,
                "stockclose": 45.4,
                "stockhigh": 45.9,
                "stocklow": 45.4,
                "stockprice": 45.4,
                "stockvolume": 2765,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-20T00:00:00"),
                "stockopen": 45.55,
                "stockclose": 45.55,
                "stockhigh": 45.95,
                "stocklow": 45.5,
                "stockprice": 45.55,
                "stockvolume": 1821,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-17T00:00:00"),
                "stockopen": 45.7,
                "stockclose": 45.25,
                "stockhigh": 45.7,
                "stocklow": 45.0,
                "stockprice": 45.25,
                "stockvolume": 8128,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-16T00:00:00"),
                "stockopen": 45.5,
                "stockclose": 45.5,
                "stockhigh": 45.95,
                "stocklow": 45.0,
                "stockprice": 45.5,
                "stockvolume": 5632,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-15T00:00:00"),
                "stockopen": 45.35,
                "stockclose": 45.5,
                "stockhigh": 46.15,
                "stocklow": 44.6,
                "stockprice": 45.5,
                "stockvolume": 9272,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-14T00:00:00"),
                "stockopen": 44.8,
                "stockclose": 45.15,
                "stockhigh": 45.4,
                "stocklow": 44.8,
                "stockprice": 45.15,
                "stockvolume": 3348,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-13T00:00:00"),
                "stockopen": 45.0,
                "stockclose": 44.8,
                "stockhigh": 45.4,
                "stocklow": 44.8,
                "stockprice": 44.8,
                "stockvolume": 4828,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-09T00:00:00"),
                "stockopen": 45.5,
                "stockclose": 46.0,
                "stockhigh": 46.15,
                "stocklow": 45.4,
                "stockprice": 46.0,
                "stockvolume": 6783,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-08T00:00:00"),
                "stockopen": 44.75,
                "stockclose": 45.35,
                "stockhigh": 45.6,
                "stocklow": 44.5,
                "stockprice": 45.35,
                "stockvolume": 6417,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-07T00:00:00"),
                "stockopen": 44.8,
                "stockclose": 44.75,
                "stockhigh": 45.0,
                "stocklow": 44.35,
                "stockprice": 44.75,
                "stockvolume": 5823,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-06T00:00:00"),
                "stockopen": 45.25,
                "stockclose": 44.8,
                "stockhigh": 45.25,
                "stocklow": 44.5,
                "stockprice": 44.8,
                "stockvolume": 5088,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-03T00:00:00"),
                "stockopen": 44.8,
                "stockclose": 45.1,
                "stockhigh": 45.3,
                "stocklow": 44.4,
                "stockprice": 45.1,
                "stockvolume": 4027,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-02T00:00:00"),
                "stockopen": 44.55,
                "stockclose": 44.7,
                "stockhigh": 44.7,
                "stocklow": 44.1,
                "stockprice": 44.7,
                "stockvolume": 6821,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-01T00:00:00"),
                "stockopen": 45.5,
                "stockclose": 44.8,
                "stockhigh": 45.5,
                "stocklow": 44.7,
                "stockprice": 44.8,
                "stockvolume": 6935,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-30T00:00:00"),
                "stockopen": 45.1,
                "stockclose": 45.3,
                "stockhigh": 45.6,
                "stocklow": 44.8,
                "stockprice": 45.3,
                "stockvolume": 6356,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-29T00:00:00"),
                "stockopen": 45.8,
                "stockclose": 45.0,
                "stockhigh": 45.8,
                "stocklow": 44.95,
                "stockprice": 45.0,
                "stockvolume": 8710,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-26T00:00:00"),
                "stockopen": 45.4,
                "stockclose": 45.3,
                "stockhigh": 45.6,
                "stocklow": 45.1,
                "stockprice": 45.3,
                "stockvolume": 8267,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-25T00:00:00"),
                "stockopen": 47.0,
                "stockclose": 45.85,
                "stockhigh": 47.0,
                "stocklow": 45.6,
                "stockprice": 45.85,
                "stockvolume": 6367,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-24T00:00:00"),
                "stockopen": 45.45,
                "stockclose": 46.7,
                "stockhigh": 46.8,
                "stocklow": 45.35,
                "stockprice": 46.7,
                "stockvolume": 10221,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-23T00:00:00"),
                "stockopen": 45.95,
                "stockclose": 45.45,
                "stockhigh": 46.0,
                "stocklow": 45.45,
                "stockprice": 45.45,
                "stockvolume": 6296,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-22T00:00:00"),
                "stockopen": 46.8,
                "stockclose": 45.8,
                "stockhigh": 46.8,
                "stocklow": 45.6,
                "stockprice": 45.8,
                "stockvolume": 7691,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-19T00:00:00"),
                "stockopen": 46.9,
                "stockclose": 46.95,
                "stockhigh": 47.45,
                "stocklow": 46.5,
                "stockprice": 46.95,
                "stockvolume": 6958,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-18T00:00:00"),
                "stockopen": 47.5,
                "stockclose": 46.7,
                "stockhigh": 47.5,
                "stocklow": 46.65,
                "stockprice": 46.7,
                "stockvolume": 6052,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-17T00:00:00"),
                "stockopen": 47.0,
                "stockclose": 47.3,
                "stockhigh": 47.45,
                "stocklow": 46.8,
                "stockprice": 47.3,
                "stockvolume": 8762,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-16T00:00:00"),
                "stockopen": 47.0,
                "stockclose": 46.3,
                "stockhigh": 47.1,
                "stocklow": 46.3,
                "stockprice": 46.3,
                "stockvolume": 3934,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-15T00:00:00"),
                "stockopen": 46.3,
                "stockclose": 46.75,
                "stockhigh": 47.0,
                "stocklow": 46.2,
                "stockprice": 46.75,
                "stockvolume": 6526,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-12T00:00:00"),
                "stockopen": 47.5,
                "stockclose": 46.1,
                "stockhigh": 47.5,
                "stocklow": 46.1,
                "stockprice": 46.1,
                "stockvolume": 7045,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-11T00:00:00"),
                "stockopen": 47.1,
                "stockclose": 47.15,
                "stockhigh": 47.5,
                "stocklow": 46.55,
                "stockprice": 47.15,
                "stockvolume": 4319,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-10T00:00:00"),
                "stockopen": 47.5,
                "stockclose": 47.1,
                "stockhigh": 47.5,
                "stocklow": 46.35,
                "stockprice": 47.1,
                "stockvolume": 7442,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-09T00:00:00"),
                "stockopen": 47.5,
                "stockclose": 47.65,
                "stockhigh": 47.7,
                "stocklow": 47.4,
                "stockprice": 47.65,
                "stockvolume": 4984,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-05T00:00:00"),
                "stockopen": 47.55,
                "stockclose": 47.3,
                "stockhigh": 47.9,
                "stocklow": 47.25,
                "stockprice": 47.3,
                "stockvolume": 5878,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-04T00:00:00"),
                "stockopen": 47.7,
                "stockclose": 47.9,
                "stockhigh": 47.9,
                "stocklow": 47.35,
                "stockprice": 47.9,
                "stockvolume": 3383,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-03T00:00:00"),
                "stockopen": 47.2,
                "stockclose": 47.75,
                "stockhigh": 47.95,
                "stocklow": 47.2,
                "stockprice": 47.75,
                "stockvolume": 6575,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-02T00:00:00"),
                "stockopen": 48.4,
                "stockclose": 47.1,
                "stockhigh": 48.4,
                "stocklow": 47.0,
                "stockprice": 47.1,
                "stockvolume": 6887,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-01T00:00:00"),
                "stockopen": 47.5,
                "stockclose": 48.5,
                "stockhigh": 48.5,
                "stocklow": 47.5,
                "stockprice": 48.5,
                "stockvolume": 6054,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-29T00:00:00"),
                "stockopen": 47.8,
                "stockclose": 47.5,
                "stockhigh": 48.1,
                "stocklow": 47.5,
                "stockprice": 47.5,
                "stockvolume": 5881,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-28T00:00:00"),
                "stockopen": 48.15,
                "stockclose": 48.2,
                "stockhigh": 48.3,
                "stocklow": 47.75,
                "stockprice": 48.2,
                "stockvolume": 5300,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-27T00:00:00"),
                "stockopen": 48.4,
                "stockclose": 48.3,
                "stockhigh": 48.6,
                "stocklow": 48.0,
                "stockprice": 48.3,
                "stockvolume": 8404,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-26T00:00:00"),
                "stockopen": 48.15,
                "stockclose": 48.4,
                "stockhigh": 48.45,
                "stocklow": 47.9,
                "stockprice": 48.4,
                "stockvolume": 5255,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-25T00:00:00"),
                "stockopen": 49.55,
                "stockclose": 48.3,
                "stockhigh": 49.55,
                "stocklow": 48.1,
                "stockprice": 48.3,
                "stockvolume": 11137,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-22T00:00:00"),
                "stockopen": 47.7,
                "stockclose": 49.55,
                "stockhigh": 49.55,
                "stocklow": 47.6,
                "stockprice": 49.55,
                "stockvolume": 25596,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-21T00:00:00"),
                "stockopen": 47.2,
                "stockclose": 47.5,
                "stockhigh": 47.5,
                "stocklow": 46.8,
                "stockprice": 47.5,
                "stockvolume": 14538,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-20T00:00:00"),
                "stockopen": 46.4,
                "stockclose": 47.0,
                "stockhigh": 47.0,
                "stocklow": 46.05,
                "stockprice": 47.0,
                "stockvolume": 11028,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-19T00:00:00"),
                "stockopen": 46.0,
                "stockclose": 46.3,
                "stockhigh": 46.35,
                "stocklow": 45.85,
                "stockprice": 46.3,
                "stockvolume": 12410,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-18T00:00:00"),
                "stockopen": 45.95,
                "stockclose": 45.6,
                "stockhigh": 46.2,
                "stocklow": 45.55,
                "stockprice": 45.6,
                "stockvolume": 8459,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-15T00:00:00"),
                "stockopen": 46.1,
                "stockclose": 45.95,
                "stockhigh": 46.1,
                "stocklow": 45.55,
                "stockprice": 45.95,
                "stockvolume": 6059,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-14T00:00:00"),
                "stockopen": 45.75,
                "stockclose": 45.95,
                "stockhigh": 45.95,
                "stocklow": 44.9,
                "stockprice": 45.95,
                "stockvolume": 9013,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-13T00:00:00"),
                "stockopen": 45.0,
                "stockclose": 45.5,
                "stockhigh": 45.5,
                "stocklow": 45.0,
                "stockprice": 45.5,
                "stockvolume": 7214,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-12T00:00:00"),
                "stockopen": 45.2,
                "stockclose": 45.0,
                "stockhigh": 45.2,
                "stocklow": 44.4,
                "stockprice": 45.0,
                "stockvolume": 4468,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-11T00:00:00"),
                "stockopen": 44.9,
                "stockclose": 44.9,
                "stockhigh": 45.2,
                "stocklow": 44.8,
                "stockprice": 44.9,
                "stockvolume": 6094,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-08T00:00:00"),
                "stockopen": 44.6,
                "stockclose": 44.8,
                "stockhigh": 44.8,
                "stocklow": 44.1,
                "stockprice": 44.8,
                "stockvolume": 6494,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-07T00:00:00"),
                "stockopen": 44.75,
                "stockclose": 44.6,
                "stockhigh": 44.75,
                "stocklow": 44.2,
                "stockprice": 44.6,
                "stockvolume": 8293,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-06T00:00:00"),
                "stockopen": 44.3,
                "stockclose": 44.2,
                "stockhigh": 44.75,
                "stocklow": 43.85,
                "stockprice": 44.2,
                "stockvolume": 8088,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-05T00:00:00"),
                "stockopen": 45.55,
                "stockclose": 44.3,
                "stockhigh": 45.6,
                "stocklow": 44.25,
                "stockprice": 44.3,
                "stockvolume": 11884,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-04T00:00:00"),
                "stockopen": 45.0,
                "stockclose": 45.55,
                "stockhigh": 45.55,
                "stocklow": 44.5,
                "stockprice": 45.55,
                "stockvolume": 10532,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-01T00:00:00"),
                "stockopen": 44.7,
                "stockclose": 44.45,
                "stockhigh": 45.0,
                "stocklow": 44.4,
                "stockprice": 44.45,
                "stockvolume": 6425,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-31T00:00:00"),
                "stockopen": 45.75,
                "stockclose": 44.85,
                "stockhigh": 45.75,
                "stocklow": 44.5,
                "stockprice": 44.85,
                "stockvolume": 8821,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-30T00:00:00"),
                "stockopen": 45.9,
                "stockclose": 45.7,
                "stockhigh": 46.0,
                "stocklow": 45.2,
                "stockprice": 45.7,
                "stockvolume": 17744,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-29T00:00:00"),
                "stockopen": 44.3,
                "stockclose": 45.5,
                "stockhigh": 45.5,
                "stocklow": 44.2,
                "stockprice": 45.5,
                "stockvolume": 17122,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-28T00:00:00"),
                "stockopen": 44.0,
                "stockclose": 44.05,
                "stockhigh": 44.3,
                "stocklow": 44.0,
                "stockprice": 44.05,
                "stockvolume": 7068,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-25T00:00:00"),
                "stockopen": 44.0,
                "stockclose": 44.0,
                "stockhigh": 44.25,
                "stocklow": 43.65,
                "stockprice": 44.0,
                "stockvolume": 5741,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-24T00:00:00"),
                "stockopen": 44.0,
                "stockclose": 44.0,
                "stockhigh": 44.2,
                "stocklow": 43.65,
                "stockprice": 44.0,
                "stockvolume": 7529,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-22T00:00:00"),
                "stockopen": 44.2,
                "stockclose": 44.0,
                "stockhigh": 44.25,
                "stocklow": 43.8,
                "stockprice": 44.0,
                "stockvolume": 5007,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-21T00:00:00"),
                "stockopen": 44.1,
                "stockclose": 44.2,
                "stockhigh": 44.3,
                "stocklow": 44.0,
                "stockprice": 44.2,
                "stockvolume": 4318,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-18T00:00:00"),
                "stockopen": 43.7,
                "stockclose": 43.8,
                "stockhigh": 44.0,
                "stocklow": 43.6,
                "stockprice": 43.8,
                "stockvolume": 4474,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-17T00:00:00"),
                "stockopen": 44.0,
                "stockclose": 43.7,
                "stockhigh": 44.0,
                "stocklow": 43.5,
                "stockprice": 43.7,
                "stockvolume": 22401,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-16T00:00:00"),
                "stockopen": 45.5,
                "stockclose": 46.2,
                "stockhigh": 46.3,
                "stocklow": 45.4,
                "stockprice": 46.2,
                "stockvolume": 25983,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-15T00:00:00"),
                "stockopen": 45.5,
                "stockclose": 45.3,
                "stockhigh": 45.5,
                "stocklow": 45.1,
                "stockprice": 45.3,
                "stockvolume": 15298,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-14T00:00:00"),
                "stockopen": 45.5,
                "stockclose": 45.2,
                "stockhigh": 45.6,
                "stocklow": 45.05,
                "stockprice": 45.2,
                "stockvolume": 9870,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-11T00:00:00"),
                "stockopen": 45.5,
                "stockclose": 45.5,
                "stockhigh": 45.7,
                "stocklow": 45.2,
                "stockprice": 45.5,
                "stockvolume": 10916,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-10T00:00:00"),
                "stockopen": 45.8,
                "stockclose": 45.7,
                "stockhigh": 46.1,
                "stocklow": 45.4,
                "stockprice": 45.7,
                "stockvolume": 14377,
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
                result[0].traderprice = 45.0;
                result[0].traderbuyvolume = 49;
                result[0].tradersellvolume = 241;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "1440-美林",
            "stockidnm": "1101-台泥",
            "tradervolume": "290",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 45.0;
                result[0].traderbuyvolume = 19;
                result[0].tradersellvolume = 46;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "1470-摩根士丹利",
            "stockidnm": "1101-台泥",
            "tradervolume": "65",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 45.0;
                result[0].traderbuyvolume = 61;
                result[0].tradersellvolume = 13;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "1520-瑞士信貸",
            "stockidnm": "1101-台泥",
            "tradervolume": "74",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 45.0;
                result[0].traderbuyvolume = 0;
                result[0].tradersellvolume = 82;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "1560-港商野村",
            "stockidnm": "1101-台泥",
            "tradervolume": "82",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 45.0;
                result[0].traderbuyvolume = 0;
                result[0].tradersellvolume = 98;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "1650-瑞銀",
            "stockidnm": "1101-台泥",
            "tradervolume": "98",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 45.0;
                result[0].traderbuyvolume = 0;
                result[0].tradersellvolume = 146;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "2181-亞東板橋",
            "stockidnm": "1101-台泥",
            "tradervolume": "146",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 45.0;
                result[0].traderbuyvolume = 56;
                result[0].tradersellvolume = 0;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "5925-元富台中",
            "stockidnm": "1101-台泥",
            "tradervolume": "56",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 45.0;
                result[0].traderbuyvolume = 14;
                result[0].tradersellvolume = 39;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "8440-摩根大通",
            "stockidnm": "1101-台泥",
            "tradervolume": "53",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 45.0;
                result[0].traderbuyvolume = 54;
                result[0].tradersellvolume = 0;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "9131-群益民權",
            "stockidnm": "1101-台泥",
            "tradervolume": "54",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 45.0;
                result[0].traderbuyvolume = 102;
                result[0].tradersellvolume = 0;
            } else {
                alert("rrr");
            }
        
        var unit = {
            "traderidnm": "980h-元大台北",
            "stockidnm": "1101-台泥",
            "tradervolume": "102",
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

