import time

start = time.perf_counter()
def do_something():
    print("Sleeping for 2 seconds")
    time.sleep(1)
    print("done sleeping")

do_something()
do_something()
finish = time.perf_counter()

print("Finished in {:.2f}".format(finish))