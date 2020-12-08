import threading
import time


def thread_job():
    print("T1 start\n")
    for i in range(10):
        time.sleep(0.1)
    print("T1 finish\n")


def T2_job():
    print("T2 start\n")
    print("T2 finish\n")


def main():
    added_thread = threading.Thread(target=thread_job, name='T1')
    # 创建了线程，指定它做什么工作，注意传入的是函数名，不要加()
    # 命名这个线程叫做T1
    thread2 = threading.Thread(target=T2_job, name='T2')

    added_thread.start()
    thread2.start()
    added_thread.join()
    thread2.join()
    print("all done\n")

    '''
    print(threading.active_count())
    print(threading.enumerate())
    print(threading.current_thread())
    '''

if __name__ == '__main__':
    main()

# 输出结果为
# T1 start
# all done                              # 主线程执行完自己的任务后就退出了
#
#
# T1 finish                             # 子线程会继续执行自己的任务，直到结束
# 表示多个线程是在同时运行的


# 还有一种情况是设置守护线程，使用setDaemon(True)方法，设置子线程为守护线程时，主线程一旦执行结束，则全部线程全部被终止执行
# 可能出现的情况就是，子线程的任务还没有完全执行结束，就被迫停止
# 此时join的作用就凸显出来了，join所完成的工作就是线程同步，即主线程任结束之务后，进入阻塞状态，一直等待其他的子线程执行结束之后，主线程在终止

# 原因就是：  join有一个timeout参数：
#
# 1 当设置守护线程时，含义是主线程对于子线程等待timeout的时间将会杀死该子线程，最后退出程序。
# 所以说，如果有10个子线程，全部的等待时间就是每个timeout的累加和。
# 简单的来说，就是给每个子线程一个timeout的时间，让他去执行，时间一到，不管任务有没有完成，直接杀死。

# 2 没有设置守护线程时，主线程将会等待timeout的累加和这样的一段时间
# 时间一到，主线程结束，但是并没有杀死子线程，子线程依然可以继续执行，直到子线程全部结束，程序退出。

# 在加了added_thread.join()后
# T1 start
#
# T1 finish
#
# all done                                # join所完成的工作就是线程同步，即主线程任结束之务后，进入阻塞状态，一直等待其他的子线程执行结束之后，主线程在终止
# 表示在线程T1运行完了之后，才会运行别的线程


# 在添加了thread2之后
# T1 start
#
# T2 start
# all done
#
#
# T2 finish
#
# T1 finish   # 因为它加了sleep，会慢一些


# 在添加了thread2之后，在加了added_thread.join()后
# T1 start
#
# T2 start
#
# T2 finish
#
# T1 finish
#
# all done
# 表示线程之间同步运行


# 在添加了thread2之后，在加了thread2.join()后
# T1 start
#
# T2 start
#
# T2 finish
#
# all done
#
# T1 finish


# 在添加了thread2之后，在加了thread2.join()后，在加了added_thread.join()后
# T1 start
#
# T2 start
#
# T2 finish
#
# T1 finish
#
# all done
# 主线程在added_thread和thread2运行完之后再运行

