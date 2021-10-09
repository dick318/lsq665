let CryptoJS = require('crypto-js')

function encryptByDES(message, key) {
    var keyHex = CryptoJS.enc.Utf8.parse(key);
    var encrypted = CryptoJS.DES.encrypt(message, keyHex, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    var str = encrypted.toString();
    str = str.replace("+", "[j]").replace("+", "[j]");
    return str;
}

console.log(encryptByDES('123456','6Ta4OaHZdpA='))