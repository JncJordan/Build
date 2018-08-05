jQuery(function () {
    calc = function () {
        var price = $("#id_单价").val();
        var num = $("#id_数量").val();
        if (price != null && num != null) {
            $("#id_金额").val((price * num).toFixed(2));
        }
    }
    $('#id_单价').blur(function () {
        calc();
    });
    $('#id_数量').blur(function () {
        calc();
    })
});
