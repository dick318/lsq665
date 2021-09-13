'''pip install bs4
pip install lxml'''
from bs4 import BeautifulSoup


r=''
soup = BeautifulSoup(r.text,'lxml')

soup.find('div',class_='')

# find_all( name , attrs , recursive , string , **kwargs )
# name：搜索 name 参数的值可以使任一类型的 过滤器 ,字符窜,正则表达式,列表,方法或是 True
# string：通过 string 参数可以搜搜文档中的字符串内容.与 name 参数的可选值一样, string 参数接受 字符串 , 正则表达式 , 列表, True
# recursive=False时值搜索当前节点的子节点，不搜索孙节点
# **kwargs：如果一个指定名字的参数不是搜索内置的参数名,搜索时会把该参数当作指定名字tag的属性来搜索,
soup.find_all('div',class_='',id="",recursive=False)
# 使用多个指定名字的参数可以同时过滤tag的多个属性:


soup.text   # 获取标签下的所有文本（包括子节点）
soup.string  # 获取当前节点的文本信息（不包括子节点）
soup.a       # 当前节点下的第一个a节点
soup.get('href',None)
soup.contents # 所有子节点组成的列表


# 兄弟节点
soup = BeautifulSoup("<a><b>text1</b><c>text2</c></b></a>",'lxml')
print(soup) # <html><body><a><b>text1</b><c>text2</c></a></body></html>
print(soup.b.next_sibling) # <c>text2</c>
print(soup.c.previous_sibling) # <b>text1</b>



# 如果传入列表参数,Beautiful Soup会将与列表中任一元素匹配的内容返回.下面代码找到文档中所有<a>标签和<b>标签:
soup.find_all(["a", "b"])
# [<b>The Dormouse's story</b>,
#  <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]



# 有些tag属性在搜索不能使用,比如HTML5中的 data-* 属性:
soup = BeautifulSoup('<div data-foo="value">foo!</div>')
# soup.find_all(data-foo="value")
# SyntaxError: keyword can't be an expression
# 但是可以通过 find_all() 方法的 attrs 参数定义一个字典参数来搜索包含特殊属性的tag:
soup.find_all(attrs={"data-foo": "value"})
# [<div data-foo="value">foo!</div>]



# tag的 class 属性是 多值属性 .按照CSS类名搜索tag时,可以分别搜索tag中的每个CSS类名:
css_soup = BeautifulSoup('<p class="body strikeout"></p>')
css_soup.find_all("p", class_="strikeout")
# [<p class="body strikeout"></p>]
css_soup.find_all("p", class_="body")
# [<p class="body strikeout"></p>]


# ### xpath解析
# - 环境安装：
#     - pip install lxml
# - 解析原理:html标签是以树状的形式进行展示
#     - 1.实例化一个etree的对象，且将待解析的页面源码数据加载到该对象中
#     - 2.调用etree对象的xpath方法结合着不同的xpath表达式实现标签的定位和数据提取
# - 实例化etree对象
#     - etree.parse('filename'):将本地html文档加载到该对象中
#     - etree.HTML(page_text):网站获取的页面数据加载到该对象
# - 标签定位：
#     - 最左侧的/:如果xpath表达式最左侧是以/开头则表示该xpath表达式一定要从根标签开始定位指定标签(忽略)
#     - 非最左侧的/:表示一个层级
#     - 非左侧的//:表示多个层级
#     - 最左侧的//：xpath表达式可以从任意位置进行标签定位
#
#     - 属性定位：tagName[@attrName="value"]
#     - 索引定位：tag[index]:索引是从1开始
#     - 模糊匹配：
#         - //div[contains(@class, "ng")]
#         - //div[starts-with(@class, "ta")]
# - 取文本
#     - /text():直系文本内容
#     - //text()：所有的文本内容
# - 取属性
#     - /@attrName
from lxml import  etree
tree=etree.HTML(r.text)
#定位class为song的div下面所有的p
tree.xpath('//div[@class="song"]/p')
#定位class为song的div下面第2个p
tree.xpath('//div[@class="song"]/p[2]//text()')
tree.xpath('//a[@id="feng"]/@href')