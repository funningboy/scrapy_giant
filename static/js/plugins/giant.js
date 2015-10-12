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
