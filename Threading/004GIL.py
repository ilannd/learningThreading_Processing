import threading
from queue import Queue
import copy
import time

# GIL（Global Interpreter Lock）即全局解释器锁，存在于python解释器中，用来确保当前只有一个线程被执行。
# 线程t1在python解释器中执行时会获得GIL，退出时释放GIL。GIL的存在让Python无法充分利用CPU资源，同时不能实现真正意义上的多线程编程。
# 当有一个线程t1获得GIL执行时，python不允许在同一时间在执行另一个t2线程，即使你是2核4线程或者更多。python不允许线程的并行执行。
# 即使你通过threading包的Thread函数进行了多线程操作，在真正执行的时候，是按串型的方式执行的，即一个线程释放GIL另一个线程获得GIL开始执行。

# Python 3.2开始使用新的GIL。新的GIL实现中用一个固定的超时时间来指示当前的线程放弃全局锁。
# 在当前线程保持这个锁，且其他线程请求这个锁时，当前线程就会在5毫秒后被强制释放该锁。

# 可以创建独立的进程来实现并行化。Python 2.6引进了多进程包multiprocessing。
# 即：Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。

# 多线程编程，模型复杂，容易发生冲突，必须用锁加以隔离，同时，又要小心死锁的发生。
#
# Python解释器由于设计时有GIL全局锁，导致了多线程无法利用多核。多线程的并发在Python中就是一个美丽的梦
#
# GIL(global interpreter locker)全局解释器锁，锁住一个运行，运行完后再切换，同时只有一个线程在工作中

def job(l, q):
    res = sum(l)
    q.put(res)


# 在多线程中，线程是不能返回一个值的，不能用return

def multithreading(l):
    q = Queue()
    # 在q放入计算的的返回值，来替代return
    threads = []
    for i in range(4):
        t = threading.Thread(target=job, args=(copy.copy(l), q), name='T%i' % i)  # args是job函数的参数
        # copy.copy()为浅copy
        # copy.deepcopy()为深拷贝
        t.start()
        threads.append(t)

    [t.join() for t in threads]
    '''
    for thread in threads:
        thread.join()
    '''
    # results = []
    total = 0
    for _ in range(4):
        # results.append(q.get())
        total += q.get()
    # print(results)
    print(total)


def normal(l):
    total = sum(l)
    print(total)


if __name__ == '__main__':
    l = list(range(1000000))
    # 不用多线程
    s_t = time.time()
    normal(l * 4)
    print('normal', time.time() - s_t)
    # 不用多线程
    s_t = time.time()
    multithreading(l)
    print('multithreading:', time.time() - s_t)

# 运行结果
# 1999998000000
# normal 0.18550467491149902
# 1999998000000
# multithreading: 0.18035554885864258
# 由此可见，多线程并不是一定会提高效率，要分情况
