
 var hisstockdetail = function() {
    this.version = '0.1.6';
    this.host = '127.0.0.1';
    this.port = '8000';
    this.settings = {};
    this.URL = 'http://' + this.host + ':' + this.port + '/handler/api/hisstock_detail/?';
    this.data = {};
    this.status = 'idle';
    this.table = {
        chart: {},
        update: false,
        timeout: 10*1000
    };
    this.topbuy = {
        chart: {},
        update: false,
        ready: false,
        timeout: 10*1000
    };
    this.topsell = {
        chart: {},
        update: false,
        ready: false,
        timeout: 10*1000
    };
    this.topmap = {
        chart: {},
        update: false,
        ready: false,
        timeout: 10*1000
    };
    this.future = {
        chart: {},
        update: false,
        timeout: 10*1000
    };
    this.credit = {
        chart: {},
        update: false,
        timeout: 10*1000
    };
};

hisstockdetail.prototype = {

    call_table: function() {
        var self = this;

        var _sync = function(){
            var call_sync = function(self) {
                if (self.status != 'success') {
                    if (self.status == 'error') {
                        return;
                    } 
                    setTimeout(function(){ call_sync(self) }, self.table.timeout); 
                } else {
                    var chart = _plot(_prepare(self.data), _callback);
                    self.table.chart = chart;
                }
            };
            call_sync(self);
        };

        var _prepare = function(data){
            var stockitem = data.stockitem;
            var credititem = data.credititem;
            var futureitem = data.futureitem;
            var item = [];

            try {
                $.each(stockitem[0].datalist, function(d_idx, d_it) {
                    var date = new Date(d_it.date);
                    item.push({
                        'date': yyyymmdd(date),
                        'open': parseFloat(d_it.open.toFixed(2)),
                        'close': parseFloat(d_it.close.toFixed(2)),
                        'high': parseFloat(d_it.high.toFixed(2)),
                        'low': parseFloat(d_it.low.toFixed(2)),
                        'volume': parseInt(d_it.volume.toFixed()),
                        'finarmn' : 0.00,
                        'bearrmn': 0.00,
                        'bfratio': 0.00,
                        'fopen': 0.00,
                        'fclose': 0.00,
                        'fvolume': 0,
                        'event': ''
                    });
                });
            } catch(err) {
                console.log('stockitem None');
            }

            try {
                item = $.extend(true, [], item);
                $.each(credititem[0].datalist, function(d_idx, d_it) {
                    var date = new Date(d_it.date);
                    var rst = $.grep(item, function(e){ return e.date == yyyymmdd(date); });
                    if (rst.length != 0) {
                        rst[0].finarmn = parseFloat(d_it.financeremain.toFixed(2));
                        rst[0].bearrmn = parseFloat(d_it.bearishremain.toFixed(2));
                        rst[0].bfratio = parseFloat(d_it.bearfinaratio.toFixed(2));
                    }
                });
            } catch(err) {
                console.log('credititem None');
            }

            try {
                item = $.extend(true, [], item);
                $.each(futureitem[0].datalist, function(d_idx, d_it) {
                    var date = new Date(d_it.date);
                    var rst = $.grep(item, function(e){ return e.date == yyyymmdd(date); });
                    if (rst.length != 0) {
                        rst[0].fopen = parseFloat(d_it.fopen.toFixed(2));
                        rst[0].fclose = parseFloat(d_it.fclose.toFixed(2));
                        rst[0].fvolume = parseInt(d_it.fvolume.toFixed());
                    }
                });
            } catch(err) {
                console.log('futureitem None');
            }

            return item;
        };

        var _plot = function(item, callback) {
            var chart = $('#stockdetail_table').dynatable({
                dataset: {
                    records: item
                },
                writers: {
                    _rowWriter: _tbody
                }
            }); 

            if (callback) {
                callback(item);
            }
            return chart;
        };

        var _tbody = function(id, item) {
            var stockidnm = item.stockidnm;
            var row = '<tr>' 
            + '<th>' + item.date + '</th>'
            + '<th>' + item.open + '</th>'
            + '<th>' + item.high + '</th>'
            + '<th>' + item.low + '</th>'
            + '<th>' + item.close + '</th>'
            + '<th>' + item.volume + '</th>'
            + '<th>' + item.finarmn + '</th>'
            + '<th>' + item.bearrmn + '</th>'
            + '<th>' + item.bfratio + '</th>'
            + '<th>' + item.fopen + '</th>'
            + '<th>' + item.fclose + '</th>'
            + '<th>' + item.fvolume + '</th>'
            + '<th>' + item.expect + '</th>'
            + '<th>' + item.accuracy + '</th>'
            + '<th>' + item.event + '</th>'
            + '</tr>';
            return row;
        };

        var _callback = function(item) {
        };

        _sync();
    },

    call_future: function() {
        var self = this;

        var _sync = function(){
            var call_sync = function(self) {
                if (self.status != 'success') {
                    if (self.status == 'error') {
                        return;
                    } 
                    setTimeout(function(){ call_sync(self) }, self.future.timeout); 
                } else {
                    var chart = _plot(_prepare(self.data), _callback);
                    self.future.chart = chart;
                }
            };
            call_sync(self);
        };

        var _prepare =  function(data){
            var stockitem = data.stockitem;
            var futureitem = data.futureitem;
            var item = [];

            $.each(stockitem[0].datalist, function(d_idx, d_it) {
                var date = new Date(d_it.date);
                item.push({
                    'date': yyyymmdd(date),
                    'stockopen': parseFloat(d_it.open.toFixed(2)),
                    'stockclose': parseFloat(d_it.close.toFixed(2)),
                    'stockhigh': parseFloat(d_it.high.toFixed(2)),
                    'stocklow': parseFloat(d_it.low.toFixed(2)),
                    'stockprice': parseFloat(d_it.close.toFixed(2)),
                    'stockvolume': parseInt(d_it.volume.toFixed()),
                    'futureopen': 0.00,
                    'futureclose': 0.00,
                    'futurehigh': 0.00,
                    'futurelow': 0.00,
                    'futureprice': 0.00,
                    'futurevolume': 0
                });
            });

            item = $.extend(true, [], item);
            $.each(futureitem[0].datalist, function(d_idx, d_it) {
                var date = new Date(d_it.date);
                var rst = $.grep(item, function(e){ return e.date == yyyymmdd(date); });
                if (rst.length != 0) {
                    rst[0].futureopen = parseFloat(d_it.fopen.toFixed(2));
                    rst[0].futureclose = parseFloat(d_it.fclose.toFixed(2));
                    rst[0].futurehigh = parseFloat(d_it.fhigh.toFixed(2));
                    rst[0].futureclose = parseFloat(d_it.fclose.toFixed(2));
                    rst[0].futureprice = parseFloat(d_it.fclose.toFixed(2));
                    rst[0].futurevolume = parseInt(d_it.fvolume.toFixed());
                }
            });

            return item;
        };

        var _plot = function(cdata) {
            var chart = AmCharts.makeChart('future_columnchart', {
                'type': 'serial',
                'theme': 'dark',
                'colors': ['#7FFFD4', '#008080', '#000080', '#000000'],
                'path': 'http://www.amcharts.com/lib/3/',
                'pathToImages': 'http://www.amcharts.com/lib/3/images/',    
                'dataProvider': cdata,  
                'legend': {
                    'horizontalGap': 10,
                    'maxColumns': 1,
                    'position': 'left',
                    'useGraphSettings': true,
                    'markerSize': 10,
                    'equalWidths': false
                },
                'valueAxes': [{
                    'id': 'volumeAxis',
                    'axisAlpha': 0,
                    'gridAlpha': 0,
                    'position': 'left',
                    'title': 'volume',        
                    'stackType': 'regular'
                }, 
                {
                    'id': 'priceAxis',
                    'axisAlpha': 0,
                    'gridAlpha': 0,
                    'inside': true,
                    'position': 'right',
                    'title': 'price'
                }],
                'graphs': [{
                    'balloonText': '[[value]]',
                    'dashLengthField': 'dashLength',
                    'fillAlphas': 0.7,
                    'legendPeriodValueText': '[[value]]',
                    'legendValueText': 'v: [[value]]',
                    'title': 'futurevolume',
                    'type': 'column',
                    'valueField': 'futurevolume',
                    'valueAxis': 'volumeAxis'
                }, 
                {
                    'balloonText': '[[value]]',
                    'dashLengthField': 'dashLength',
                    'fillAlphas': 0.7,
                    'legendPeriodValueText': '[[value]]',
                    'legendValueText': 'v: [[value]]',
                    'title': 'stockvolume',
                    'type': 'column',
                    'newStack': true, 
                    'valueField': 'stockvolume',
                    'valueAxis': 'volumeAxis'
                },    
                {
                    'balloonText': 'p: [[value]]',
                    'bullet': 'round',
                    'bulletBorderAlpha': 1,
                    'useLineColorForBulletBorder': true,
                    'bulletColor': '#FFFFFF',
                    'bulletSizeField': 'townSize',
                    'dashLengthField': 'dashLength',
                    'descriptionField': 'event',
                    'labelPosition': 'right',
                    'labelText': '[[event]]',
                    'legendValueText': 'p: [[value]]',
                    'title': 'futureprice',
                    'fillAlphas': 0,
                    'valueField': 'futureprice',
                    'valueAxis': 'priceAxis'
                },  
                {
                    'balloonText': 'p: [[value]]',
                    'bullet': 'round',
                    'bulletBorderAlpha': 1,
                    'useLineColorForBulletBorder': true,
                    'bulletColor': '#FFFFFF',
                    'bulletSizeField': 'townSize',
                    'dashLengthField': 'dashLength',
                    'descriptionField': 'event',
                    'labelPosition': 'right',
                    'labelText': '[[event]]',
                    'legendValueText': 'p: [[value]]',
                    'title': 'stockprice',
                    'fillAlphas': 0,
                    'valueField': 'stockprice',
                    'valueAxis': 'priceAxis'
                }], 
                'chartCursor': {
                    'categoryBalloonDateFormat': 'WW',
                    'cursorAlpha': 0.1,
                    'cursorColor':'#000000',
                    'fullWidth':true,
                    'valueBalloonsEnabled': false,
                    'zoomable': false
                },
                'dataDateFormat': 'YYYY-MM-DD', 
                'categoryField': 'date',
                'categoryAxis': {
                    'dateFormats': [{
                        'period': 'DD',
                        'format': 'DD'
                    }, {
                        'period': 'WW',
                        'format': 'MMM DD'
                    }, {
                        'period': 'MM',
                        'format': 'MMM'
                    }, {
                        'period': 'YYYY',
                        'format': 'YYYY'
                    }],
                    'parseDates': true,
                    'autoGridCount': false,
                    'axisColor': '#555555',
                    'gridAlpha': 0.1,
                    'gridColor': '#FFFFFF',
                    'gridCount': 50,
                    'equalSpacing': true
                },
                'connect': false,
                'export': {
                    'enabled': true
                },
                'chartScrollbar': {},  
                'chartCursor': {
                    'cursorPosition': 'mouse'
                }
            });

            return chart;
        };

        var _callback = function(item) {
        };

        _sync();
    },

    call_credit: function() {
        var self = this;

        var _sync = function(){
            var call_sync = function(self) {
                if (self.status != 'success') {
                    if (self.status == 'error') {
                        return;
                    } 
                    setTimeout(function(){ call_sync(self) }, self.credit.timeout); 
                } else {
                    var chart = _plot(_prepare(self.data), _callback);
                    self.credit.chart = chart;
                }
            };
            call_sync(self);
        };

        var _prepare = function(data){
            var stockitem = data.stockitem;
            var credititem = data.credititem;
            var item = [];

            $.each(stockitem[0].datalist, function(d_idx, d_it) {
                var date = new Date(d_it.date);
                item.push({
                    'date': yyyymmdd(date),
                    'stockopen': parseFloat(d_it.open.toFixed(2)),
                    'stockclose': parseFloat(d_it.close.toFixed(2)),
                    'stockhigh': parseFloat(d_it.high.toFixed(2)),
                    'stocklow': parseFloat(d_it.low.toFixed(2)),
                    'stockprice': parseFloat(d_it.close.toFixed(2)),
                    'stockvolume': parseInt(d_it.volume.toFixed()),
                    'finaremain': 0.00,
                    'finabuyvolume': 0.00,
                    'finasellvolume': 0.00,
                    'bearremain': 0.00,
                    'bearbuyvolume': 0.00,
                    'bearsellvolume': 0.00
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
        };
   
        var _plot = function(cdata) {
            var chart = AmCharts.makeChart('credit_columnchart', {
                'type': 'serial',
                'theme': 'dark',
                'colors': ['#5F9EA0', '#7FFFD4', '#20B2AA', '#E0FFFF', '#008080', '#000000'],
                'path': 'http://www.amcharts.com/lib/3/',
                'pathToImages': 'http://www.amcharts.com/lib/3/images/',    
                'dataProvider': cdata,  
                'legend': {
                    'horizontalGap': 10,
                    'maxColumns': 1,
                    'position': 'left',
                    'useGraphSettings': true,
                    'markerSize': 10,
                    'equalWidths': false
                },
                'valueAxes': [{
                    'id': 'volumeAxis',
                    'axisAlpha': 0,
                    'gridAlpha': 0,
                    'position': 'left',
                    'title': 'credit',        
                    'stackType': 'regular'
                }, 
                {
                    'id': 'priceAxis',
                    'axisAlpha': 0,
                    'gridAlpha': 0,
                    'inside': true,
                    'position': 'right',
                    'title': 'price'
                }],
                'graphs': [{
                    'balloonText': '[[value]]',
                    'dashLengthField': 'dashLength',
                    'fillAlphas': 0.7,
                    'legendPeriodValueText': '[[value]]',
                    'legendValueText': 'v: [[value]]',
                    'title': 'finabuyvolume',
                    'type': 'column',
                    'valueField': 'finabuyvolume',
                    'valueAxis': 'volumeAxis'
                },
                {
                    'balloonText': '[[value]]',
                    'dashLengthField': 'dashLength',
                    'fillAlphas': 0.7,
                    'legendPeriodValueText': '[[value]]',
                    'legendValueText': 'v: [[value]]',
                    'title': 'bearsellvolume',
                    'type': 'column',
                    'valueField': 'bearsellvolume',
                    'valueAxis': 'volumeAxis'
                }, 
                {
                    'balloonText': '[[value]]',
                    'dashLengthField': 'dashLength',
                    'fillAlphas': 0.7,
                    'legendPeriodValueText': '[[value]]',
                    'legendValueText': 'v: [[value]]',
                    'title': 'bearbuyvolume',
                    'type': 'column',
                    'newStack': true,
                    'valueField': 'bearbuyvolume',
                    'valueAxis': 'volumeAxis'
                },
                {
                    'balloonText': '[[value]]',
                    'dashLengthField': 'dashLength',
                    'fillAlphas': 0.7,
                    'legendPeriodValueText': '[[value]]',
                    'legendValueText': 'v: [[value]]',
                    'title': 'finasellvolume',
                    'type': 'column',
                    'valueField': 'finasellvolume',
                    'valueAxis': 'volumeAxis'
                }, 
                {
                    'balloonText': '[[value]]',
                    'dashLengthField': 'dashLength',
                    'fillAlphas': 0.7,
                    'legendPeriodValueText': '[[value]]',
                    'legendValueText': 'v: [[value]]',
                    'title': 'stockvolume',
                    'type': 'column',
                    'newStack': true, 
                    'valueField': 'stockvolume',
                    'valueAxis': 'volumeAxis'
                },      
                {
                    'balloonText': 'p: [[value]]',
                    'bullet': 'round',
                    'bulletBorderAlpha': 1,
                    'useLineColorForBulletBorder': true,
                    'bulletColor': '#FFFFFF',
                    'bulletSizeField': 'townSize',
                    'dashLengthField': 'dashLength',
                    'descriptionField': 'event',
                    'labelPosition': 'right',
                    'labelText': '[[event]]',
                    'legendValueText': 'p: [[value]]',
                    'title': 'stockprice',
                    'fillAlphas': 0,
                    'valueField': 'stockprice',
                    'valueAxis': 'priceAxis'
                }], 
                'chartCursor': {
                    'categoryBalloonDateFormat': 'WW',
                    'cursorAlpha': 0.1,
                    'cursorColor':'#000000',
                    'fullWidth':true,
                    'valueBalloonsEnabled': false,
                    'zoomable': false
                },
                'dataDateFormat': 'YYYY-MM-DD', 
                'categoryField': 'date',
                'categoryAxis': {
                    'dateFormats': [{
                        'period': 'DD',
                        'format': 'DD'
                    }, {
                        'period': 'WW',
                        'format': 'MMM DD'
                    }, {
                        'period': 'MM',
                        'format': 'MMM'
                    }, {
                        'period': 'YYYY',
                        'format': 'YYYY'
                    }],
                    'parseDates': true,
                    'autoGridCount': false,
                    'axisColor': '#555555',
                    'gridAlpha': 0.1,
                    'gridColor': '#FFFFFF',
                    'gridCount': 50,
                    'equalSpacing': true
                },
                'connect': false,
                'export': {
                    'enabled': true
                },
                'chartScrollbar': {},  
                'chartCursor': {
                    'cursorPosition': 'mouse'
                }
            });
            return chart;
        };

        var _callback = function(item) {
        };

        _sync();
    },

    call_trader: function(){
        var self = this;
        var pdata = {};
        var coll = {};
        var ready = false;

        var _prepare = function(data) {
            var stockitem = data.stockitem;  
            var traderitem = data.traderitem;
            var index = 0;
            var item = [];
            var pdata = [];

            $.each(stockitem[0].datalist, function(d_idx, d_it) {
                item.push({
                    'date': new Date(d_it.date),
                    'stockopen': parseFloat(d_it.open.toFixed(2)),
                    'stockclose': parseFloat(d_it.close.toFixed(2)),
                    'stockhigh': parseFloat(d_it.high.toFixed(2)),
                    'stocklow': parseFloat(d_it.low.toFixed(2)),
                    'stockprice': parseFloat(d_it.close.toFixed(2)),
                    'stockvolume': parseInt(d_it.volume.toFixed()),
                    'traderavgbuyprice': 0.00,
                    'traderavgsellprice': 0.00,
                    'traderbuyvolume': 0.00,
                    'tradersellvolume': 0.00,
                    'event': ''
                });
            });

            $.each(traderitem, function(t_idx, t_it) {
                item = $.extend(true, [], item);
                $.each(t_it.datalist, function(d_idx, d_it) {
                    var date = new Date(d_it.date);
                    var rst = $.grep(item, function(e){ return e.date.getTime() == date.getTime(); });
                    if (rst.length != 0) {
                        rst[0].traderavgbuyprice = parseFloat(d_it.avgbuyprice.toFixed(2));
                        rst[0].traderavgsellprice = parseFloat(d_it.avgsellprice.toFixed(2));
                        rst[0].traderbuyvolume = parseInt(d_it.buyvolume.toFixed());
                        rst[0].tradersellvolume = parseInt(d_it.sellvolume.toFixed());
                    }
                });

                var unit = {
                      'index': index++,
                      'traderidnm': t_it.traderid + '-' + t_it.tradernm,
                      'stockidnm': t_it.stockid + '-' + t_it.stocknm,
                      'totalbuyvolume': parseInt(t_it.totalbuyvolume.toFixed()),
                      'totalsellvolume': parseInt(t_it.totalsellvolume.toFixed()),
                      'description': '',
                      'data': item
                }
                pdata.push(unit);
            });

            return pdata;
        };

        var _collect = function(pdata){
            // aggregate collective data
            var cdata = []
            for (var x in pdata) {
                var dp = pdata[x];
                if ( 0 == x ) {
                    for (var y in dp.data) {
                        cdata.push({
                            'date': dp.data[y].date,
                            'traderbuyvolume': dp.data[y].traderbuyvolume,
                            'tradersellvolume': dp.data[y].tradersellvolume,
                            'traderavgbuyprice': dp.data[y].traderavgbuyprice * dp.data[y].traderbuyvolume,
                            'traderavgsellprice': dp.data[y].traderavgsellprice * dp.data[y].tradersellvolume,
                            'stockvolume': dp.data[y].stockvolume,
                            'stockprice': dp.data[y].stockprice
                        });
                    }
                }
                else {
                    for (var y in dp.data) {
                        cdata[y].traderbuyvolume += dp.data[y].traderbuyvolume;
                        cdata[y].tradersellvolume += dp.data[y].tradersellvolume;
                        cdata[y].traderavgbuyprice += dp.data[y].traderavgbuyprice * dp.data[y].traderbuyvolume;
                        cdata[y].traderavgsellprice += dp.data[y].traderavgsellprice * dp.data[y].tradersellvolume
                    }
                }
            }
            for (var x in cdata) {
                cdata[x].traderavgbuyprice = Math.floor(cdata[x].traderavgbuyprice / cdata[x].traderbuyvolume);
                cdata[x].traderavgsellprice = Math.floor(cdata[x].traderavgsellprice / cdata[x].tradersellvolume);
            }
            return cdata;
        };

        var _sync_all = function() {
            var call_sync = function(self) {
                if (self.status != 'success') {
                    if (self.status == 'error') {
                        return;
                    } 
                    setTimeout(function(){ call_sync(self) }, 10*1000); 
                } else {
                    pdata = _prepare(self.data);
                    coll = _collect(pdata);
                    ready = true;
                }
            };
            call_sync(self);
        };
        
        var _sync_topsell = function() {
            var call_sync = function(self) {
                if (!ready) {
                    setTimeout(function(){ call_sync(self) }, self.topsell.timeout); 
                } else {
                    var chart = _plot_topsell(pdata, _callback_topsell);
                    self.topsell.chart = chart;
                    self.topsell.ready = true;
                }
            };
            call_sync(self);
        };

        var _plot_topsell = function(pdata) {
            var chart = AmCharts.makeChart('topsell_piechart', {
                'type': 'pie',
                'theme': 'dark',
                'colors': ['#FF0000', '#8B0000', '#B22222', '#DC143C', '#CD5C5C', 
                           '#F08080', '#E98072', '#FRA07A', '#C71585', '#DB7093', 
                           '#FF1493', '#FF69B4', '#FFB6C1', '#FFC0CB', '#FFA500', 
                           '#FFA500', '#FF8C00', '#FF7F50', '#FF6347', '#FF4500'],
                'path': 'http://www.amcharts.com/lib/3/',
                'out': false,
                'dataProvider': pdata,
                'valueField': 'totalsellvolume',
                'titleField': 'traderidnm',
                'labelText': '[[title]]: \n[[value]]',
                'pullOutOnlyOne': true,
                'export': {
                    'enabled': true
                }
            });
            return chart;
        };

        var _callback_topsell = function(item) {
        };

        var _sync_topbuy = function() {
            var call_sync = function(self) {
                if (!ready) {
                    setTimeout(function(){ call_sync(self) }, self.topbuy.timeout); 
                } else {
                    var chart = _plot_topbuy(pdata, _callback_topbuy);
                    self.topbuy.chart = chart;
                    self.topbuy.ready = true;
                }
            };
            call_sync(self);
        };

        var _plot_topbuy = function(pdata) {
            var chart = AmCharts.makeChart('topbuy_piechart', {
                    'type': 'pie',
                    'theme': 'dark',
                    'colors': ['#006400', '#008000', '#228B22', '#2E8B57', '#3CB371', 
                               '#8FBC8F', '#98FB98', '#90EE90', '#00FA9A', '#00FF7F',
                               '#ADFF2F', '#7FFF00', '#7CFC00', '#00FF00', '#32CD32', 
                               '#9ACD32', '#6B8123', '#808000', '#556B2F', '#008B8B'],
                    'path': 'http://www.amcharts.com/lib/3/',
                    'out': false,
                    'dataProvider': pdata,
                    'valueField': 'totalbuyvolume',
                    'titleField': 'traderidnm',
                    'labelText': '[[title]]: \n[[value]]',
                    'pullOutOnlyOne': true,
                    'export': {
                        'enabled': true
                    }
            });
            return chart;
        };

        var _callback_topbuy = function(item) {
        };

        var _sync_topmap = function() {
            var call_sync = function(self) {
                if (!ready) {
                    setTimeout(function(){ call_sync(self) }, self.topmap.timeout); 
                } else {
                    var chart = _plot_topmap(coll, _callback_topmap);
                    self.topmap.chart = chart;
                    self.topmap.ready = true;
                }
            };
            call_sync(self);
        };

        var _plot_topmap = function(cdata) {
            var chart = AmCharts.makeChart('topmap_columnchart', {
                'type': 'serial',
                'theme': 'dark',
                'colors': ['#5F9EA0', '#7FFFD4', '#20B2AA', '#E0FFFF', '#008080', '#000000'],
                'path': 'http://www.amcharts.com/lib/3/',
                'pathToImages': 'http://www.amcharts.com/lib/3/images/', 
                'dataProvider': cdata,  
                'legend': {
                    'horizontalGap': 10,
                    'maxColumns': 1,
                    'position': 'left',
                    'useGraphSettings': true,
                    'markerSize': 10,
                    'equalWidths': false
                },
                'valueAxes': [{
                    'id': 'volumeAxis',
                    'axisAlpha': 0,
                    'gridAlpha': 0,
                    'position': 'left',
                    'title': 'volume',        
                    'stackType': 'regular'
                }, 
                {
                    'id': 'priceAxis',
                    'axisAlpha': 0,
                    'gridAlpha': 0,
                    'inside': true,
                    'position': 'right',
                    'title': 'price'
                }],
                'graphs': [{
                    'balloonText': '[[value]]',
                    'dashLengthField': 'dashLength',
                    'fillAlphas': 0.7,
                    'legendPeriodValueText': '[[value]]',
                    'legendValueText': 'v: [[value]]',
                    'title': 'traderbuyvolume',
                    'type': 'column',
                    'valueField': 'traderbuyvolume',
                    'valueAxis': 'volumeAxis'
                },
                {
                    'balloonText': '[[value]]',
                    'dashLengthField': 'dashLength',
                    'fillAlphas': 0.7,
                    'legendPeriodValueText': '[[value]]',
                    'legendValueText': 'v: [[value]]',
                    'title': 'tradersellvolume',
                    'type': 'column',
                    'valueField': 'tradersellvolume',
                    'valueAxis': 'volumeAxis'
                },  
                {
                    'balloonText': '[[value]]',
                    'dashLengthField': 'dashLength',
                    'fillAlphas': 0.7,
                    'legendPeriodValueText': '[[value]]',
                    'legendValueText': 'v: [[value]]',
                    'title': 'stockvolume',
                    'type': 'column',
                    'newStack': true,
                    'valueField': 'stockvolume',
                    'valueAxis': 'volumeAxis'
                },             
                {
                    'balloonText': 'p:[[value]]',
                    'bullet': 'round',
                    'bulletBorderAlpha': 1,
                    'useLineColorForBulletBorder': true,
                    'bulletColor': '#FFFFFF',
                    'bulletSizeField': 'townSize',
                    'dashLengthField': 'dashLength',
                    'descriptionField': 'event',
                    'labelPosition': 'right',
                    'labelText': '[[event]]',
                    'legendValueText': 'p: [[value]]',
                    'title': 'traderavgbuyprice',
                    'fillAlphas': 0,
                    'valueField': 'traderavgbuyprice',
                    'valueAxis': 'priceAxis'
                },
                {
                    'balloonText': 'p:[[value]]',
                    'bullet': 'round',
                    'bulletBorderAlpha': 1,
                    'useLineColorForBulletBorder': true,
                    'bulletColor': '#FFFFFF',
                    'bulletSizeField': 'townSize',
                    'dashLengthField': 'dashLength',
                    'descriptionField': 'event',
                    'labelPosition': 'right',
                    'labelText': '[[event]]',
                    'legendValueText': 'p: [[value]]',
                    'title': 'traderavgsellprice',
                    'fillAlphas': 0,
                    'valueField': 'traderavgsellprice',
                    'valueAxis': 'priceAxis'
                },
                {
                    'balloonText': 'p: [[value]]',
                    'bullet': 'round',
                    'bulletBorderAlpha': 1,
                    'useLineColorForBulletBorder': true,
                    'bulletColor': '#FFFFFF',
                    'bulletSizeField': 'townSize',
                    'dashLengthField': 'dashLength',
                    'descriptionField': 'event',
                    'labelPosition': 'right',
                    'labelText': '[[event]]',
                    'legendValueText': 'p: [[value]]',
                    'title': 'stockprice',
                    'fillAlphas': 0,
                    'valueField': 'stockprice',
                    'valueAxis': 'priceAxis'
                }], 
                'chartCursor': {
                    'categoryBalloonDateFormat': 'WW',
                    'cursorAlpha': 0.1,
                    'cursorColor':'#000000',
                    'fullWidth':true,
                    'valueBalloonsEnabled': false,
                    'zoomable': false
                },
                'dataDateFormat': 'YYYY-MM-DD', 
                'categoryField': 'date',
                'categoryAxis': {
                    'dateFormats': [{
                        'period': 'DD',
                        'format': 'DD'
                    }, {
                        'period': 'WW',
                        'format': 'MMM DD'
                    }, {
                        'period': 'MM',
                        'format': 'MMM'
                    }, {
                        'period': 'YYYY',
                        'format': 'YYYY'
                    }],
                    'parseDates': true,
                    'autoGridCount': false,
                    'axisColor': '#555555',
                    'gridAlpha': 0.1,
                    'gridColor': '#FFFFFF',
                    'gridCount': 50,
                    'equalSpacing': true
                },
                'connect': false,
                'export': {
                    'enabled': true
                },
                'chartScrollbar': {},  
                'chartCursor': {
                    'cursorPosition': 'mouse'
                }
            });
            return chart;
        };

        var _callback_topmap = function(item) {
        }; 

        var _sync_callback = function(){
            var call_sync = function(self) {
                if (!self.topbuy.ready && !self.topsell.ready && !self.topmap.ready) {
                    setTimeout(function(){ call_sync(self) }, 10*1000); 
                } else {
                    var bchart = self.topbuy.chart;
                    var schart = self.topsell.chart;
                    var mchart = self.topmap.chart;

                    bchart.addListener("pullOutSlice", function (event) {
                        if (bchart.out == true) { 
                            return;
                        }
                        index = event.dataItem.dataContext.index;
                        mchart.dataProvider = event.dataItem.dataContext.data;
                        mchart.validateData();
                        mchart.animateAgain();
                        if (schart.out == false) {
                            schart.out = true;
                            schart.clickSlice(index);
                        }
                        bchart.out = true;
                    });
                    bchart.addListener("pullInSlice", function (event) {
                        if (bchart.out == false) {
                            return;
                        }
                        index = event.dataItem.dataContext.index;
                        mchart.dataProvider = coll;
                        mchart.validateData();
                        mchart.animateAgain();
                        if  (schart.out == true){
                            schart.out = false;
                            schart.clickSlice(index);
                        }
                        bchart.out = false;
                    });
                    schart.addListener("pullOutSlice", function (event) {
                        if (schart.out == true) {
                            return;
                        }
                        index = event.dataItem.dataContext.index;
                        mchart.dataProvider = event.dataItem.dataContext.data;
                        mchart.validateData();
                        mchart.animateAgain();
                        if (bchart.out == false) {
                            bchart.out = true;
                            bchart.clickSlice(index);
                        }
                        schart.out = true;
                    });
                    schart.addListener("pullInSlice", function (event) {
                        if (schart.out == false) {
                            return;
                        }
                        index = event.dataItem.dataContext.index;
                        mchart.dataProvider = coll;
                        mchart.validateData();
                        mchart.animateAgain();
                        if (bchart.out == true){
                            bchart.out = false;
                            bchart.clickSlice(index);
                        }
                        schart.out = false;
                    });
                }
            };
            call_sync(self);
        };

        _sync_all();
        _sync_topsell();
        _sync_topbuy();
        _sync_topmap();
        _sync_callback();
    },

    set: function(settings) {
        var self = this;
        if (JSON.stringify(self.settings) != JSON.stringify(settings)) {
            self.settings = settings;
            self.update = true;
        }
    },

    load: function() {
        var self = this;
        $.ajax({
            url: encodeURI(self.URL),
            data: self.settings,
            type: 'GET',
            dataType: 'json',
            cache: false,
            beforeSend: function() {
                self.status = 'idle';
            },
            success: function (data) { 
                self.data = data;
                console.log(self.data);
                self.status = 'success';
                self.update = false;
            },
            error: function (xhr, ajaxOptions, thrownError) {
                self.status = 'error';
                console.log(xhr.status);
            }
        });
    },  

    run: function() {
        var self = this;
        if (self.update) {
            self.load();
        }
        self.call_table();
        self.call_future();
        self.call_credit();
        self.call_trader();
    }

};

