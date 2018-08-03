jQuery(function () {
    calc = function () {
        var price = $("#id_单价").val();
        var num = $("#id_图算量").val();
        if (price != null && num != null) {
            $("#id_金额").val((price * num).toFixed(2));
        }
    }
    $('#id_单价').blur(function () {
        calc();
    });
    $('#id_图算量').blur(function () {
        calc();
    })
});
