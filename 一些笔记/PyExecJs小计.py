'''pip install PyExecJs  执行js代码'''

'''
找到execjs模块下的_external_runtime.py文件，里面有一句代码：
p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self._cwd, universal_newlines=True)
把上面的代码改成：
p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self._cwd, universal_newlines=True, encoding='utf-8')
也就是加上了encoding =‘utf-8’，保存，问题解决。
'''


import execjs
import requests
headers={'Referer': 'http://www.dm5.com/'}
url='http://www.dm5.com/m485300/chapterfun.ashx?cid=485300&page=2&key=&language=1&gtk=6&_cid=485300&_mid=36410&_dt=2021-04-11+12%3A59%3A52&_sign=a106d90516c307775a804ca1bf2a93fa'
r=requests.get(url,headers=headers,timeout=5)
print(r.status_code)
print(r.text)
print(execjs.eval(r.text)[0]) # 执行js代码返回结果


import execjs
print(execjs.eval(r'''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}('e 9(){2 6=4;2 5=\'a\';2 7="g://j.h.f/1/b/4";2 3=["/c.8","/k.8"];o(2 i=0;i<3.l;i++){3[i]=7+3[i]+\'?6=4&5=a&m=\'}n 3}2 d;d=9();',25,25,'||var|pvalue|180970|key|cid|pix|jpg|dm5imagefun|e7a63405323a7a1735bb5b6774e48c36|266|1_8812||function|com|https|mangabz||image|2_6933|length|uk|return|for'.split('|'),0,{}))'''))


# javascript代码
'''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((
c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String))
{while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\w+'}
;c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}
('l 8(){1 5=3;1 4=\'9\';1 6="g://h-j-k-f-a.b.e/c/r/3";1 2=["/q.7","/s.7"];p(1 i=0;i<2.m;i++)
{2[i]=6+2[i]+\'?5=3&4=9&o=\'}n 2}1 d;d=8();',29,29,'|var|pvalue|538519|key|cid|pix|jpg|dm5imagefun
|cf7d83689b3046d368aece37b15a8383|98|cdndm5|39||com|161|http|manhua1032||101|69|function|length|return|u
k|for|2_5561|38427|3_4637'.split('|'),0,{}))

http://manhua1032-101-69-161-98.cdndm5.com/39/38427/538519/2_5561.jpg?cid=538519&key=cf7d83689
b3046d368aece37b15a8383&uk='''



import execjs
#1.实例化一个node对象
node = execjs.get()
path=r'C:\Users\26359\Desktop\Python爬虫逆向课程课件\逆向课件\3.微信公众平台js逆向\微信公众平台\wechat.js'
with open(path,'r',encoding='utf-8') as f:
    #2.js源文件编译
    ctx = node.compile(f.read())

    #3.执行js函数
    # funcName = 'getPwd("{0}")'.format('123456')
    # pwd = ctx.eval(funcName)
    pwd = ctx.call("getPwd",'123456')
    print(pwd)