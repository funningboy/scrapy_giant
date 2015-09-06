
function loadChartData(settings) {
    // host:port ...
    var URL = "http://127.0.0.1:8000/handler/api/hisstock_detail/?";
    $.each(settings, function(k, v) {
        if (k == "stockids" || k == "traderids") {
            v = v.join();
        }
        URL = URL + k + "=" + v +"&"
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
            $("#topbuy_piechart").show();
            $("#topsell_piechart").show();
            $("#topmap_columnchart").show();
            $("#credit_columnchart").show();
            $("#future_columnchar").show();
            // auto refresh after time out
            setTimeout(loadChartData, 10*60*1000); 
        },

        success: function (result) {
            try {
                plotTraderData(result);
            } catch(err) {
                console.log("plotTraderData fail");
            }

            try {
                plotCreditData(result);
            } catch(err) {
                console.log("plotCreditData fail");
            }

            try {
                plotFutureData(result);
            } catch(err) {
                console.log("plotFutureData fail");
            }

            try {
                plotTableData(result);
            } catch(err) {
                console.log("plotTableData fail");
            }
        },

        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
            $("#topbuy_piechart").hide();
            $("#topsell_piechart").hide();
            $("#topmap_columnchart").hide();
            $("#credit_columnchart").hide();
            $("future_columnchart").hide();
        }
    });
}



