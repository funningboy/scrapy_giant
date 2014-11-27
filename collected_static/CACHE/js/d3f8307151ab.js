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
                "stockopen": 140.0,
                "stockclose": 140.0,
                "stockhigh": 142.0,
                "stocklow": 140.0,
                "stockprice": 140.0,
                "stockvolume": 26580,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-26T00:00:00"),
                "stockopen": 138.5,
                "stockclose": 139.0,
                "stockhigh": 139.0,
                "stocklow": 138.0,
                "stockprice": 139.0,
                "stockvolume": 23201,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-25T00:00:00"),
                "stockopen": 138.5,
                "stockclose": 139.0,
                "stockhigh": 140.0,
                "stocklow": 138.5,
                "stockprice": 139.0,
                "stockvolume": 42940,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-24T00:00:00"),
                "stockopen": 140.0,
                "stockclose": 138.5,
                "stockhigh": 140.5,
                "stocklow": 138.0,
                "stockprice": 138.5,
                "stockvolume": 33408,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-21T00:00:00"),
                "stockopen": 139.5,
                "stockclose": 138.5,
                "stockhigh": 139.5,
                "stocklow": 137.5,
                "stockprice": 138.5,
                "stockvolume": 30621,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-20T00:00:00"),
                "stockopen": 137.5,
                "stockclose": 139.0,
                "stockhigh": 139.0,
                "stocklow": 137.0,
                "stockprice": 139.0,
                "stockvolume": 44216,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-19T00:00:00"),
                "stockopen": 133.0,
                "stockclose": 136.0,
                "stockhigh": 136.5,
                "stocklow": 132.5,
                "stockprice": 136.0,
                "stockvolume": 71400,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-18T00:00:00"),
                "stockopen": 134.0,
                "stockclose": 131.5,
                "stockhigh": 134.5,
                "stocklow": 131.0,
                "stockprice": 131.5,
                "stockvolume": 43227,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-17T00:00:00"),
                "stockopen": 135.0,
                "stockclose": 133.0,
                "stockhigh": 135.5,
                "stocklow": 132.5,
                "stockprice": 133.0,
                "stockvolume": 24772,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-14T00:00:00"),
                "stockopen": 134.0,
                "stockclose": 135.0,
                "stockhigh": 135.0,
                "stocklow": 133.5,
                "stockprice": 135.0,
                "stockvolume": 24361,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-13T00:00:00"),
                "stockopen": 133.5,
                "stockclose": 134.0,
                "stockhigh": 134.5,
                "stocklow": 132.5,
                "stockprice": 134.0,
                "stockvolume": 25055,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-12T00:00:00"),
                "stockopen": 134.5,
                "stockclose": 132.0,
                "stockhigh": 134.5,
                "stocklow": 131.5,
                "stockprice": 132.0,
                "stockvolume": 27434,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-11T00:00:00"),
                "stockopen": 135.0,
                "stockclose": 134.0,
                "stockhigh": 135.0,
                "stocklow": 133.0,
                "stockprice": 134.0,
                "stockvolume": 20484,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-10T00:00:00"),
                "stockopen": 132.5,
                "stockclose": 134.5,
                "stockhigh": 134.5,
                "stocklow": 132.0,
                "stockprice": 134.5,
                "stockvolume": 43174,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-07T00:00:00"),
                "stockopen": 131.5,
                "stockclose": 131.0,
                "stockhigh": 131.5,
                "stocklow": 130.5,
                "stockprice": 131.0,
                "stockvolume": 17385,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-06T00:00:00"),
                "stockopen": 132.5,
                "stockclose": 132.0,
                "stockhigh": 132.5,
                "stocklow": 131.5,
                "stockprice": 132.0,
                "stockvolume": 28559,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-05T00:00:00"),
                "stockopen": 131.5,
                "stockclose": 132.0,
                "stockhigh": 132.0,
                "stocklow": 131.0,
                "stockprice": 132.0,
                "stockvolume": 22638,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-04T00:00:00"),
                "stockopen": 132.0,
                "stockclose": 132.0,
                "stockhigh": 132.0,
                "stocklow": 131.0,
                "stockprice": 132.0,
                "stockvolume": 32566,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-03T00:00:00"),
                "stockopen": 132.0,
                "stockclose": 131.0,
                "stockhigh": 132.5,
                "stocklow": 130.5,
                "stockprice": 131.0,
                "stockvolume": 45307,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-31T00:00:00"),
                "stockopen": 128.0,
                "stockclose": 130.5,
                "stockhigh": 130.5,
                "stocklow": 127.5,
                "stockprice": 130.5,
                "stockvolume": 42413,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-30T00:00:00"),
                "stockopen": 128.5,
                "stockclose": 128.5,
                "stockhigh": 129.0,
                "stocklow": 127.0,
                "stockprice": 128.5,
                "stockvolume": 35723,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-29T00:00:00"),
                "stockopen": 129.0,
                "stockclose": 129.0,
                "stockhigh": 129.5,
                "stocklow": 128.0,
                "stockprice": 129.0,
                "stockvolume": 34860,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-28T00:00:00"),
                "stockopen": 129.0,
                "stockclose": 128.0,
                "stockhigh": 129.5,
                "stocklow": 127.5,
                "stockprice": 128.0,
                "stockvolume": 35018,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-27T00:00:00"),
                "stockopen": 126.5,
                "stockclose": 128.0,
                "stockhigh": 128.0,
                "stocklow": 126.5,
                "stockprice": 128.0,
                "stockvolume": 25145,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-24T00:00:00"),
                "stockopen": 127.0,
                "stockclose": 125.5,
                "stockhigh": 127.5,
                "stocklow": 125.0,
                "stockprice": 125.5,
                "stockvolume": 42161,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-23T00:00:00"),
                "stockopen": 128.0,
                "stockclose": 127.5,
                "stockhigh": 128.5,
                "stocklow": 127.5,
                "stockprice": 127.5,
                "stockvolume": 28085,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-22T00:00:00"),
                "stockopen": 127.5,
                "stockclose": 129.0,
                "stockhigh": 129.0,
                "stocklow": 127.5,
                "stockprice": 129.0,
                "stockvolume": 65855,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-21T00:00:00"),
                "stockopen": 126.0,
                "stockclose": 125.0,
                "stockhigh": 126.0,
                "stocklow": 124.5,
                "stockprice": 125.0,
                "stockvolume": 25647,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-20T00:00:00"),
                "stockopen": 125.0,
                "stockclose": 126.0,
                "stockhigh": 126.0,
                "stocklow": 124.5,
                "stockprice": 126.0,
                "stockvolume": 38619,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-17T00:00:00"),
                "stockopen": 125.0,
                "stockclose": 123.5,
                "stockhigh": 125.5,
                "stocklow": 123.5,
                "stockprice": 123.5,
                "stockvolume": 92077,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-16T00:00:00"),
                "stockopen": 121.5,
                "stockclose": 121.5,
                "stockhigh": 124.0,
                "stocklow": 120.0,
                "stockprice": 121.5,
                "stockvolume": 46431,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-15T00:00:00"),
                "stockopen": 121.5,
                "stockclose": 121.5,
                "stockhigh": 123.0,
                "stocklow": 121.0,
                "stockprice": 121.5,
                "stockvolume": 50496,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-14T00:00:00"),
                "stockopen": 120.0,
                "stockclose": 121.0,
                "stockhigh": 121.5,
                "stocklow": 119.5,
                "stockprice": 121.0,
                "stockvolume": 31887,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-13T00:00:00"),
                "stockopen": 119.0,
                "stockclose": 120.5,
                "stockhigh": 121.5,
                "stocklow": 118.0,
                "stockprice": 120.5,
                "stockvolume": 77985,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-09T00:00:00"),
                "stockopen": 124.0,
                "stockclose": 125.0,
                "stockhigh": 125.0,
                "stocklow": 123.5,
                "stockprice": 125.0,
                "stockvolume": 37115,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-08T00:00:00"),
                "stockopen": 123.5,
                "stockclose": 122.5,
                "stockhigh": 125.0,
                "stocklow": 122.5,
                "stockprice": 122.5,
                "stockvolume": 30938,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-07T00:00:00"),
                "stockopen": 125.0,
                "stockclose": 125.0,
                "stockhigh": 125.5,
                "stocklow": 123.5,
                "stockprice": 125.0,
                "stockvolume": 40188,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-06T00:00:00"),
                "stockopen": 125.0,
                "stockclose": 126.0,
                "stockhigh": 126.0,
                "stocklow": 124.0,
                "stockprice": 126.0,
                "stockvolume": 39292,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-03T00:00:00"),
                "stockopen": 122.5,
                "stockclose": 124.5,
                "stockhigh": 125.0,
                "stocklow": 122.0,
                "stockprice": 124.5,
                "stockvolume": 52042,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-02T00:00:00"),
                "stockopen": 121.0,
                "stockclose": 121.0,
                "stockhigh": 122.5,
                "stocklow": 120.5,
                "stockprice": 121.0,
                "stockvolume": 30795,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-01T00:00:00"),
                "stockopen": 120.0,
                "stockclose": 121.5,
                "stockhigh": 122.0,
                "stocklow": 120.0,
                "stockprice": 121.5,
                "stockvolume": 42581,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-30T00:00:00"),
                "stockopen": 120.0,
                "stockclose": 120.0,
                "stockhigh": 121.0,
                "stocklow": 119.0,
                "stockprice": 120.0,
                "stockvolume": 52027,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-29T00:00:00"),
                "stockopen": 122.0,
                "stockclose": 120.5,
                "stockhigh": 122.0,
                "stocklow": 120.0,
                "stockprice": 120.5,
                "stockvolume": 55071,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-26T00:00:00"),
                "stockopen": 121.0,
                "stockclose": 121.0,
                "stockhigh": 121.5,
                "stocklow": 120.5,
                "stockprice": 121.0,
                "stockvolume": 25408,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-25T00:00:00"),
                "stockopen": 123.0,
                "stockclose": 122.0,
                "stockhigh": 124.0,
                "stocklow": 121.5,
                "stockprice": 122.0,
                "stockvolume": 23840,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-24T00:00:00"),
                "stockopen": 122.0,
                "stockclose": 123.0,
                "stockhigh": 124.0,
                "stocklow": 122.0,
                "stockprice": 123.0,
                "stockvolume": 28552,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-23T00:00:00"),
                "stockopen": 123.0,
                "stockclose": 122.5,
                "stockhigh": 123.5,
                "stocklow": 122.0,
                "stockprice": 122.5,
                "stockvolume": 16208,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-22T00:00:00"),
                "stockopen": 124.0,
                "stockclose": 122.0,
                "stockhigh": 124.0,
                "stocklow": 122.0,
                "stockprice": 122.0,
                "stockvolume": 40658,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-19T00:00:00"),
                "stockopen": 125.5,
                "stockclose": 125.0,
                "stockhigh": 126.0,
                "stocklow": 125.0,
                "stockprice": 125.0,
                "stockvolume": 30781,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-18T00:00:00"),
                "stockopen": 124.5,
                "stockclose": 125.0,
                "stockhigh": 125.0,
                "stocklow": 123.5,
                "stockprice": 125.0,
                "stockvolume": 14791,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-17T00:00:00"),
                "stockopen": 123.5,
                "stockclose": 124.5,
                "stockhigh": 125.0,
                "stocklow": 123.0,
                "stockprice": 124.5,
                "stockvolume": 24018,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-16T00:00:00"),
                "stockopen": 123.0,
                "stockclose": 122.5,
                "stockhigh": 123.0,
                "stocklow": 122.0,
                "stockprice": 122.5,
                "stockvolume": 19248,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-15T00:00:00"),
                "stockopen": 122.5,
                "stockclose": 123.5,
                "stockhigh": 123.5,
                "stocklow": 122.0,
                "stockprice": 123.5,
                "stockvolume": 19643,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-12T00:00:00"),
                "stockopen": 124.5,
                "stockclose": 123.0,
                "stockhigh": 125.0,
                "stocklow": 123.0,
                "stockprice": 123.0,
                "stockvolume": 20299,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-11T00:00:00"),
                "stockopen": 126.0,
                "stockclose": 125.0,
                "stockhigh": 126.0,
                "stocklow": 125.0,
                "stockprice": 125.0,
                "stockvolume": 24328,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-10T00:00:00"),
                "stockopen": 126.0,
                "stockclose": 125.0,
                "stockhigh": 126.0,
                "stocklow": 124.0,
                "stockprice": 125.0,
                "stockvolume": 29718,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-09T00:00:00"),
                "stockopen": 127.5,
                "stockclose": 127.0,
                "stockhigh": 127.5,
                "stocklow": 126.5,
                "stockprice": 127.0,
                "stockvolume": 24359,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-05T00:00:00"),
                "stockopen": 128.5,
                "stockclose": 127.0,
                "stockhigh": 128.5,
                "stocklow": 125.5,
                "stockprice": 127.0,
                "stockvolume": 20128,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-04T00:00:00"),
                "stockopen": 128.0,
                "stockclose": 127.5,
                "stockhigh": 128.0,
                "stocklow": 126.0,
                "stockprice": 127.5,
                "stockvolume": 22110,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-03T00:00:00"),
                "stockopen": 127.0,
                "stockclose": 128.0,
                "stockhigh": 128.0,
                "stocklow": 125.5,
                "stockprice": 128.0,
                "stockvolume": 24642,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-02T00:00:00"),
                "stockopen": 128.0,
                "stockclose": 126.0,
                "stockhigh": 128.0,
                "stocklow": 125.5,
                "stockprice": 126.0,
                "stockvolume": 20057,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-01T00:00:00"),
                "stockopen": 125.0,
                "stockclose": 128.5,
                "stockhigh": 128.5,
                "stocklow": 125.0,
                "stockprice": 128.5,
                "stockvolume": 37523,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-29T00:00:00"),
                "stockopen": 124.5,
                "stockclose": 124.0,
                "stockhigh": 125.0,
                "stocklow": 124.0,
                "stockprice": 124.0,
                "stockvolume": 28358,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-28T00:00:00"),
                "stockopen": 126.0,
                "stockclose": 125.0,
                "stockhigh": 126.0,
                "stocklow": 124.5,
                "stockprice": 125.0,
                "stockvolume": 21759,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-27T00:00:00"),
                "stockopen": 125.5,
                "stockclose": 125.5,
                "stockhigh": 126.0,
                "stocklow": 124.5,
                "stockprice": 125.5,
                "stockvolume": 36839,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-26T00:00:00"),
                "stockopen": 125.0,
                "stockclose": 124.5,
                "stockhigh": 125.5,
                "stocklow": 124.0,
                "stockprice": 124.5,
                "stockvolume": 30428,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-25T00:00:00"),
                "stockopen": 125.5,
                "stockclose": 125.0,
                "stockhigh": 126.0,
                "stocklow": 125.0,
                "stockprice": 125.0,
                "stockvolume": 21107,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-22T00:00:00"),
                "stockopen": 124.5,
                "stockclose": 125.5,
                "stockhigh": 126.0,
                "stocklow": 123.5,
                "stockprice": 125.5,
                "stockvolume": 42775,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-21T00:00:00"),
                "stockopen": 126.0,
                "stockclose": 124.5,
                "stockhigh": 126.0,
                "stocklow": 124.0,
                "stockprice": 124.5,
                "stockvolume": 23089,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-20T00:00:00"),
                "stockopen": 125.0,
                "stockclose": 125.5,
                "stockhigh": 125.5,
                "stocklow": 124.5,
                "stockprice": 125.5,
                "stockvolume": 28975,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-19T00:00:00"),
                "stockopen": 124.0,
                "stockclose": 124.0,
                "stockhigh": 125.0,
                "stocklow": 123.5,
                "stockprice": 124.0,
                "stockvolume": 31922,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-18T00:00:00"),
                "stockopen": 124.0,
                "stockclose": 123.0,
                "stockhigh": 124.0,
                "stocklow": 122.5,
                "stockprice": 123.0,
                "stockvolume": 14766,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-15T00:00:00"),
                "stockopen": 124.5,
                "stockclose": 124.0,
                "stockhigh": 125.0,
                "stocklow": 123.0,
                "stockprice": 124.0,
                "stockvolume": 19189,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-14T00:00:00"),
                "stockopen": 123.5,
                "stockclose": 124.0,
                "stockhigh": 124.0,
                "stocklow": 123.0,
                "stockprice": 124.0,
                "stockvolume": 32955,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-13T00:00:00"),
                "stockopen": 121.0,
                "stockclose": 122.5,
                "stockhigh": 123.5,
                "stocklow": 120.5,
                "stockprice": 122.5,
                "stockvolume": 39837,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-12T00:00:00"),
                "stockopen": 121.0,
                "stockclose": 121.5,
                "stockhigh": 122.0,
                "stocklow": 120.5,
                "stockprice": 121.5,
                "stockvolume": 32278,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-11T00:00:00"),
                "stockopen": 120.0,
                "stockclose": 120.5,
                "stockhigh": 121.0,
                "stocklow": 119.5,
                "stockprice": 120.5,
                "stockvolume": 42993,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-08T00:00:00"),
                "stockopen": 120.5,
                "stockclose": 120.5,
                "stockhigh": 121.0,
                "stocklow": 119.5,
                "stockprice": 120.5,
                "stockvolume": 35170,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-07T00:00:00"),
                "stockopen": 120.5,
                "stockclose": 121.5,
                "stockhigh": 121.5,
                "stocklow": 119.5,
                "stockprice": 121.5,
                "stockvolume": 30079,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-06T00:00:00"),
                "stockopen": 119.0,
                "stockclose": 120.5,
                "stockhigh": 121.5,
                "stocklow": 119.0,
                "stockprice": 120.5,
                "stockvolume": 38043,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-05T00:00:00"),
                "stockopen": 122.5,
                "stockclose": 119.5,
                "stockhigh": 122.5,
                "stocklow": 119.5,
                "stockprice": 119.5,
                "stockvolume": 61536,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-04T00:00:00"),
                "stockopen": 120.0,
                "stockclose": 123.5,
                "stockhigh": 123.5,
                "stocklow": 120.0,
                "stockprice": 123.5,
                "stockvolume": 39730,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-01T00:00:00"),
                "stockopen": 120.0,
                "stockclose": 120.0,
                "stockhigh": 121.0,
                "stocklow": 119.5,
                "stockprice": 120.0,
                "stockvolume": 61873,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-31T00:00:00"),
                "stockopen": 124.0,
                "stockclose": 121.0,
                "stockhigh": 124.0,
                "stocklow": 121.0,
                "stockprice": 121.0,
                "stockvolume": 44806,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-30T00:00:00"),
                "stockopen": 123.5,
                "stockclose": 124.5,
                "stockhigh": 125.0,
                "stocklow": 123.0,
                "stockprice": 124.5,
                "stockvolume": 32428,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-29T00:00:00"),
                "stockopen": 122.5,
                "stockclose": 124.0,
                "stockhigh": 124.0,
                "stocklow": 122.0,
                "stockprice": 124.0,
                "stockvolume": 40749,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-28T00:00:00"),
                "stockopen": 122.0,
                "stockclose": 121.5,
                "stockhigh": 122.5,
                "stocklow": 121.0,
                "stockprice": 121.5,
                "stockvolume": 43514,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-25T00:00:00"),
                "stockopen": 124.5,
                "stockclose": 123.0,
                "stockhigh": 125.0,
                "stocklow": 122.5,
                "stockprice": 123.0,
                "stockvolume": 31609,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-24T00:00:00"),
                "stockopen": 124.5,
                "stockclose": 125.0,
                "stockhigh": 125.0,
                "stocklow": 124.0,
                "stockprice": 125.0,
                "stockvolume": 66041,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-22T00:00:00"),
                "stockopen": 123.5,
                "stockclose": 124.5,
                "stockhigh": 125.0,
                "stocklow": 122.5,
                "stockprice": 124.5,
                "stockvolume": 53307,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-21T00:00:00"),
                "stockopen": 124.0,
                "stockclose": 123.5,
                "stockhigh": 124.5,
                "stocklow": 122.5,
                "stockprice": 123.5,
                "stockvolume": 58994,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-18T00:00:00"),
                "stockopen": 121.5,
                "stockclose": 123.5,
                "stockhigh": 124.0,
                "stocklow": 121.5,
                "stockprice": 123.5,
                "stockvolume": 97366,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-17T00:00:00"),
                "stockopen": 125.0,
                "stockclose": 124.5,
                "stockhigh": 125.5,
                "stocklow": 123.0,
                "stockprice": 124.5,
                "stockvolume": 138665,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-16T00:00:00"),
                "stockopen": 133.0,
                "stockclose": 130.5,
                "stockhigh": 133.5,
                "stocklow": 130.0,
                "stockprice": 130.5,
                "stockvolume": 42072,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-15T00:00:00"),
                "stockopen": 133.0,
                "stockclose": 133.0,
                "stockhigh": 134.0,
                "stocklow": 132.5,
                "stockprice": 133.0,
                "stockvolume": 37976,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-14T00:00:00"),
                "stockopen": 134.5,
                "stockclose": 132.5,
                "stockhigh": 134.5,
                "stocklow": 132.5,
                "stockprice": 132.5,
                "stockvolume": 46818,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-11T00:00:00"),
                "stockopen": 136.0,
                "stockclose": 136.5,
                "stockhigh": 138.0,
                "stocklow": 135.5,
                "stockprice": 136.5,
                "stockvolume": 43513,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-10T00:00:00"),
                "stockopen": 134.5,
                "stockclose": 134.5,
                "stockhigh": 136.0,
                "stocklow": 134.5,
                "stockprice": 134.5,
                "stockvolume": 51132,
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
                result[0].traderprice = 140.0;
                result[0].traderbuyvolume = 2346;
                result[0].tradersellvolume = 2574;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "1470-台灣摩根",
            "stockidnm": "2330-台積電",
            "tradervolume": "4920",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 141.0;
                result[0].traderbuyvolume = 1757;
                result[0].tradersellvolume = 806;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "1520-瑞士信貸",
            "stockidnm": "2330-台積電",
            "tradervolume": "2563",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 140.0;
                result[0].traderbuyvolume = 2953;
                result[0].tradersellvolume = 81;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "8440-摩根大通",
            "stockidnm": "2330-台積電",
            "tradervolume": "3034",
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

