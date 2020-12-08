import threading


def thread_job():
    print("This is an added Thread,number is %s" % threading.current_thread())


def main():
    added_thread = threading.Thread(target=thread_job)  # 创建了线程，指定它做什么工作，注意传入的是函数名，不要加()
    added_thread.start()
    '''
    print(threading.active_count())
    print(threading.enumerate())
    print(threading.current_thread())
    '''


if __name__ == '__main__':
    main()
