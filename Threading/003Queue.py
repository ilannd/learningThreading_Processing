import threading
from queue import Queue


# Python 的 Queue 模块中提供了同步的、线程安全的队列类
# 包括FIFO（先入先出)队列Queue，LIFO（后入先出）队列LifoQueue，和优先级队列 PriorityQueue。
# 这些队列都实现了锁原语，能够在多线程中直接使用，可以使用队列来实现线程间的同步。
# Queue.put(item) 写入队列，timeout等待时间
# Queue.get([block[, timeout]])获取队列，timeout等待时间
# Queue模块中还有很多方法

def job(l, q):
    for i in range(len(l)):
        l[i] = l[i] ** 2
    # return l
    q.put(l)


# 在多线程中，线程是不能返回一个值的

def multithreading():
    q = Queue()
    # 在q放入计算的的返回值，来替代return
    threads = []
    data = [[1, 2, 3], [3, 4, 5], [4, 4, 4], [5, 5, 5]]
    for i in range(4):
        t = threading.Thread(target=job, args=(data[i], q))  # args是job函数的参数
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    results = []
    for _ in range(4):
        results.append(q.get())
    print(results)


if __name__ == '__main__':
    multithreading()

# 运行结果
# [[1, 4, 9], [9, 16, 25], [16, 16, 16], [25, 25, 25]]
