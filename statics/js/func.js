function animate_ico(isPause = false) {
    if (isPause !== true) {
        $(".glyphicon-refresh").css("animation", "spin 1.5s linear infinite")
        $(".progress").addClass("active")
    }
    $(".glyphicon-play").addClass("glyphicon-stop")
    $(".glyphicon-play").removeClass("glyphicon-play")
    $(".history-ip").addClass("unactive-ip")
    $(".scan-ip").removeClass("unactive-ip")
}


function unanimate_ico() {
    $(".progress").removeClass("active")
    $(".glyphicon-refresh").css("animation", "1")
    $(".glyphicon-stop").addClass("glyphicon-play")
    $(".glyphicon-stop").removeClass("glyphicon-stop")
}

$("[data-toggle='popover']").popover();
$("[data-toggle='popover']").hover(function () {
    $(this).popover('show')
}, function () {
    $(this).popover('hide')
})


function scan() {
    $(".target-ip").html($("#ip").val())
    $(".table").css("display", "")
    $(".progress-bar").css("width", "0")
    animate_ico()
    $("tbody").html("")

}

function scan_over() {
    $(".history-ip").removeClass("unactive-ip")
    $(".scan-ip").addClass("unactive-ip")
    $(".progress").removeClass("active")
}

function reload_process(width, speed = "slow") {
    var n_width = $(".progress").width() * width
    $(".progress-bar").animate({"width": n_width})
}

function stop_process(id) {
    $.ajax({
        url: "/scan/stop/", data: {"id": id}, async: false, success: function (data) {
            unanimate_ico()
            isPause = true
        }
    })
}

            $(".ip-list").click(function () {
                $(".port-range").html($(this).text().split(" ")[0] + "<span style=\"margin-left: 3px\"><b class=\"caret\"></b></span>")
                $("#port").val($(this).attr("id"))
            })
