var CryptoJS = require("crypto-js");

function getFromData(loginName,password){
    var skey='3c5ad16dbc06cd16ae1fd3344d87f16b';
    var set ={};
    var _t =Date.now();
    var cookie_cid_sid=getCookieCidSid();
    set.data = {api_key: "70f71280d5d547b2a7bb370a529aeea1",
    captchaId: "",
    captchaTicket: "",
    loginName:loginName,
//    password: "e10adc3949ba59abbe56e057f20f883e",
    password:password,
    remUser: 0,
    whereFrom: "",
    _t: _t}
    var vipParamsEncrypt = {
        data: {
            secret: {
                "3c5ad16dbc06cd16ae1fd3344d87f16b": "U2FsdGVkX1/f3zYuiRoYm9vb5Z9R2sDcnm/4rC23IgvW9E8as+kKYw1cSmpBB0eFUycxirbwr17ynjGWr7QAyg=="
            },
            aes: {
                secret: "qyrohlf5sjazleru"
            }
        },
        encrypt: function(skey, params, pc_eversion) {
            var _this = this;
            if (!skey || !params)
                return;
            if (typeof params === "object") {
                var arr = [];
                for (var i in params) {
                    if (params[i] === undefined || params[i] === null)
                        params[i] = "";
                    arr.push(i + "=" + encodeURIComponent(params[i]))
                }
                params = arr.join("&")
            }
            var iv = CryptoJS.lib.WordArray.random(16);
            var secret = _this.data.secret[skey] ? _this.data.secret[skey] : "";
            secret = _this.aesDecrypt(secret, _this.data.aes.secret);
            var key = CryptoJS.MD5(secret);
            var encrypted = CryptoJS.AES.encrypt(params, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            var output = CryptoJS.lib.WordArray.create(iv.words.slice(0));
            output.concat(encrypted.ciphertext);
            var edata = output.toString(CryptoJS.enc.Base64);
            return edata
        },
        aesEncrypt: function(msg, secret) {
            return CryptoJS.AES.encrypt(msg, secret).toString()
        },
        aesDecrypt: function(msg, secret) {
            var bytes = CryptoJS.AES.decrypt(msg, secret);
            return bytes.toString(CryptoJS.enc.Utf8)
        }
    };
    var sign = {
                data: {
                    "secret": "qyrohlf5sjazleru",
                    "enString": {
                        "70f71280d5d547b2a7bb370a529aeea1": "U2FsdGVkX197SM3Eh62XyjAwTXznW9DdALdNR1gKNsewAg3fzwA0x/+UQldlbi3oYBn8eFHgTtBUcGneYPCjIA==",
                        "8cec5243ade04ed3a02c5972bcda0d3f": "U2FsdGVkX1+ZmG8rT/n9qDbrWBnK0K3G0gsoPo0N6/6qx8AklnZmXLyulj0KAy07ixFAu6oMKmOY0+VH3DjQ2Q==",
                        "adf779847ac641dd9590ccc5674e25d2": "U2FsdGVkX1/VI+95aRUsSZCDB3rmMe2DPSUO+rSH7U/tlNnA5u9anTM3oHI+XgIeHWA5XDAo0Z19ddwzFeHFXA=="
                    }
                },
                getSign: function(url, param, cookie) {
                    var rs = "";
                    var _this = this;
                    var api = _this.replaceHost(url);
                    var hashParam = _this.hashParam(param, url);
    //                var cid = _this.getCookie("mars_cid") ? _this.getCookie("mars_cid") : "";
    //                var sid = _this.getCookie("mars_sid") ? _this.getCookie("mars_sid") : "";
                    var cid =cookie_cid_sid[0];
                    var sid = cookie_cid_sid[1];
                    var secret = _this.getSecret(param);
                    rs = this.sha1(api + hashParam + sid + cid + secret);
                    rs = "OAuth api_sign=" + rs;
                    return rs
                },
                replaceHost: function(url) {
                    if (url) {
                        url = url.replace(/^http:\/\/[^\/]*/, "");
                        url = url.replace(/^https:\/\/[^\/]*/, "");
                        url = url.replace(/^\/\/[^\/]*/, "")
                    }
                    return url
                },
                hashParam: function(param, url) {
                    var rs = "";
                    var keyAry = [];
                    if (url && url.indexOf("?") != -1) {
                        url = url.split("?")[1];
                        if (url.indexOf("#") != -1)
                            url = url.split("#")[0];
                        var aryUrl = url.split("&");
                        for (var i in aryUrl) {
                            var arySplit = aryUrl[i].split("=");
                            param[arySplit[0]] = arySplit[1] ? arySplit[1] : ""
                        }
                    }
                    for (var i in param)
                        keyAry.push(i);
                    keyAry = keyAry.sort();
                    for (var j in keyAry) {
                        if (keyAry[j] == "api_key")
                            continue;
                        rs += "&" + keyAry[j] + "=" + (param[keyAry[j]] !== undefined && param[keyAry[j]] !== null ? param[keyAry[j]] : "")
                    }
                    if (rs.length > 0)
                        rs = rs.substring(1);
                    rs = this.sha1(rs);
                    return rs
                },
                getSecret: function(param) {
                    var rs = "";
                    var _this = this;
                    var enString = param.api_key && _this.data.enString[param.api_key] ? _this.data.enString[param.api_key] : "";
                    return _this.aesDecrypt(enString, _this.data.secret)
                },
                aesEncrypt: function(msg, secret) {
                    return CryptoJS.AES.encrypt(msg, secret).toString()
                },
                aesDecrypt: function(msg, secret) {
                    var bytes = CryptoJS.AES.decrypt(msg, secret);
                    return bytes.toString(CryptoJS.enc.Utf8)
                },
                sha1: function(msg) {
                    return CryptoJS.SHA1(msg).toString()
                },
                getCookie: function(name) {
                    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
                    if (arr = document.cookie.match(reg))
                        if (arr[2])
                            return unescape(arr[2]);
                    return ""
                }
            };
    var pc_edata = vipParamsEncrypt.encrypt(skey, set.data);
    var parme ={api_key: "70f71280d5d547b2a7bb370a529aeea1", pc_eversion: 1, skey: "3c5ad16dbc06cd16ae1fd3344d87f16b", pc_edata: pc_edata};
    var headers=sign.getSign('https://passport.vip.com/login/postLogin',parme);
    var data={'pc_edata':pc_edata,'headers':headers,'cid':cookie_cid_sid[0],'sid':cookie_cid_sid[1]};
    return data
}

console.log(getFromData('17683774590',"e10adc3949ba59abbe56e057f20f883e"))

// 获取cookie中的sid和cid
function getCookieCidSid(){
     var k = function(a) {
                        var b = ""
                          , c = 0;
                        for (a = a || 32; c < a; c++)
                            b += "0123456789abcdef".charAt(Math.ceil(1E8 * Math.random()) % 16);
                        return b
                    }
    ;
    function generateCid() {
        for (var a = (new Date).getTime().toString(), b = k(), c = 0, d = a.length, f = 0; f < d; f++)
            c += parseInt(a[f]);
        for (var d = c % 32, e = c, c = b.length, f = 0; f < c; f++)
            f !== d && (e += parseInt(b[f], 16));
        f = (e % 16).toString(16);
        a = a + "_" + b.substr(0, d) + f.toString() + b.substr(1 + d, c);
        return a
    }

    return [generateCid(),k()]
}



