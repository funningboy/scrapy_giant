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
                "stockopen": 2440.0,
                "stockclose": 2375.0,
                "stockhigh": 2475.0,
                "stocklow": 2370.0,
                "stockprice": 2375.0,
                "stockvolume": 1411,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-26T00:00:00"),
                "stockopen": 2385.0,
                "stockclose": 2425.0,
                "stockhigh": 2440.0,
                "stocklow": 2365.0,
                "stockprice": 2425.0,
                "stockvolume": 1772,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-25T00:00:00"),
                "stockopen": 2320.0,
                "stockclose": 2385.0,
                "stockhigh": 2385.0,
                "stocklow": 2295.0,
                "stockprice": 2385.0,
                "stockvolume": 1086,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-24T00:00:00"),
                "stockopen": 2355.0,
                "stockclose": 2305.0,
                "stockhigh": 2385.0,
                "stocklow": 2305.0,
                "stockprice": 2305.0,
                "stockvolume": 1030,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-21T00:00:00"),
                "stockopen": 2360.0,
                "stockclose": 2335.0,
                "stockhigh": 2365.0,
                "stocklow": 2295.0,
                "stockprice": 2335.0,
                "stockvolume": 1342,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-20T00:00:00"),
                "stockopen": 2215.0,
                "stockclose": 2340.0,
                "stockhigh": 2340.0,
                "stocklow": 2215.0,
                "stockprice": 2340.0,
                "stockvolume": 2483,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-19T00:00:00"),
                "stockopen": 2150.0,
                "stockclose": 2190.0,
                "stockhigh": 2220.0,
                "stocklow": 2125.0,
                "stockprice": 2190.0,
                "stockvolume": 1731,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-18T00:00:00"),
                "stockopen": 2130.0,
                "stockclose": 2130.0,
                "stockhigh": 2140.0,
                "stocklow": 2110.0,
                "stockprice": 2130.0,
                "stockvolume": 564,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-17T00:00:00"),
                "stockopen": 2160.0,
                "stockclose": 2115.0,
                "stockhigh": 2160.0,
                "stocklow": 2105.0,
                "stockprice": 2115.0,
                "stockvolume": 605,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-14T00:00:00"),
                "stockopen": 2145.0,
                "stockclose": 2125.0,
                "stockhigh": 2160.0,
                "stocklow": 2110.0,
                "stockprice": 2125.0,
                "stockvolume": 978,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-13T00:00:00"),
                "stockopen": 2085.0,
                "stockclose": 2120.0,
                "stockhigh": 2145.0,
                "stocklow": 2085.0,
                "stockprice": 2120.0,
                "stockvolume": 1539,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-12T00:00:00"),
                "stockopen": 2115.0,
                "stockclose": 2080.0,
                "stockhigh": 2130.0,
                "stocklow": 2035.0,
                "stockprice": 2080.0,
                "stockvolume": 1465,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-11T00:00:00"),
                "stockopen": 2140.0,
                "stockclose": 2120.0,
                "stockhigh": 2170.0,
                "stocklow": 2100.0,
                "stockprice": 2120.0,
                "stockvolume": 1188,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-10T00:00:00"),
                "stockopen": 2155.0,
                "stockclose": 2115.0,
                "stockhigh": 2220.0,
                "stocklow": 2110.0,
                "stockprice": 2115.0,
                "stockvolume": 1513,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-07T00:00:00"),
                "stockopen": 2015.0,
                "stockclose": 2145.0,
                "stockhigh": 2150.0,
                "stocklow": 2015.0,
                "stockprice": 2145.0,
                "stockvolume": 1652,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-06T00:00:00"),
                "stockopen": 2125.0,
                "stockclose": 2010.0,
                "stockhigh": 2140.0,
                "stocklow": 2005.0,
                "stockprice": 2010.0,
                "stockvolume": 1808,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-05T00:00:00"),
                "stockopen": 2190.0,
                "stockclose": 2085.0,
                "stockhigh": 2190.0,
                "stocklow": 2080.0,
                "stockprice": 2085.0,
                "stockvolume": 1157,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-04T00:00:00"),
                "stockopen": 2210.0,
                "stockclose": 2160.0,
                "stockhigh": 2230.0,
                "stocklow": 2160.0,
                "stockprice": 2160.0,
                "stockvolume": 1535,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-11-03T00:00:00"),
                "stockopen": 2155.0,
                "stockclose": 2210.0,
                "stockhigh": 2230.0,
                "stocklow": 2140.0,
                "stockprice": 2210.0,
                "stockvolume": 1289,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-31T00:00:00"),
                "stockopen": 2115.0,
                "stockclose": 2135.0,
                "stockhigh": 2145.0,
                "stocklow": 2115.0,
                "stockprice": 2135.0,
                "stockvolume": 847,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-30T00:00:00"),
                "stockopen": 2120.0,
                "stockclose": 2095.0,
                "stockhigh": 2125.0,
                "stocklow": 2085.0,
                "stockprice": 2095.0,
                "stockvolume": 939,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-29T00:00:00"),
                "stockopen": 2100.0,
                "stockclose": 2120.0,
                "stockhigh": 2160.0,
                "stocklow": 2085.0,
                "stockprice": 2120.0,
                "stockvolume": 1683,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-28T00:00:00"),
                "stockopen": 1995.0,
                "stockclose": 2080.0,
                "stockhigh": 2085.0,
                "stocklow": 1935.0,
                "stockprice": 2080.0,
                "stockvolume": 2184,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-27T00:00:00"),
                "stockopen": 2050.0,
                "stockclose": 1950.0,
                "stockhigh": 2060.0,
                "stocklow": 1950.0,
                "stockprice": 1950.0,
                "stockvolume": 1979,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-24T00:00:00"),
                "stockopen": 2050.0,
                "stockclose": 2030.0,
                "stockhigh": 2065.0,
                "stocklow": 2005.0,
                "stockprice": 2030.0,
                "stockvolume": 1334,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-23T00:00:00"),
                "stockopen": 2025.0,
                "stockclose": 2025.0,
                "stockhigh": 2105.0,
                "stocklow": 2010.0,
                "stockprice": 2025.0,
                "stockvolume": 1998,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-22T00:00:00"),
                "stockopen": 2200.0,
                "stockclose": 2050.0,
                "stockhigh": 2215.0,
                "stocklow": 2050.0,
                "stockprice": 2050.0,
                "stockvolume": 2197,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-21T00:00:00"),
                "stockopen": 2160.0,
                "stockclose": 2150.0,
                "stockhigh": 2200.0,
                "stocklow": 2110.0,
                "stockprice": 2150.0,
                "stockvolume": 1263,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-20T00:00:00"),
                "stockopen": 2200.0,
                "stockclose": 2155.0,
                "stockhigh": 2200.0,
                "stocklow": 2060.0,
                "stockprice": 2155.0,
                "stockvolume": 2527,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-17T00:00:00"),
                "stockopen": 2295.0,
                "stockclose": 2160.0,
                "stockhigh": 2295.0,
                "stocklow": 2160.0,
                "stockprice": 2160.0,
                "stockvolume": 2603,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-16T00:00:00"),
                "stockopen": 2215.0,
                "stockclose": 2320.0,
                "stockhigh": 2325.0,
                "stocklow": 2160.0,
                "stockprice": 2320.0,
                "stockvolume": 1833,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-15T00:00:00"),
                "stockopen": 2275.0,
                "stockclose": 2215.0,
                "stockhigh": 2305.0,
                "stocklow": 2135.0,
                "stockprice": 2215.0,
                "stockvolume": 2063,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-14T00:00:00"),
                "stockopen": 2280.0,
                "stockclose": 2275.0,
                "stockhigh": 2330.0,
                "stocklow": 2270.0,
                "stockprice": 2275.0,
                "stockvolume": 988,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-13T00:00:00"),
                "stockopen": 2220.0,
                "stockclose": 2275.0,
                "stockhigh": 2295.0,
                "stocklow": 2210.0,
                "stockprice": 2275.0,
                "stockvolume": 1114,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-09T00:00:00"),
                "stockopen": 2350.0,
                "stockclose": 2275.0,
                "stockhigh": 2360.0,
                "stocklow": 2275.0,
                "stockprice": 2275.0,
                "stockvolume": 1100,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-08T00:00:00"),
                "stockopen": 2300.0,
                "stockclose": 2275.0,
                "stockhigh": 2365.0,
                "stocklow": 2275.0,
                "stockprice": 2275.0,
                "stockvolume": 1191,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-07T00:00:00"),
                "stockopen": 2370.0,
                "stockclose": 2305.0,
                "stockhigh": 2375.0,
                "stocklow": 2290.0,
                "stockprice": 2305.0,
                "stockvolume": 1288,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-06T00:00:00"),
                "stockopen": 2420.0,
                "stockclose": 2370.0,
                "stockhigh": 2450.0,
                "stocklow": 2370.0,
                "stockprice": 2370.0,
                "stockvolume": 1565,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-03T00:00:00"),
                "stockopen": 2315.0,
                "stockclose": 2390.0,
                "stockhigh": 2420.0,
                "stocklow": 2315.0,
                "stockprice": 2390.0,
                "stockvolume": 1857,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-02T00:00:00"),
                "stockopen": 2195.0,
                "stockclose": 2270.0,
                "stockhigh": 2275.0,
                "stocklow": 2185.0,
                "stockprice": 2270.0,
                "stockvolume": 1083,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-10-01T00:00:00"),
                "stockopen": 2180.0,
                "stockclose": 2210.0,
                "stockhigh": 2275.0,
                "stocklow": 2160.0,
                "stockprice": 2210.0,
                "stockvolume": 1535,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-30T00:00:00"),
                "stockopen": 2235.0,
                "stockclose": 2180.0,
                "stockhigh": 2240.0,
                "stocklow": 2125.0,
                "stockprice": 2180.0,
                "stockvolume": 1549,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-29T00:00:00"),
                "stockopen": 2110.0,
                "stockclose": 2230.0,
                "stockhigh": 2235.0,
                "stocklow": 2070.0,
                "stockprice": 2230.0,
                "stockvolume": 1801,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-26T00:00:00"),
                "stockopen": 2060.0,
                "stockclose": 2090.0,
                "stockhigh": 2095.0,
                "stocklow": 1985.0,
                "stockprice": 2090.0,
                "stockvolume": 2108,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-25T00:00:00"),
                "stockopen": 2290.0,
                "stockclose": 2110.0,
                "stockhigh": 2320.0,
                "stocklow": 2110.0,
                "stockprice": 2110.0,
                "stockvolume": 1678,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-24T00:00:00"),
                "stockopen": 2280.0,
                "stockclose": 2265.0,
                "stockhigh": 2335.0,
                "stocklow": 2260.0,
                "stockprice": 2265.0,
                "stockvolume": 769,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-23T00:00:00"),
                "stockopen": 2320.0,
                "stockclose": 2280.0,
                "stockhigh": 2350.0,
                "stocklow": 2280.0,
                "stockprice": 2280.0,
                "stockvolume": 767,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-22T00:00:00"),
                "stockopen": 2385.0,
                "stockclose": 2340.0,
                "stockhigh": 2390.0,
                "stocklow": 2330.0,
                "stockprice": 2340.0,
                "stockvolume": 681,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-19T00:00:00"),
                "stockopen": 2375.0,
                "stockclose": 2400.0,
                "stockhigh": 2400.0,
                "stocklow": 2360.0,
                "stockprice": 2400.0,
                "stockvolume": 686,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-18T00:00:00"),
                "stockopen": 2365.0,
                "stockclose": 2360.0,
                "stockhigh": 2375.0,
                "stocklow": 2325.0,
                "stockprice": 2360.0,
                "stockvolume": 753,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-17T00:00:00"),
                "stockopen": 2270.0,
                "stockclose": 2350.0,
                "stockhigh": 2375.0,
                "stocklow": 2270.0,
                "stockprice": 2350.0,
                "stockvolume": 1302,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-16T00:00:00"),
                "stockopen": 2290.0,
                "stockclose": 2255.0,
                "stockhigh": 2310.0,
                "stocklow": 2255.0,
                "stockprice": 2255.0,
                "stockvolume": 697,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-15T00:00:00"),
                "stockopen": 2250.0,
                "stockclose": 2280.0,
                "stockhigh": 2310.0,
                "stocklow": 2250.0,
                "stockprice": 2280.0,
                "stockvolume": 1499,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-12T00:00:00"),
                "stockopen": 2385.0,
                "stockclose": 2250.0,
                "stockhigh": 2385.0,
                "stocklow": 2235.0,
                "stockprice": 2250.0,
                "stockvolume": 2059,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-11T00:00:00"),
                "stockopen": 2470.0,
                "stockclose": 2400.0,
                "stockhigh": 2470.0,
                "stocklow": 2400.0,
                "stockprice": 2400.0,
                "stockvolume": 501,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-10T00:00:00"),
                "stockopen": 2435.0,
                "stockclose": 2445.0,
                "stockhigh": 2445.0,
                "stocklow": 2405.0,
                "stockprice": 2445.0,
                "stockvolume": 507,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-09T00:00:00"),
                "stockopen": 2480.0,
                "stockclose": 2440.0,
                "stockhigh": 2490.0,
                "stocklow": 2425.0,
                "stockprice": 2440.0,
                "stockvolume": 756,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-05T00:00:00"),
                "stockopen": 2460.0,
                "stockclose": 2415.0,
                "stockhigh": 2465.0,
                "stocklow": 2390.0,
                "stockprice": 2415.0,
                "stockvolume": 958,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-04T00:00:00"),
                "stockopen": 2385.0,
                "stockclose": 2450.0,
                "stockhigh": 2450.0,
                "stocklow": 2355.0,
                "stockprice": 2450.0,
                "stockvolume": 789,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-03T00:00:00"),
                "stockopen": 2430.0,
                "stockclose": 2405.0,
                "stockhigh": 2465.0,
                "stocklow": 2385.0,
                "stockprice": 2405.0,
                "stockvolume": 911,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-02T00:00:00"),
                "stockopen": 2525.0,
                "stockclose": 2405.0,
                "stockhigh": 2525.0,
                "stocklow": 2405.0,
                "stockprice": 2405.0,
                "stockvolume": 983,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-09-01T00:00:00"),
                "stockopen": 2495.0,
                "stockclose": 2510.0,
                "stockhigh": 2540.0,
                "stocklow": 2495.0,
                "stockprice": 2510.0,
                "stockvolume": 449,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-29T00:00:00"),
                "stockopen": 2525.0,
                "stockclose": 2475.0,
                "stockhigh": 2525.0,
                "stocklow": 2465.0,
                "stockprice": 2475.0,
                "stockvolume": 679,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-28T00:00:00"),
                "stockopen": 2550.0,
                "stockclose": 2515.0,
                "stockhigh": 2565.0,
                "stocklow": 2500.0,
                "stockprice": 2515.0,
                "stockvolume": 617,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-27T00:00:00"),
                "stockopen": 2565.0,
                "stockclose": 2540.0,
                "stockhigh": 2605.0,
                "stocklow": 2520.0,
                "stockprice": 2540.0,
                "stockvolume": 925,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-26T00:00:00"),
                "stockopen": 2460.0,
                "stockclose": 2550.0,
                "stockhigh": 2570.0,
                "stocklow": 2460.0,
                "stockprice": 2550.0,
                "stockvolume": 1279,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-25T00:00:00"),
                "stockopen": 2460.0,
                "stockclose": 2460.0,
                "stockhigh": 2465.0,
                "stocklow": 2435.0,
                "stockprice": 2460.0,
                "stockvolume": 401,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-22T00:00:00"),
                "stockopen": 2410.0,
                "stockclose": 2450.0,
                "stockhigh": 2475.0,
                "stocklow": 2410.0,
                "stockprice": 2450.0,
                "stockvolume": 759,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-21T00:00:00"),
                "stockopen": 2410.0,
                "stockclose": 2385.0,
                "stockhigh": 2425.0,
                "stocklow": 2380.0,
                "stockprice": 2385.0,
                "stockvolume": 634,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-20T00:00:00"),
                "stockopen": 2465.0,
                "stockclose": 2440.0,
                "stockhigh": 2480.0,
                "stocklow": 2425.0,
                "stockprice": 2440.0,
                "stockvolume": 695,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-19T00:00:00"),
                "stockopen": 2415.0,
                "stockclose": 2460.0,
                "stockhigh": 2480.0,
                "stocklow": 2415.0,
                "stockprice": 2460.0,
                "stockvolume": 780,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-18T00:00:00"),
                "stockopen": 2445.0,
                "stockclose": 2395.0,
                "stockhigh": 2455.0,
                "stocklow": 2385.0,
                "stockprice": 2395.0,
                "stockvolume": 309,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-15T00:00:00"),
                "stockopen": 2405.0,
                "stockclose": 2445.0,
                "stockhigh": 2445.0,
                "stocklow": 2400.0,
                "stockprice": 2445.0,
                "stockvolume": 608,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-14T00:00:00"),
                "stockopen": 2460.0,
                "stockclose": 2395.0,
                "stockhigh": 2460.0,
                "stocklow": 2390.0,
                "stockprice": 2395.0,
                "stockvolume": 521,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-13T00:00:00"),
                "stockopen": 2435.0,
                "stockclose": 2425.0,
                "stockhigh": 2465.0,
                "stocklow": 2425.0,
                "stockprice": 2425.0,
                "stockvolume": 545,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-12T00:00:00"),
                "stockopen": 2440.0,
                "stockclose": 2430.0,
                "stockhigh": 2450.0,
                "stocklow": 2420.0,
                "stockprice": 2430.0,
                "stockvolume": 864,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-11T00:00:00"),
                "stockopen": 2390.0,
                "stockclose": 2435.0,
                "stockhigh": 2445.0,
                "stocklow": 2355.0,
                "stockprice": 2435.0,
                "stockvolume": 1293,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-08T00:00:00"),
                "stockopen": 2300.0,
                "stockclose": 2390.0,
                "stockhigh": 2390.0,
                "stocklow": 2250.0,
                "stockprice": 2390.0,
                "stockvolume": 1258,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-07T00:00:00"),
                "stockopen": 2345.0,
                "stockclose": 2280.0,
                "stockhigh": 2380.0,
                "stocklow": 2275.0,
                "stockprice": 2280.0,
                "stockvolume": 751,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-06T00:00:00"),
                "stockopen": 2350.0,
                "stockclose": 2325.0,
                "stockhigh": 2360.0,
                "stocklow": 2235.0,
                "stockprice": 2325.0,
                "stockvolume": 1341,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-05T00:00:00"),
                "stockopen": 2400.0,
                "stockclose": 2310.0,
                "stockhigh": 2430.0,
                "stocklow": 2280.0,
                "stockprice": 2310.0,
                "stockvolume": 1350,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-04T00:00:00"),
                "stockopen": 2345.0,
                "stockclose": 2400.0,
                "stockhigh": 2400.0,
                "stocklow": 2325.0,
                "stockprice": 2400.0,
                "stockvolume": 818,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-08-01T00:00:00"),
                "stockopen": 2265.0,
                "stockclose": 2325.0,
                "stockhigh": 2340.0,
                "stocklow": 2265.0,
                "stockprice": 2325.0,
                "stockvolume": 824,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-31T00:00:00"),
                "stockopen": 2350.0,
                "stockclose": 2330.0,
                "stockhigh": 2360.0,
                "stocklow": 2315.0,
                "stockprice": 2330.0,
                "stockvolume": 815,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-30T00:00:00"),
                "stockopen": 2330.0,
                "stockclose": 2345.0,
                "stockhigh": 2360.0,
                "stocklow": 2305.0,
                "stockprice": 2345.0,
                "stockvolume": 891,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-29T00:00:00"),
                "stockopen": 2325.0,
                "stockclose": 2310.0,
                "stockhigh": 2350.0,
                "stocklow": 2265.0,
                "stockprice": 2310.0,
                "stockvolume": 1377,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-28T00:00:00"),
                "stockopen": 2255.0,
                "stockclose": 2255.0,
                "stockhigh": 2350.0,
                "stocklow": 2220.0,
                "stockprice": 2255.0,
                "stockvolume": 1555,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-25T00:00:00"),
                "stockopen": 2465.0,
                "stockclose": 2300.0,
                "stockhigh": 2500.0,
                "stocklow": 2300.0,
                "stockprice": 2300.0,
                "stockvolume": 2025,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-24T00:00:00"),
                "stockopen": 2540.0,
                "stockclose": 2470.0,
                "stockhigh": 2560.0,
                "stocklow": 2460.0,
                "stockprice": 2470.0,
                "stockvolume": 913,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-22T00:00:00"),
                "stockopen": 2500.0,
                "stockclose": 2495.0,
                "stockhigh": 2520.0,
                "stocklow": 2475.0,
                "stockprice": 2495.0,
                "stockvolume": 733,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-21T00:00:00"),
                "stockopen": 2470.0,
                "stockclose": 2510.0,
                "stockhigh": 2530.0,
                "stocklow": 2440.0,
                "stockprice": 2510.0,
                "stockvolume": 1285,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-18T00:00:00"),
                "stockopen": 2480.0,
                "stockclose": 2380.0,
                "stockhigh": 2480.0,
                "stocklow": 2380.0,
                "stockprice": 2380.0,
                "stockvolume": 2155,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-17T00:00:00"),
                "stockopen": 2630.0,
                "stockclose": 2530.0,
                "stockhigh": 2630.0,
                "stocklow": 2465.0,
                "stockprice": 2530.0,
                "stockvolume": 1566,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-16T00:00:00"),
                "stockopen": 2590.0,
                "stockclose": 2635.0,
                "stockhigh": 2640.0,
                "stocklow": 2565.0,
                "stockprice": 2635.0,
                "stockvolume": 938,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-15T00:00:00"),
                "stockopen": 2565.0,
                "stockclose": 2570.0,
                "stockhigh": 2610.0,
                "stocklow": 2560.0,
                "stockprice": 2570.0,
                "stockvolume": 900,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-14T00:00:00"),
                "stockopen": 2505.0,
                "stockclose": 2560.0,
                "stockhigh": 2560.0,
                "stocklow": 2505.0,
                "stockprice": 2560.0,
                "stockvolume": 814,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-11T00:00:00"),
                "stockopen": 2475.0,
                "stockclose": 2495.0,
                "stockhigh": 2555.0,
                "stocklow": 2445.0,
                "stockprice": 2495.0,
                "stockvolume": 1331,
                "traderprice": 0,
                "traderbuyvolume": 0,
                "tradersellvolume": 0,
                "event": ""
            });
        
		    data.unshift({
                "date": new Date("2014-07-10T00:00:00"),
                "stockopen": 2395.0,
                "stockclose": 2480.0,
                "stockhigh": 2490.0,
                "stocklow": 2395.0,
                "stockprice": 2480.0,
                "stockvolume": 1447,
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
                result[0].traderprice = 2375.0;
                result[0].traderbuyvolume = 16;
                result[0].tradersellvolume = 3;
            } else {
                
            }
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2375.0;
                result[0].traderbuyvolume = 4;
                result[0].tradersellvolume = 5;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "1520-瑞士信貸",
            "stockidnm": "3008-大立光",
            "tradervolume": "28",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2415.0;
                result[0].traderbuyvolume = 5;
                result[0].tradersellvolume = 0;
            } else {
                
            }
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2375.0;
                result[0].traderbuyvolume = 6;
                result[0].tradersellvolume = 0;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "1590-花旗環球",
            "stockidnm": "3008-大立光",
            "tradervolume": "11",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2380.0;
                result[0].traderbuyvolume = 0;
                result[0].tradersellvolume = 4;
            } else {
                
            }
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2380.0;
                result[0].traderbuyvolume = 5;
                result[0].tradersellvolume = 7;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "538E-第一自由",
            "stockidnm": "3008-大立光",
            "tradervolume": "16",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2425.0;
                result[0].traderbuyvolume = 5;
                result[0].tradersellvolume = 0;
            } else {
                
            }
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2390.0;
                result[0].traderbuyvolume = 5;
                result[0].tradersellvolume = 0;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "585h-統一新桃",
            "stockidnm": "3008-大立光",
            "tradervolume": "10",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2375.0;
                result[0].traderbuyvolume = 0;
                result[0].tradersellvolume = 8;
            } else {
                
            }
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2385.0;
                result[0].traderbuyvolume = 6;
                result[0].tradersellvolume = 1;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "5920-元富",
            "stockidnm": "3008-大立光",
            "tradervolume": "15",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2420.0;
                result[0].traderbuyvolume = 0;
                result[0].tradersellvolume = 10;
            } else {
                
            }
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2385.0;
                result[0].traderbuyvolume = 2;
                result[0].tradersellvolume = 0;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "9200-凱基",
            "stockidnm": "3008-大立光",
            "tradervolume": "12",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2385.0;
                result[0].traderbuyvolume = 3;
                result[0].tradersellvolume = 0;
            } else {
                
            }
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2380.0;
                result[0].traderbuyvolume = 7;
                result[0].tradersellvolume = 0;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "9600-富邦",
            "stockidnm": "3008-大立光",
            "tradervolume": "10",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2375.0;
                result[0].traderbuyvolume = 1;
                result[0].tradersellvolume = 0;
            } else {
                
            }
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2385.0;
                result[0].traderbuyvolume = 14;
                result[0].tradersellvolume = 0;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "9663-富邦敦南",
            "stockidnm": "3008-大立光",
            "tradervolume": "15",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2420.0;
                result[0].traderbuyvolume = 6;
                result[0].tradersellvolume = 0;
            } else {
                
            }
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2380.0;
                result[0].traderbuyvolume = 2;
                result[0].tradersellvolume = 3;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "9A9K-永豐三重",
            "stockidnm": "3008-大立光",
            "tradervolume": "11",
            "url": "",
            "description": "",
            "data": ndata
        }
        chartData.push(unit);
    
        var ndata = jQuery.extend(true, [], data);
        
            var date = new Date("2014-11-27T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2410.0;
                result[0].traderbuyvolume = 13;
                result[0].tradersellvolume = 0;
            } else {
                
            }
        
            var date = new Date("2014-11-26T00:00:00");
            var result = jQuery.grep(ndata, function(e){ return e.date.getTime() == date.getTime(); });
            if (result.length != 0) {
                result[0].traderprice = 2370.0;
                result[0].traderbuyvolume = 0;
                result[0].tradersellvolume = 3;
            } else {
                
            }
        
        var unit = {
            "traderidnm": "9A9S-永豐南京",
            "stockidnm": "3008-大立光",
            "tradervolume": "16",
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

