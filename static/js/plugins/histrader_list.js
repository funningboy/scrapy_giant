
var histraderlist = function(){
    this.version = '0.1.6';
    this.port = '127.0.0.1';
    this.port = '8000';
    this.settings = {};
    this.URL = 'http://' + this.host + ':' + this.port + '/handler/api/histrader_list/?';
    this.data = {};
    this.status = 'idle';
    this.table = {
        chart: {},
        update: false,
        timeout; 10*1000
    };
};

histraderlist.prototype = {

    call_table: function() {
        var self = this;

        var _sync = function() {
            var call_sync = function(self) {
                if (self.status != 'success') {
                    if (self.status == 'error') {
                        return;
                    }
                    setTimeout(function(){ call_sync(self) }, self.table.timeout); 
                } else {
                    _plot(_prepare(self.data), _callback);
                }
            }; 
            call_sync(self);
        };

        var _prepare = function(data) {
            var stockitem = result.stockitem;
            var credititem = result.credititem;
            var futureitem = result.futureitem;
            var traderitem = result.traderitem;
            var item = [];

            try {
                $.each(stockitem, function(s_idx, s_it) {
                    var d_idx = s_it.datalist.length -1;
                    var d_it = s_it.datalist[d_idx];
                    var stockidnm = s_it.stockid + '-' + s_it.stocknm;
                    var date = new Date(d_it.date);
                    item.push({
                        'date': yyyymmdd(date),
                        'stockidnm': stockidnm,
                        'traderidnm': '',
                        'buyrat': 0.00,
                        'sellrat': 0.00,
                        'open': parseFloat(d_it.open.toFixed(2)),
                        'close': parseFloat(d_it.close.toFixed(2)),
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
                console.log('stockidnm None');
            }

            try {
                item = $.extend(true, [], item);
                $.each(traderitem, function(t_idx, t_it) {
                    var d_idx = t_it.datalist.length -1;
                    var d_it = t_it.datalist[d_idx];
                    var date = new Date(d_it.date);
                    var stockidnm = t_it.stockid + '-' + t_it.stocknm;
                    var traderidnm = t_it.traderid + '-' + t_it.tradernm;
                    var rst = $.grep(item, function(e){ return e.date == yyyymmdd(date) && e.stockidnm == stockidnm; });
                    if (rst.length != 0) {
                        rst[0].traderidnm = traderidnm;
                        rst[0].buyrat = parseFloat(d_it.buyratio.toFixed(2));
                        rst[0].sellrat = parseFloat(d_it.sellratio.toFixed(2));
                    }
                });
            } catch(err) {
                console.log('traderitem None');
            }

            try {
                item = $.extend(true, [], item);
                $.each(credititem, function(c_idx, c_it) {
                    var d_idx = c_it.datalist.length -1;
                    var d_it = c_it.datalist[d_idx];
                    var date = new Date(d_it.date);
                    var stockidnm = c_it.stockid + '-' + c_it.stocknm;
                    var rst = $.grep(item, function(e){ return e.date == yyyymmdd(date) && e.stockidnm == stockidnm; });
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
                $.each(futureitem, function(f_idx, f_it) {
                    var d_idx = f_it.datalist.length -1;
                    var d_it = f_it.datalist[d_idx];
                    var date = new Date(d_it.date);
                    var stockidnm = f_it.stockid + '-' + f_it.stocknm;
                    var rst = $.grep(item, function(e){ return e.date == yyyymmdd(date) && e.stockidnm == stockidnm; });
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
            var chart = $('#traderlist_table').dynatable({
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
            + '<th>' 
            + `<class='bpop' id='${item.stockidnm}'>`
            + item.stockidnm
            // popup win
            + `<div class='bpopup' id="${item.stockidnm}_popup" style='display:none'>Content of popup`
            + '<span class="button b-close"><span>X</span></span>'
            + 'If you can\'t get it up use<br/>'
            + '<span class="logo">bPopup</span>'
            + '<span class="button b-close"><span>X</span></span>'
            + '    <div class="panel-body">'
            + '       <ul id="credit_columnchart"></ul>'
            + '    </div>'
            +  '</div>'
            + '</th>'
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
            $.each(item, function(s_idx, s_it) {
                var stockidnm = s_it.stockidnm;
                $(`#${stockidnm}`).click(function(e) {
                    e.preventDefault();
                    $(`#${stockidnm}_popup`).bPopup({
                        contentContainer:'.content',
                    });
                });
            });
        };
        
        _sync();
    },

    set: function(settings) {
        var self = this;
        if (JSON.stringify(self.settings) != JSON.stringify(settings)) {
            self.settings = settings;
            self.update = true;
        }
    },

    load: function(callback) {
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
                self.status = 'success';
                self.update = false;
            },
            error: function (xhr, ajaxOptions, thrownError) {
                self.status = 'error';
                console.log(xhr.status);
            }
        });
    },

    run: function(){
        var self = this;
        if (self.update) {
            self.load();
        }
        self.call_table();
    }

};