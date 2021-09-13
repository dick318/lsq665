def encrypto(pk, password):     # 注意公钥格式 要有头有尾 有换行
    from Crypto.PublicKey import RSA  # 导入模块
    from Crypto.Cipher import PKCS1_v1_5
    import base64
    public_key = "-----BEGIN PUBLIC KEY-----\n{}\n-----END PUBLIC KEY-----".format(pk)
    rsakey = RSA.importKey(public_key,'100001')
    cipher = PKCS1_v1_5.new(rsakey)
    result_encode = cipher.encrypt(password.encode())
    cipher_text = base64.b64encode(result_encode)
    result = cipher_text.decode()   # 这里根据实际情况选择要不要编码
    print(result)
    return result

if __name__ == '__main__':
    key='''MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1uonJlrio1n53/QcFTEW
    jdcBaduq4kJc81QbkQ2aIN2rbhbQZ+XyXcL2Yo1A/mP1vBdgxl0YBcO3pAOSowIK
    t/vTBcDMRMfKRB2MaO8X9oZPGzkWyM9kIKy9eYHmRTsqMmahzNH7sC8O3JI3XulP
    da2QNbVmcqZlVFGnPs3+4vsNnJ0xlQ7usPDDUh/+HqC6bD2q2UNGNjHz+6AwWrmb
    tXg582UWD6F6IWnUbNg4VqXcoRjeYU6BrPGIx1PeMm4RuzafnYxrcoFwu7OlidjU
    w3JbI/kpmRiHMs+qp8JdAhZC03bGCbzrsMApGEK+LIP0diOobBDjrNCM/IObdzLb
    XQIDAQAB'''
    encrypto(key,'17683774590asad',)




from Crypto.PublicKey import RSA # 导入模块
from Crypto.Cipher import PKCS1_v1_5
import base64

key = RSA.generate(2048)
with open('prkey.pem', 'wb') as f: # 生成私钥文件
    f.write(key.exportKey('PEM'))

public = key.publickey()
with open('pukey.pem', 'wb') as f: # 生成公钥文件
    f.write(public.exportKey('PEM'))


def encrypto(password):  # 使用公钥加密
    rsakey = RSA.importKey(open('pukey.pem').read())
    cipher = PKCS1_v1_5.new(rsakey)
    result_encode = cipher.encrypt(password.encode())
    cipher_text = base64.b64encode(result_encode)
    result = cipher_text.decode()
    print(result)
    return result


def dencrypto(password):  # 使用私钥解密
    prkey = RSA.importKey(open('prkey.pem').read())
    cipher = PKCS1_v1_5.new(prkey)
    result_encode = cipher.decrypt(base64.b64decode(password.encode()), 'ERROR')
    result = result_encode.decode()
    print(result)


if "__name__" == "__main__":
    dencrypto(encrypto('网虫Spider'))
