function x(e, t) {
    var n = "9SASji5OWnG41iRKiSvTJHlXHmRySRp1";
    e = e || "";
    var u, a = "", c = t || {}, i = e.split("?");
    if (i.length > 0 && (u = i[1]),
        u) {
        var s = u.split("&")
            , d = "";
        s.forEach((function(e) {
                var t = e.split("=");
                d += "".concat(t[0], "=").concat(encodeURI(t[1]), "&")
            }
        )),
            a = "".concat(r.trimEnd(d, "&"), "&").concat(n)
    } else
        a = Object.keys(c).length > 0 ? "".concat(JSON.stringify(c), "&").concat(n) : "&".concat(n);
    a = a.toLowerCase();
    console.log(a)
    return a
}

 x('/youzy.dms.basiclib.api.college.query',{"keyword":"","provinceNames":[],"natureTypes":[],"eduLevel":"","categories":[],"features":[],"pageIndex":3,"pageSize":20,"sort":7})