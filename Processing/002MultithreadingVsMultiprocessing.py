# 一般的Python程序只会用到计算机的一个核或一个线程
# 多线程实际上还是让计算机在同一个时间处理一个线程
# 多核就能解决这种问题
import multiprocessing as mp
import threading as td
import time


def job(q):
    res = 0
    for i in range(10000000):
        res += i + i ** 2 + i ** 3
    q.put(res)


def normal():
    res = 0
    for _ in range(2):
        for i in range(10000000):
            res += i + i ** 2 + i ** 3
    print('normal', res)
    # 普通方法，没有q


def multithread():
    q = mp.Queue()  # 注意这里是多进程模块的Queue模块，与多线程的Queue模块不一样
    t1 = td.Thread(target=job, args=(q,))  # 注意这里args的参数，q后边要加一个,
    t2 = td.Thread(target=job, args=(q,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    res1 = q.get()
    res2 = q.get()
    print('thread', res1 + res2)


def multicore():
    q = mp.Queue()  # 注意这里是多进程模块的Queue模块，与多线程的Queue模块不一样
    p1 = mp.Process(target=job, args=(q,))  # 注意这里args的参数，q后边要加一个,
    p2 = mp.Process(target=job, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    res1 = q.get()
    res2 = q.get()
    print('core', res1 + res2)


if __name__ == '__main__':
    st = time.time()
    normal()
    st1 = time.time()
    print('normal time:', st1 - st)
    multithread()
    st2 = time.time()
    print('multithread time:', st2 - st1)
    multicore()
    st3 = time.time()
    print('multicore time:', st3 - st2)

# 下面这段话的原理是针对多线程的词语，因为我在多线程的代码中也看到了冗余的join()
# 没必要写join(),也没有设置守护线程，主线程会等其他线程执行的。又有队列，队列的get 已经是阻塞式的了


# 运行结果  1000000次下                     # 不同的次数下，有不同的运行结果
# normal 499999666667166666000000
# normal time: 1.7184052467346191
# thread 499999666667166666000000
# multithread time: 1.750396490097046
# core 499999666667166666000000
# multicore time: 1.2378895282745361
# 可以看出多线程的时间比普通的时间还要长一点
# 多核的最快，在运算量越大情况下越明显
