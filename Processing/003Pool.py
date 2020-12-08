import multiprocessing as mp


def job(x):
    return x * x


# 以前用mp.Process(),job()是不能用return的，要用Queue的q去q.put(),再q.get()
# 但是在pool(进程池)里面有return

# Pool类可以提供指定数量的进程供用户调用
# 当有新的请求提交到Pool中时，如果池还没有满，就会创建一个新的进程来执行请求。
# 如果池满，请求就会告知先等待，直到池中有进程结束，才会创建新的进程来执行这些请求。

def multicore():
    pool = mp.Pool()  # 默认的值是你所有的核
    # pool有很多函数
    # pool = mp.Pool(processes=1)  # 指定用3个核，不过我试了一下不管用,还是四格核
    # 把res与job要map在一起
    # 往pool里面放入你的方程和你要运算的值，会自动分配给每一个进程，每一个cup核，再返回出res
    res = pool.map(job, range(10))
    print(res)
    # 运行结果
    # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

    res = pool.apply_async(job, (2,))  # 只传入一个值，放到一个核里面运算一次
    print(res.get())
    # 运行结果
    # 4

    '''
    # 会报错，因为只能传入一个值
    res = pool.apply_async(job, (2,3,4))  # 只传入一个值，放到一个核里面运算一次
    print(res.get())
    '''

    # 用迭代器可以实现传入多个值,但是输出结果时也要用到迭代
    multi_res = [pool.apply_async(job, (i,)) for i in range(10)]
    print([res.get() for res in multi_res])
    # 运行结果
    # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]


if __name__ == '__main__':
    multicore()
