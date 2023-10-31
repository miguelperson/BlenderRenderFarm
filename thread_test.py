import threading

frames = 10
q1 = True
q2 = True
 
def print_cube(num):
    # function to print cube of given num
    print("Cube: {}" .format(num * num * num))
 
 
def print_square(num):
    # function to print square of given num
    print("Square: {}" .format(num * num))
 
i=1
while (i<=frames):
    if (q1==True):
        t1 = threading.Thread(target=print_square, args=(i,))
        i += 1
    if (q2==True):
        t2 = threading.Thread(target=print_cube, args=(i,))
        i += 1
 
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
 
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
 
    # both threads completely executed
    print("Done!")