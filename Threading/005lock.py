import threading
import time


# 第一个线程处理完得到一个初步的结果，第二个线程再处理第一个线程得到的结果
# 就要用到锁了，先锁住第一个线程，等它处理完，再开始第二个线程

def job1():
    global A, lock
    # 加了锁之后，job2不会再接触到这块共享存储空间
    lock.acquire()
    for i in range(10):
        A += 1
        # time.sleep(0.1)
        print('job1', A)
    lock.release()


def job2():
    global A, lock
    lock.acquire()
    for i in range(10):
        A += 10
        print('job2', A)
    lock.release()


if __name__ == '__main__':
    lock = threading.Lock()
    A = 0
    # 这是一个全局变量，是shared memory
    # 不加锁的情况下，两个进程对同一个共享存储空间进行操作，会乱掉
    t1 = threading.Thread(target=job1)
    t2 = threading.Thread(target=job2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

# 运行结果
# 可以看出，job1运行完之后才运行的job2,他两互不影响
# job1 1
# job1 2
# job1 3
# job1 4
# job1 5
# job1 6
# job1 7
# job1 8
# job1 9
# job1 10
# job2 20
# job2 30
# job2 40
# job2 50
# job2 60
# job2 70
# job2 80
# job2 90
# job2 100
# job2 110
