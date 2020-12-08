# 一般的Python程序只会用到计算机的一个核或一个线程
# 多线程实际上还是让计算机在同一个时间处理一个线程
# 多核就能解决这种问题
import multiprocessing as mp

# 进程的创建于线程的创建类似

def job(q):
    res = 0
    for i in range(1000):
        res += i + i ** 2 + i ** 3
    q.put(res)


if __name__ == '__main__':
    q = mp.Queue()  # 注意这里是多进程模块的Queue模块，与多线程的Queue模块不一样
    p1 = mp.Process(target=job, args=(q,))  # 注意这里args的参数，q后边要加一个,
    p2 = mp.Process(target=job, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    res1 = q.get()
    res2 = q.get()
    print(res1 + res2)

# 下面这段话的原理是针对多线程的词语，因为我在多线程的代码中也看到了冗余的join()
# 没必要写join(),也没有设置守护线程，主线程会等其他线程执行的。又有队列，队列的get 已经是阻塞式的了
