
    function changeTitle(title) {
        var pre = title.prev("div");
        /*切换折叠指示图标*/
        pre.find("span").toggleClass("glyphicon-chevron-down");
        pre.find("span").toggleClass("glyphicon-chevron-right");
        pre.find("div").toggleClass("activeTitle");
        pre.find("div").toggleClass("unactiveTitle");
    }

