import threading
import time
x = 0


def userIn():
    global x
    print("THREADZ")
    x = int(input())
    print("ty for input")

t = threading.Thread(target=userIn)

while True:
    if x != 0:
        exit()
    print("Hello World")
    t = threading.Thread(target=userIn)
    t.start()
    t = threading.Thread(target=userIn)
    t.start()
    time.sleep(5)

