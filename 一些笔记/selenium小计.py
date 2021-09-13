from selenium import webdriver

'''不打开浏览器'''
option = webdriver.ChromeOptions()
option.add_argument("headless")

'''
不加载图片，css和js
# 2代表禁止加载，1代表允许加载
'''
prefs = {
        'profile.default_content_setting_values': {
            'images': 2,
            'permissions.default.stylesheet':2,
            'javascript': 2
        }
    }
option.add_experimental_option('prefs', prefs)

'''去掉chrom受自动测试软件的控制的提示'''
option.add_experimental_option('useAutomationExtension', False)
option.add_experimental_option("excludeSwitches", ['enable-automation'])

driver = webdriver.Chrome(executable_path='D:/project/爬虫/chromedriver.exe', chrome_options=option)


# 打开浏览器，'D:/environment/pycharm/爬虫/chromedriver.exe'文件位置
driver = webdriver.Chrome(executable_path='D:/project/爬虫/chromedriver.exe')

# 关闭浏览器，关闭当前窗口
driver.quit()
driver.close()

# 隐性等待，最多10秒
driver.implicitly_wait(10)
# 打开链接地址页面
url = ''
driver.get(url)
# 伪装selenium,写在获取页面后
script = 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined,});'
driver.execute_script(script)


'''向下滑动页面,滑动当要可视范围的高度，js注入'''
script1 = 'window.scrollTo(0,document.body.scrollHeight)'  # 0，表示左右滑动，后面表示上下滑动
# 执行js代码完成操作
driver.execute_script(script1)
driver.set_script_timeout(5)  # 设置脚本延时五秒后执行


# 获取当前界面url
driver.current_url
# 获取当前元素的字
driver.text
# 刷新当前页面
driver.refresh()
driver.forward()  # 前进
driver.back()  # 后退
# 获取源码
driver.page_source
# 获取当前cookie
driver.get_cookies()
# 添加cookie
driver.add_cookie({'name':'name','value':'value'})

'''对图片进行操作'''
from PIL import Image
# 获取图片的信息
img_tag=driver.find_element_by_xpath('//*[@id="J-loginImg"]')
# 获取图片的左上角坐标【返回一个字典】
location = img_tag.location#img_tag表示的图片在当前页面中左下角坐标
# 获取图片的长宽 【返回一个字典】
size = img_tag.size #验证码图片的尺寸
rangle = (int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
i = Image.open('./12306.png')
frame = i.crop(rangle)
frame.save('./code.png')

'''切换'''
# 处理iframe标签
driver.switch_to.frame('iframe标签的位置或者id')
# 返回window界面
driver.switch_to.window()
# 处理alert弹框
'''切换到弹窗'''
alert = driver.switch_to.alert   # 切换到弹窗
text = alert.text      # 获取警告信息
alert.accept()      # 点击确认按钮
alert.dismiss()     # 点击取消按钮
alert.send_keys()   # 输入字符  prompt
'''切换标签页'''
current_window = driver.window_handles
driver.switch_to.window(current_window[1])

# 查找元素
driver.find_element_by_link_text('搜索设置').click() # 根据链接文本内容查找链接
driver.find_element_by_xpath('copy检查元素中的xpath')
driver.find_element_by_css_selector('标签[属性=‘名’]')  # CSS选择器  #id  tag.class
driver.find_element_by_id(id_='id')
driver.find_element_by_tag_name('标签名')
driver.find_element_by_name(name='')
# 获取标签中的属性
driver.find_element_by_name('').get_attribute('url')

'''操作'''
c = driver.find_element_by_name('')
c.clear()  # 清除元素内容
c.send_keys('')  # 模拟按键输入
c.click()  # 单击元素
c.text  # 获取标签内容



# 模拟键盘输入
from selenium.webdriver.common.keys import Keys

c.send_keys(Keys.BACK_SPACE)  # 删除键BackSpace
c.send_keys(Keys.SPACE)  # 空格键Space
c.send_keys(Keys.TAB)  # 制表键Tab
c.send_keys(Keys.ESPACE)  # 回退键Esc
c.send_keys(Keys.ENTER)  # 回车键Enter
c.send_keys(Keys.CONTROL, 'a')  # 全选Ctrl+A
c.send_keys(Keys.CONTROL, 'c')  # 复制CTRL+C
c.send_keys(Keys.CONTROL, 'x')  # 剪切CTRL+X
c.send_keys(Keys.CONTROL, 'v')  # 粘贴Ctrl+V
c.send_keys(Keys.SHIFT, 'a')  # shift+a
c.send_keys(Keys.F1)  # 键盘F1
c.send_keys(Keys.F12)  # 键盘F12

'''窗口操作'''
c.maximize_window()  # 最大化
c.fullscreen_window()  # 全屏
c.minimize_window()  # 最小化
c.get_window_position()  # 获取窗口的坐标
c.get_window_rect()  # 获取窗口的大小和坐标
c.get_window_size()  # 获取窗口的大小
c.set_window_position(100, 200)  # 设置窗口的坐标
c.set_window_rect(100, 200, 32, 50)  # 设置窗口的大小和坐标
c.set_window_size(400, 600)  # 设置窗口的大小
c.current_window_handle  # 返回当前窗口的句柄
c.window_handles  # 返回当前会话中的所有窗口的句柄


'''截图'''
c.save_screenshot('1.png')  # 截图，只支持PNG格式
c.get_screenshot_as_png()  # 获取当前窗口的截图作为二进制数据
c.get_screenshot_as_base64()  # 获取当前窗口的截图作为base64编码的字符串




'''动作链'''

# span=driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
# action=webdriver.ActionChains(driver)
# action.click_and_hold(span).perform()
# action.drag_and_drop_by_offset(span,400,0).perform()

from selenium.webdriver import ActionChains  # 动作链
from time import sleep
#对div_tag进行滑动操作
action = ActionChains(driver) # 创建对象
div_tag = driver.find_element_by_xpath('//*[@id="draggable"]') # 获取要操作的对象
action.click_and_hold(div_tag) # 点击且长按

for i in range(6):
    #perform让动作链立即执行
    action.move_by_offset(10,15).perform()
    sleep(0.5)
action.release() # 松开鼠标左键
driver.quit()

'''
click(on_element=None)                 #鼠标左键单击
click_and_hold(on_element=None)        #单击鼠标左键，不松开
context_click(on_element=None)         #单击鼠标右键
double_click(on_element=None)          #双击鼠标左键
drag_and_drop(source,target)           #拖拽到某个元素然后松开
drag_and_drop_by_offset(source,xoffset,yoffset) #拖拽到某个坐标然后松开
key_down(value,element=None)     #按下键盘上的某个键
key_up(value, element=None)      #松开键盘上的某个键
move_by_offset(xoffset, yoffset)  #鼠标从当前位置移动到某个坐标
move_to_element(to_element)        #鼠标移动到某个元素
move_to_element_with_offset(to_element, xoffset, yoffset) #移动到距某个元素（左上角坐标）多少距离的位置
pause(seconds)                  #暂停所有输入(指定持续时间以秒为单位)
perform()                       #执行所有操作
reset_actions()                 #结束已经存在的操作并重置
release(on_element=None)       #在某个元素位置松开鼠标左键
send_keys(*keys_to_send)        #发送某个键或者输入文本到当前焦点的元素
send_keys_to_element(element, *keys_to_send) #发送某个键到指定元素
'''


'''
- 如何让selenium规避检测
    - 有的网站会检测请求是否为selenium发起，如果是的话则让该次请求失败
    - 规避检测的方法：
        - selenium接管chrome浏览器

- 实现步骤
    - 1.必须将你电脑中安装的谷歌浏览器的驱动程序所在的目录找到。且将目录添加到环境变量中。
    - 2.打开cmd，在命令行中输入命令：
        - chrome.exe --remote-debugging-port=9222 --user-data-dir="一个空文件夹的目录"
        - 指定执行结束后，会打开你本机安装好的谷歌浏览器。
    - 3.执行如下代码：可以使用下属代码接管步骤2打开的真实的浏览器
    
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#本机安装好谷歌的驱动程序路径
chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver,chrome_options=chrome_options)
print(driver.title)
'''