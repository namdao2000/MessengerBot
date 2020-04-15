from multiprocessing import Process, Value, Array

def f(n, a, name):
    s = 30
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]
    name.value = 10

def execute(x, foo):
    print(x)
    foo.show()

class foo():
    def show(self):
        print("hello")


if __name__ == '__main__':
    s = Value('i', 3)
    num = Value('d', 0.0)
    arr = Array('i', range(10))
    name = Value("i", 33)
    # p = Process(target=foo, args=(num, arr, name))
    # p.start()
    # p.join()
    # print (num.value)
    # print (arr[:])
    # print(name.value)
    # print(s.value)