import threading
import time
import icecream as ic

frames = 10
q1 = True
q2 = True
rendered = 0

def move_frame():
    rendered = input("Finished frame: ")
    return

def queue1(num):
    return

def queue2(num):
    return

rendered_frames = threading.Thread(target=move_frame, daemon=True)    

i=1
while (i<=frames):
    time.sleep(1)
    if (q1==True):
        t1 = threading.Thread(target=queue1, daemon=True, args=(i,))
        q1 = False
        i += 1
    if (q2==True):
        t2 = threading.Thread(target=queue2, daemon=True, args=(i,))
        q2 = False
        i += 1
    else:
        ic(f"Queue 1: {i}")
        ic(f"Queue 2: {i}")
 
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