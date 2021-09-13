'''https://loguru.readthedocs.io/en/stable/api/logger.html#file'''
'''pip install loguru'''

from loguru import logger

import sys
# 如果要将记录的消息发送到文件，则只需使用字符串路径作为接收器。为方便起见，它也可以自动计时：
# logger.add("file_{time}.log")

# 日志文件中只记载级别以上的日志，而控制台中输出所有的日志
logger.add(sys.stderr,level='WARNING')
# logger.add('./a.txt',mode='w',encoding='utf-8',level='error'.upper())
# 默认输出：包括时间、日志级别、模块名、行号、日志内容
logger.debug('hello world')
logger.info('hello world')
logger.warning('hello world')
logger.error('hello world')
logger.critical('hello world')

'''add 参数'''
# sink ( , , , , or ) – 一个对象，负责接收格式化的日志消息并将它们传播到适当的端点。file-like objectstrpathlib.Pathcallablecoroutine functionlogging.Handler
# level ( intor str, 可选) -- 记录的消息应该发送到接收器的最低严重级别。
# format（str或callable，可选）– 用于在发送到接收器之前格式化记录的消息的模板。
# filter ( callable, stror dict, optional) -- 一个可选的指令，用于决定每个记录的消息是否应该发送到接收器。
# colorize ( bool, 可选) – 格式化消息中包含的颜色标记是否应转换为用于终端着色的 ansi 代码，或者以其他方式剥离。如果None，则根据接收器是否为 tty 自动做出选择。
# serialize ( bool, 可选) – 在发送到接收器之前，是否应首先将记录的消息及其记录转换为 JSON 字符串。
# backtrace ( bool, 可选) – 格式化的异常跟踪是否应该向上扩展，超出捕获点，以显示生成错误的完整堆栈跟踪。
# diagnose（bool，可选）– 异常跟踪是否应显示变量值以简化调试。这应该False在生产中设置为避免泄露敏感数据。
# enqueue ( bool, 可选) – 要记录的消息是否应在到达接收器之前首先通过多进程安全队列。这在通过多个进程记录到文件时很有用。这也具有使日志记录调用非阻塞的优点。
# catch ( bool, 可选) – 是否应自动捕获接收器处理日志消息时发生的错误。如果True，则显示异常消息，sys.stderr但异常不会传播到调用者，从而防止您的应用程序崩溃。
# **kwargs – 仅对配置协程或文件接收器有效的附加参数（见下文）。



# rotation ( str, int, datetime.time, datetime.timedeltaor callable, optional) – 一种条件，指示何时应关闭当前记录的文件并开始新的文件。
# retention( str, int, datetime.timedeltaor callable, 可选) – 过滤旧文件的指令，应在循环或程序结束期间删除。
# compression（str或callable，可选）– 日志文件在关闭时应转换为的压缩或存档格式。
# delay ( bool, 可选) -- 是在配置接收器后立即创建文件，还是延迟到第一条记录的消息。它默认为False.
# mode ( str, 可选) – 内置open()函数的打开模式。它默认为"a"（以追加模式打开文件）。
# buffering ( int, optional) – 内置open()函数的缓冲策略。它默认为1（行缓冲文件）。
# encoding ( str, optional) – 内置open()函数的文件编码。如果None，则默认为 locale.getpreferredencoding()。
# **kwargs – 其他参数传递给内置open()函数。

'''level 参数'''
# TRACE	5	logger.trace()
# DEBUG	10	logger.debug()
# INFO	20	logger.info()
# SUCCESS	25	logger.success()
# WARNING	30	logger.warning()
# ERROR	40	logger.error()
# CRITICAL	50	logger.critical()





























import logging
from loguru import logger


# level 配置为 WARNING 信息，即只输出 WARNING 级别及其以上的信息，
# 其中Logging一共有五种级别，依次是 DEBUG < INFO < WARNING < ERROR < CRITICAL
'''输出内容'''
# format指定了 format 格式的字符串，包括
# asctime运行时间
# name模块名称、
# levelname（日志级别）,
# lineno 行号
# message （日志内容）
# pathname 完整文件路径
# filename 文件名称
# funcName 函数名称
LOG_FORMAT = "%(asctime)s----%(name)s----%(levelname)s----%(lineno)s----%(message)s----%(pathname)s----%(filename)s----%(funcName)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logging.debug("This is a debug log")
logging.info("This is a info log")
logging.warning("This is a warning log")
logging.error("This is a error log")
logging.critical("This is a critical log")