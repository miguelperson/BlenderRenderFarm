import threading
import queue
import time

# Function to distribute numbers to queues
def number_distributor(queue1, queue2):
    for number in range(1, 11):
        if number % 2 == 1:
            queue1.put(number)
            print(f"Distributed {number} to Queue 1")
        else:
            queue2.put(number)
            print(f"Distributed {number} to Queue 2")
        time.sleep(1)  # Simulate processing time

# Function to consume numbers from a queue
def number_consumer(queue):
    while True:
        try:
            number = queue.get(timeout=1)
            print(f"Consumed {number} from {queue.name}")
            # Simulate processing here
            time.sleep(1)
            queue.task_done()
        except queue.Empty:
            print(f"{queue.name} is empty. Waiting...")
            time.sleep(1)

# Create two queues
queue1 = queue.Queue()
queue2 = queue.Queue()
queue1.name = "Queue 1"
queue2.name = "Queue 2"

# Create distributor and consumer threads
distributor_thread = threading.Thread(target=number_distributor, args=(queue1, queue2))
consumer_thread1 = threading.Thread(target=number_consumer, args=(queue1,))
consumer_thread2 = threading.Thread(target=number_consumer, args=(queue2))

# Start the threads
distributor_thread.start()
consumer_thread1.start()
consumer_thread2.start()

# Wait for all threads to finish (you may use a different termination mechanism)
distributor_thread.join()
consumer_thread1.join()
consumer_thread2.join()
