import threading


# ps -fLu nigga | wc -l
# ulimit -u

def create_threads_from_list(iplist, function):
    threads = []

    for ip in iplist:
        th = threading.Thread(target=function, args=(ip,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()


def create_threads_to_max(max, function):
    global threads
    threads = []
    count = 0
    while count < max:
        th = threading.Thread(target=function, args=(count,))
        print(f"starting thread {th.getName()}")
        th.start()
        threads.append(th)
        count += 1

    for th in threads:
        print(f"joining thread {th.getName()}")
        th.join()


def function(count):
    print(f"function({count=})")


threads = []
if __name__ == '__main__':
    try:
        create_threads_to_max(99999, function=function)
    except KeyboardInterrupt:
        print("CTRL-C")
        for th in threads:
            print(f"joining thread {th.getName()}")
            th.join()
        exit()
    except Exception as e:
        print(repr(e))
        exit()
