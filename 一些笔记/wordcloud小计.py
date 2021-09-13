from wordcloud import WordCloud

wc = WordCloud('参数')

#参数
# font_path:字体文件（OTF或TTF）的路径，字符串

# width:绘图区宽度，默认400，整型

# height:绘图区高度，默认200，整型

# prefer_horizontal:单词倾向于水平放置还是垂直放置，如果值小于1，则会在不合适的情况下旋转单词，浮点型，默认0.9

# mask:是否在给定的形状内绘制单词，这个参数使我们能够根据给定的轮廓形状绘制各种词云图，当此参数不为None时，width和height将被忽略，nd-array型或None，默认None

# scale:计算过程和实际绘图的比例，浮点型，默认1

# min_font_size:绘图时最小的字体大小，整型，默认4

# font_step:字体大小的迭代步长，大于1时可能会出现错误排列，整型，默认1

# max_words:绘图使用的最大单词数，整型，默认200

# stopwords:排除的单词集，字符串集或None，默认为None时，内置的字符串集将会被使用

# background_color:背景颜色，颜色值，默认为'black'

# max_font_size:绘图时最大字体大小，整型或None，默认为None

# mode:模式，默认为'RGB'，当为'RGBA'时，倘若背景颜色为None，则会得到透明的背景

# relative_scaling:单词出现频率对其字体大小的权重，值为0时，只考虑单词排名对字体大小的影响，值为1时，具有2倍出现频率的单词具有2倍的字体大小，一般值设置为0.5最棒，浮点型

# color_func:颜色函数，用于生成不同颜色单词的词云图，默认为None

# regexp:正则表达式，用于分词，默认为 r"\w[\w']+"

# collocations:是否包括二元词组，布尔型，默认为True

# colormap:颜色图，随机分配颜色给每个单词，如果指定了color_func，则本参数被忽略，字符串或matplotlib colormap型，默认为'viridis'

# normalize_plurals:移除单词末尾的's'，布尔型，默认为True

'''属性'''
wc.words_
#对应频率的词例，字典类型{字符串：浮点数}

wc.layout_
#记录每个单词的值，字体大小，位置，方向以及颜色，由一系列元组组成的列表，每个元组格式为(string, int, (int, int), int, color)

x=[]
'''方法'''
text=' '.join(x)
wc.generate(text)
#从文本中生成词云图

frequencies=('词','频率')
wc.fit_words(frequencies)
#根据给定单词及频率生成词云图
#frequencies:元组型数组，每个元组包含一个单词及其频率

wc.generate_from_frequencies(frequencies, max_font_size=None)
#根据给定单词及频率生成词云图
#frequencies:字典，包含字符串（单词）:浮点数（频率）的值对
#max_font_size:最大字体大小


wc.process_text(text)
#将长文本分词，并移除stopwords集合中的单词
#返回字典，dict (string, int)

wc.recolor(random_state=None, color_func=None, colormap=None)
#重新上色
#random_state:随机种子，整型或None

wc.to_array()
#以numpy矩阵的格式返回词云图

wc.to_file('')
#以图片的格式返回词云图
#filename:保存路径