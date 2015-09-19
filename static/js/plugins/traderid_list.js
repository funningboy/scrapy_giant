//csrf_token
function loadTraderids(settings) {
     // host:port ...
    var URL = "http://127.0.0.1:8000/handler/api/traderid_list/?";
    $.each(settings, function(k, v) {

    });
    console.log(encodeURI(URL));
    // csrf_token
    $.ajax({
        url: encodeURI(URL),
        data: {},
        type: "GET",
        dataType: "json",
        cache: false,

        beforeSend: function() {
        },

        complete: function() {
           // auto refresh after time out
            setTimeout(loadChartData, 10*60*1000); 
        },

        success: function (result) {
            try {
                plotlTableData(result);
            } catch(err) {
                console.log("plotTableData fail");
            }
        },

        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
}