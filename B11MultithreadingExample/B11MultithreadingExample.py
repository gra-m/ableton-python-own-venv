import threading
import time


def my_thread_function1():
    for i in range(10):
        print("1")
        time.sleep(0.001)


def my_thread_function2():
    for i in range(10):
        print("2")
        time.sleep(0.001)


#my_thread_function1()
#my_thread_function2()

thread1 = threading.Thread(target=my_thread_function1)
thread2 = threading.Thread(target=my_thread_function2)

thread1.start()
thread2.start()
