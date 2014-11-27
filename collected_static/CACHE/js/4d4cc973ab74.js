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
                "date": new Date("2014-11-20T00:00:00"),
                "stockopen": 96.2,
                "stockclose": 96.7,
                "stockhigh": 97.0,
                "stocklow": 96.2,
                "stockprice": 96.7,
                "stockvolume": 28687,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-19T00:00:00"),
                "stockopen": 96.1,
                "stockclose": 96.0,
                "stockhigh": 97.0,
                "stocklow": 95.6,
                "stockprice": 96.0,
                "stockvolume": 39046,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-18T00:00:00"),
                "stockopen": 95.6,
                "stockclose": 95.5,
                "stockhigh": 96.6,
                "stocklow": 95.0,
                "stockprice": 95.5,
                "stockvolume": 25656,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-17T00:00:00"),
                "stockopen": 97.0,
                "stockclose": 95.6,
                "stockhigh": 97.8,
                "stocklow": 95.6,
                "stockprice": 95.6,
                "stockvolume": 36525,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-14T00:00:00"),
                "stockopen": 98.0,
                "stockclose": 96.8,
                "stockhigh": 98.1,
                "stocklow": 96.5,
                "stockprice": 96.8,
                "stockvolume": 35431,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-13T00:00:00"),
                "stockopen": 96.5,
                "stockclose": 98.0,
                "stockhigh": 98.0,
                "stocklow": 96.2,
                "stockprice": 98.0,
                "stockvolume": 24882,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-12T00:00:00"),
                "stockopen": 98.1,
                "stockclose": 96.0,
                "stockhigh": 99.0,
                "stocklow": 95.8,
                "stockprice": 96.0,
                "stockvolume": 39099,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-11T00:00:00"),
                "stockopen": 98.6,
                "stockclose": 97.7,
                "stockhigh": 98.6,
                "stocklow": 97.5,
                "stockprice": 97.7,
                "stockvolume": 22857,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-10T00:00:00"),
                "stockopen": 95.2,
                "stockclose": 98.3,
                "stockhigh": 98.4,
                "stocklow": 95.2,
                "stockprice": 98.3,
                "stockvolume": 35347,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-07T00:00:00"),
                "stockopen": 95.2,
                "stockclose": 96.3,
                "stockhigh": 96.5,
                "stocklow": 95.1,
                "stockprice": 96.3,
                "stockvolume": 18107,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-06T00:00:00"),
                "stockopen": 97.2,
                "stockclose": 95.9,
                "stockhigh": 97.9,
                "stocklow": 95.8,
                "stockprice": 95.9,
                "stockvolume": 26712,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-05T00:00:00"),
                "stockopen": 98.5,
                "stockclose": 98.2,
                "stockhigh": 98.5,
                "stocklow": 97.4,
                "stockprice": 98.2,
                "stockvolume": 16066,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-04T00:00:00"),
                "stockopen": 98.7,
                "stockclose": 97.5,
                "stockhigh": 98.7,
                "stocklow": 97.4,
                "stockprice": 97.5,
                "stockvolume": 19243,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-03T00:00:00"),
                "stockopen": 97.0,
                "stockclose": 98.1,
                "stockhigh": 98.7,
                "stocklow": 96.5,
                "stockprice": 98.1,
                "stockvolume": 38018,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-31T00:00:00"),
                "stockopen": 95.4,
                "stockclose": 96.0,
                "stockhigh": 96.2,
                "stocklow": 95.0,
                "stockprice": 96.0,
                "stockvolume": 28039,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-30T00:00:00"),
                "stockopen": 95.0,
                "stockclose": 95.2,
                "stockhigh": 95.5,
                "stocklow": 94.7,
                "stockprice": 95.2,
                "stockvolume": 15900,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-29T00:00:00"),
                "stockopen": 96.0,
                "stockclose": 95.0,
                "stockhigh": 96.2,
                "stocklow": 94.8,
                "stockprice": 95.0,
                "stockvolume": 28653,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-28T00:00:00"),
                "stockopen": 95.0,
                "stockclose": 95.5,
                "stockhigh": 95.8,
                "stocklow": 95.0,
                "stockprice": 95.5,
                "stockvolume": 32009,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-27T00:00:00"),
                "stockopen": 93.5,
                "stockclose": 94.0,
                "stockhigh": 94.5,
                "stocklow": 93.3,
                "stockprice": 94.0,
                "stockvolume": 20843,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-24T00:00:00"),
                "stockopen": 95.0,
                "stockclose": 93.2,
                "stockhigh": 95.3,
                "stocklow": 93.1,
                "stockprice": 93.2,
                "stockvolume": 22843,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-23T00:00:00"),
                "stockopen": 95.0,
                "stockclose": 95.0,
                "stockhigh": 95.0,
                "stocklow": 94.2,
                "stockprice": 95.0,
                "stockvolume": 22871,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-22T00:00:00"),
                "stockopen": 95.0,
                "stockclose": 94.0,
                "stockhigh": 95.5,
                "stocklow": 94.0,
                "stockprice": 94.0,
                "stockvolume": 33940,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-21T00:00:00"),
                "stockopen": 94.0,
                "stockclose": 93.5,
                "stockhigh": 94.6,
                "stocklow": 93.0,
                "stockprice": 93.5,
                "stockvolume": 36618,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-20T00:00:00"),
                "stockopen": 91.0,
                "stockclose": 93.2,
                "stockhigh": 93.4,
                "stocklow": 90.8,
                "stockprice": 93.2,
                "stockvolume": 34994,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-17T00:00:00"),
                "stockopen": 92.5,
                "stockclose": 89.0,
                "stockhigh": 92.8,
                "stocklow": 89.0,
                "stockprice": 89.0,
                "stockvolume": 66228,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-16T00:00:00"),
                "stockopen": 93.0,
                "stockclose": 92.2,
                "stockhigh": 93.4,
                "stocklow": 90.6,
                "stockprice": 92.2,
                "stockvolume": 52554,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-15T00:00:00"),
                "stockopen": 95.5,
                "stockclose": 93.5,
                "stockhigh": 95.7,
                "stocklow": 92.4,
                "stockprice": 93.5,
                "stockvolume": 90024,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-14T00:00:00"),
                "stockopen": 95.6,
                "stockclose": 96.0,
                "stockhigh": 96.1,
                "stocklow": 95.0,
                "stockprice": 96.0,
                "stockvolume": 32867,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-13T00:00:00"),
                "stockopen": 95.0,
                "stockclose": 95.8,
                "stockhigh": 96.7,
                "stocklow": 95.0,
                "stockprice": 95.8,
                "stockvolume": 35801,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-09T00:00:00"),
                "stockopen": 98.2,
                "stockclose": 97.6,
                "stockhigh": 98.3,
                "stocklow": 96.7,
                "stockprice": 97.6,
                "stockvolume": 27512,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-08T00:00:00"),
                "stockopen": 96.5,
                "stockclose": 96.7,
                "stockhigh": 97.6,
                "stocklow": 96.5,
                "stockprice": 96.7,
                "stockvolume": 22228,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-07T00:00:00"),
                "stockopen": 98.6,
                "stockclose": 97.6,
                "stockhigh": 99.0,
                "stocklow": 97.0,
                "stockprice": 97.6,
                "stockvolume": 27137,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-06T00:00:00"),
                "stockopen": 99.7,
                "stockclose": 98.5,
                "stockhigh": 99.7,
                "stocklow": 98.5,
                "stockprice": 98.5,
                "stockvolume": 22887,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-03T00:00:00"),
                "stockopen": 98.0,
                "stockclose": 99.3,
                "stockhigh": 99.7,
                "stocklow": 97.9,
                "stockprice": 99.3,
                "stockvolume": 24011,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-02T00:00:00"),
                "stockopen": 97.8,
                "stockclose": 97.5,
                "stockhigh": 98.4,
                "stocklow": 97.1,
                "stockprice": 97.5,
                "stockvolume": 23725,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-01T00:00:00"),
                "stockopen": 96.5,
                "stockclose": 98.4,
                "stockhigh": 98.6,
                "stocklow": 95.5,
                "stockprice": 98.4,
                "stockvolume": 30242,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-30T00:00:00"),
                "stockopen": 97.5,
                "stockclose": 96.0,
                "stockhigh": 97.5,
                "stocklow": 94.8,
                "stockprice": 96.0,
                "stockvolume": 53444,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-29T00:00:00"),
                "stockopen": 97.8,
                "stockclose": 97.6,
                "stockhigh": 98.2,
                "stocklow": 97.1,
                "stockprice": 97.6,
                "stockvolume": 38784,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-26T00:00:00"),
                "stockopen": 99.0,
                "stockclose": 97.1,
                "stockhigh": 99.0,
                "stocklow": 97.1,
                "stockprice": 97.1,
                "stockvolume": 58713,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-25T00:00:00"),
                "stockopen": 101.0,
                "stockclose": 100.0,
                "stockhigh": 102.5,
                "stocklow": 99.6,
                "stockprice": 100.0,
                "stockvolume": 35162,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-24T00:00:00"),
                "stockopen": 100.0,
                "stockclose": 100.5,
                "stockhigh": 101.0,
                "stocklow": 100.0,
                "stockprice": 100.5,
                "stockvolume": 16931,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-23T00:00:00"),
                "stockopen": 100.5,
                "stockclose": 100.5,
                "stockhigh": 101.0,
                "stocklow": 99.8,
                "stockprice": 100.5,
                "stockvolume": 16015,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-22T00:00:00"),
                "stockopen": 100.5,
                "stockclose": 100.5,
                "stockhigh": 100.5,
                "stocklow": 99.6,
                "stockprice": 100.5,
                "stockvolume": 24844,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-19T00:00:00"),
                "stockopen": 102.5,
                "stockclose": 101.0,
                "stockhigh": 103.0,
                "stocklow": 101.0,
                "stockprice": 101.0,
                "stockvolume": 32404,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-18T00:00:00"),
                "stockopen": 100.5,
                "stockclose": 102.0,
                "stockhigh": 102.0,
                "stocklow": 100.5,
                "stockprice": 102.0,
                "stockvolume": 22083,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-17T00:00:00"),
                "stockopen": 100.0,
                "stockclose": 101.0,
                "stockhigh": 101.5,
                "stocklow": 100.0,
                "stockprice": 101.0,
                "stockvolume": 27850,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-16T00:00:00"),
                "stockopen": 101.0,
                "stockclose": 99.5,
                "stockhigh": 101.0,
                "stocklow": 99.5,
                "stockprice": 99.5,
                "stockvolume": 15858,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-15T00:00:00"),
                "stockopen": 99.4,
                "stockclose": 101.0,
                "stockhigh": 101.0,
                "stocklow": 99.2,
                "stockprice": 101.0,
                "stockvolume": 17076,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-12T00:00:00"),
                "stockopen": 100.5,
                "stockclose": 99.4,
                "stockhigh": 100.5,
                "stocklow": 99.1,
                "stockprice": 99.4,
                "stockvolume": 23455,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-11T00:00:00"),
                "stockopen": 100.5,
                "stockclose": 100.0,
                "stockhigh": 101.5,
                "stocklow": 100.0,
                "stockprice": 100.0,
                "stockvolume": 18011,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-10T00:00:00"),
                "stockopen": 101.0,
                "stockclose": 101.0,
                "stockhigh": 101.5,
                "stocklow": 99.6,
                "stockprice": 101.0,
                "stockvolume": 30085,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-09T00:00:00"),
                "stockopen": 101.0,
                "stockclose": 102.0,
                "stockhigh": 102.0,
                "stocklow": 100.5,
                "stockprice": 102.0,
                "stockvolume": 25181,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-05T00:00:00"),
                "stockopen": 99.5,
                "stockclose": 100.5,
                "stockhigh": 100.5,
                "stocklow": 98.6,
                "stockprice": 100.5,
                "stockvolume": 37775,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-04T00:00:00"),
                "stockopen": 100.5,
                "stockclose": 99.9,
                "stockhigh": 100.5,
                "stocklow": 99.5,
                "stockprice": 99.9,
                "stockvolume": 42401,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-03T00:00:00"),
                "stockopen": 101.0,
                "stockclose": 101.0,
                "stockhigh": 101.5,
                "stocklow": 100.0,
                "stockprice": 101.0,
                "stockvolume": 29980,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-02T00:00:00"),
                "stockopen": 101.5,
                "stockclose": 100.5,
                "stockhigh": 102.0,
                "stocklow": 100.5,
                "stockprice": 100.5,
                "stockvolume": 22070,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-01T00:00:00"),
                "stockopen": 103.0,
                "stockclose": 101.5,
                "stockhigh": 103.5,
                "stocklow": 101.5,
                "stockprice": 101.5,
                "stockvolume": 29167,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-29T00:00:00"),
                "stockopen": 102.0,
                "stockclose": 102.0,
                "stockhigh": 103.0,
                "stocklow": 101.0,
                "stockprice": 102.0,
                "stockvolume": 40542,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-28T00:00:00"),
                "stockopen": 100.5,
                "stockclose": 102.0,
                "stockhigh": 104.0,
                "stocklow": 100.5,
                "stockprice": 102.0,
                "stockvolume": 105054,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-27T00:00:00"),
                "stockopen": 110.0,
                "stockclose": 112.0,
                "stockhigh": 112.0,
                "stocklow": 110.0,
                "stockprice": 112.0,
                "stockvolume": 87045,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-26T00:00:00"),
                "stockopen": 110.5,
                "stockclose": 110.0,
                "stockhigh": 111.0,
                "stocklow": 109.5,
                "stockprice": 110.0,
                "stockvolume": 40265,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-25T00:00:00"),
                "stockopen": 110.0,
                "stockclose": 110.5,
                "stockhigh": 111.0,
                "stocklow": 109.5,
                "stockprice": 110.5,
                "stockvolume": 25906,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-22T00:00:00"),
                "stockopen": 109.0,
                "stockclose": 110.0,
                "stockhigh": 110.0,
                "stocklow": 108.5,
                "stockprice": 110.0,
                "stockvolume": 35790,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-21T00:00:00"),
                "stockopen": 108.5,
                "stockclose": 108.5,
                "stockhigh": 108.5,
                "stocklow": 107.5,
                "stockprice": 108.5,
                "stockvolume": 15557,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-20T00:00:00"),
                "stockopen": 109.5,
                "stockclose": 108.5,
                "stockhigh": 109.5,
                "stocklow": 107.0,
                "stockprice": 108.5,
                "stockvolume": 27207,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-19T00:00:00"),
                "stockopen": 108.5,
                "stockclose": 108.5,
                "stockhigh": 109.5,
                "stocklow": 107.5,
                "stockprice": 108.5,
                "stockvolume": 21745,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-18T00:00:00"),
                "stockopen": 108.0,
                "stockclose": 107.5,
                "stockhigh": 108.5,
                "stocklow": 107.5,
                "stockprice": 107.5,
                "stockvolume": 18848,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-15T00:00:00"),
                "stockopen": 109.0,
                "stockclose": 107.5,
                "stockhigh": 109.5,
                "stocklow": 107.0,
                "stockprice": 107.5,
                "stockvolume": 28562,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-14T00:00:00"),
                "stockopen": 109.5,
                "stockclose": 109.0,
                "stockhigh": 111.0,
                "stocklow": 108.0,
                "stockprice": 109.0,
                "stockvolume": 38756,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-13T00:00:00"),
                "stockopen": 104.5,
                "stockclose": 106.0,
                "stockhigh": 106.5,
                "stocklow": 104.5,
                "stockprice": 106.0,
                "stockvolume": 26383,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-12T00:00:00"),
                "stockopen": 104.0,
                "stockclose": 104.5,
                "stockhigh": 105.5,
                "stocklow": 103.5,
                "stockprice": 104.5,
                "stockvolume": 22237,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-11T00:00:00"),
                "stockopen": 101.0,
                "stockclose": 104.0,
                "stockhigh": 105.0,
                "stocklow": 100.5,
                "stockprice": 104.0,
                "stockvolume": 35057,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-08T00:00:00"),
                "stockopen": 103.5,
                "stockclose": 102.5,
                "stockhigh": 103.5,
                "stocklow": 101.5,
                "stockprice": 102.5,
                "stockvolume": 19775,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-07T00:00:00"),
                "stockopen": 104.5,
                "stockclose": 103.5,
                "stockhigh": 104.5,
                "stocklow": 102.5,
                "stockprice": 103.5,
                "stockvolume": 15553,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-06T00:00:00"),
                "stockopen": 102.0,
                "stockclose": 103.5,
                "stockhigh": 103.5,
                "stocklow": 101.0,
                "stockprice": 103.5,
                "stockvolume": 24413,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-05T00:00:00"),
                "stockopen": 105.0,
                "stockclose": 102.0,
                "stockhigh": 105.0,
                "stocklow": 102.0,
                "stockprice": 102.0,
                "stockvolume": 31938,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-04T00:00:00"),
                "stockopen": 102.0,
                "stockclose": 105.5,
                "stockhigh": 105.5,
                "stocklow": 102.0,
                "stockprice": 105.5,
                "stockvolume": 22866,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-01T00:00:00"),
                "stockopen": 101.0,
                "stockclose": 102.0,
                "stockhigh": 102.5,
                "stocklow": 100.5,
                "stockprice": 102.0,
                "stockvolume": 32762,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-31T00:00:00"),
                "stockopen": 104.5,
                "stockclose": 103.5,
                "stockhigh": 105.0,
                "stocklow": 102.5,
                "stockprice": 103.5,
                "stockvolume": 29623,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-30T00:00:00"),
                "stockopen": 106.0,
                "stockclose": 104.5,
                "stockhigh": 107.0,
                "stocklow": 104.5,
                "stockprice": 104.5,
                "stockvolume": 31370,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-29T00:00:00"),
                "stockopen": 106.0,
                "stockclose": 105.0,
                "stockhigh": 107.0,
                "stocklow": 102.0,
                "stockprice": 105.0,
                "stockvolume": 49762,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-28T00:00:00"),
                "stockopen": 107.0,
                "stockclose": 105.0,
                "stockhigh": 108.0,
                "stocklow": 105.0,
                "stockprice": 105.0,
                "stockvolume": 37840,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-25T00:00:00"),
                "stockopen": 109.5,
                "stockclose": 108.0,
                "stockhigh": 110.5,
                "stocklow": 107.0,
                "stockprice": 108.0,
                "stockvolume": 25472,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-24T00:00:00"),
                "stockopen": 111.0,
                "stockclose": 110.5,
                "stockhigh": 112.0,
                "stocklow": 108.5,
                "stockprice": 110.5,
                "stockvolume": 33521,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-22T00:00:00"),
                "stockopen": 110.5,
                "stockclose": 110.0,
                "stockhigh": 110.5,
                "stocklow": 107.5,
                "stockprice": 110.0,
                "stockvolume": 25372,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-21T00:00:00"),
                "stockopen": 109.0,
                "stockclose": 110.5,
                "stockhigh": 110.5,
                "stocklow": 108.5,
                "stockprice": 110.5,
                "stockvolume": 31307,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-18T00:00:00"),
                "stockopen": 104.5,
                "stockclose": 107.5,
                "stockhigh": 107.5,
                "stocklow": 104.5,
                "stockprice": 107.5,
                "stockvolume": 28216,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-17T00:00:00"),
                "stockopen": 107.0,
                "stockclose": 106.5,
                "stockhigh": 108.0,
                "stocklow": 105.0,
                "stockprice": 106.5,
                "stockvolume": 43816,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-16T00:00:00"),
                "stockopen": 111.0,
                "stockclose": 107.5,
                "stockhigh": 111.0,
                "stocklow": 107.0,
                "stockprice": 107.5,
                "stockvolume": 42722,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-15T00:00:00"),
                "stockopen": 110.5,
                "stockclose": 111.0,
                "stockhigh": 111.5,
                "stocklow": 109.0,
                "stockprice": 111.0,
                "stockvolume": 50007,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-14T00:00:00"),
                "stockopen": 109.0,
                "stockclose": 110.0,
                "stockhigh": 113.0,
                "stocklow": 109.0,
                "stockprice": 110.0,
                "stockvolume": 66688,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-11T00:00:00"),
                "stockopen": 109.0,
                "stockclose": 109.0,
                "stockhigh": 112.0,
                "stocklow": 108.0,
                "stockprice": 109.0,
                "stockvolume": 69080,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-10T00:00:00"),
                "stockopen": 105.0,
                "stockclose": 108.5,
                "stockhigh": 108.5,
                "stocklow": 105.0,
                "stockprice": 108.5,
                "stockvolume": 51473,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-09T00:00:00"),
                "stockopen": 104.0,
                "stockclose": 105.0,
                "stockhigh": 105.0,
                "stocklow": 103.5,
                "stockprice": 105.0,
                "stockvolume": 24427,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-08T00:00:00"),
                "stockopen": 104.0,
                "stockclose": 104.5,
                "stockhigh": 104.5,
                "stocklow": 103.5,
                "stockprice": 104.5,
                "stockvolume": 21969,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-07T00:00:00"),
                "stockopen": 102.0,
                "stockclose": 103.5,
                "stockhigh": 103.5,
                "stocklow": 101.5,
                "stockprice": 103.5,
                "stockvolume": 26119,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-04T00:00:00"),
                "stockopen": 104.5,
                "stockclose": 103.0,
                "stockhigh": 104.5,
                "stocklow": 102.5,
                "stockprice": 103.0,
                "stockvolume": 24537,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-03T00:00:00"),
                "stockopen": 103.5,
                "stockclose": 104.0,
                "stockhigh": 104.5,
                "stocklow": 103.0,
                "stockprice": 104.0,
                "stockvolume": 31242,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-02T00:00:00"),
                "stockopen": 102.5,
                "stockclose": 103.0,
                "stockhigh": 105.0,
                "stocklow": 102.0,
                "stockprice": 103.0,
                "stockvolume": 57731,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-01T00:00:00"),
                "stockopen": 100.5,
                "stockclose": 102.0,
                "stockhigh": 102.0,
                "stocklow": 100.0,
                "stockprice": 102.0,
                "stockvolume": 36524,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-27T00:00:00"),
                "stockopen": 97.3,
                "stockclose": 97.1,
                "stockhigh": 97.9,
                "stocklow": 97.1,
                "stockprice": 97.1,
                "stockvolume": 27026,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-26T00:00:00"),
                "stockopen": 96.5,
                "stockclose": 97.3,
                "stockhigh": 98.0,
                "stocklow": 96.5,
                "stockprice": 97.3,
                "stockvolume": 30379,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-25T00:00:00"),
                "stockopen": 96.5,
                "stockclose": 96.4,
                "stockhigh": 96.9,
                "stocklow": 96.1,
                "stockprice": 96.4,
                "stockvolume": 30621,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-24T00:00:00"),
                "stockopen": 96.8,
                "stockclose": 96.5,
                "stockhigh": 96.9,
                "stocklow": 96.3,
                "stockprice": 96.5,
                "stockvolume": 19076,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-21T00:00:00"),
                "stockopen": 97.4,
                "stockclose": 96.3,
                "stockhigh": 97.5,
                "stocklow": 96.2,
                "stockprice": 96.3,
                "stockvolume": 29685,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
    
    // populate trader data as update
    
        
            var date = new Date("2014-11-25T00:00:00");
            var result = jQuery.grep(data, function(e){ return e.date == date; });
            if (result.length != 0) {
                result[0].traderprice = 96.0;
                result[0].traderbuyvolume = 82;
                result[0].tradersellvolume = 522;
            }
        
        var unit = {
            "traderid": "1590",
            "stockid": "2317",
            "url": "",
            "description": "",
            "data": data
        }
        chartData.push(unit);
    
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(data, function(e){ return e.date == date; });
            if (result.length != 0) {
                result[0].traderprice = 97.0;
                result[0].traderbuyvolume = 58;
                result[0].tradersellvolume = 314;
            }
        
        var unit = {
            "traderid": "8440",
            "stockid": "2317",
            "url": "",
            "description": "",
            "data": data
        }
        chartData.push(unit);
    
}

function checkChartData(){
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

