import queue

# 构造一个FIFO队列, maxsize设置队列大小的上界, 如果插入数据时达到上界就会发生阻塞
# 直到队列可以放入数据. 当maxsize小于或者等于0, 表示不限制队列的大小(默认)
q = queue.Queue(maxsize=5)
# 直到队列可以放入数据. 当maxsize小于或者等于0, 表示不限制队列的大小(默认)
lq = queue.LifoQueue(maxsize=0)
# 优先级队列中, 最小值被最先取出
pq = queue.PriorityQueue(maxsize=0)

# 向队列添加元素，如果队列已满等待，等待时间结束还是满则抛出Full()异常，如果没有设置等待时间则一直等待
q.put(item='', timeout=5, block=True)
# 队列弹出元素，如果队列为空，则等待，等待时间结束还是空则抛出Empty()异常
c=q.get(timeout=5, block=True)
# 相当于put(block=Flase),队列满时直接抛出Full()异常
q.put_nowait(item='')
# 相当于get(block=False),队列为空时直接抛出Empty()异常
q.get_nowait()


# 定义的异常 大写
queue.Empty()  # 当调用非阻塞的 get() 获取空队列的元素时, 引发异常
queue.Full()  # 当调用非阻塞的 put() 向满队列中添加元素时, 引发异常

# 返回队列的大小，相当于len（）
q.qsize()
# 如果队列为空，返回True，反之False
q.empty()
# 如果队列满了，返回True，反之False
q.full()
# 实际上意味着等到队列为空，再执行别的操作。待队列中任务全部处理完毕，需要配合queue.task_done使用
q.join()
