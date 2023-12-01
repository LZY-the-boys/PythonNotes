import ray
import time
import numpy as np

# Start Ray.
ray.init()

# “remote function” (a function that can be executed remotely and asynchronously)
@ray.remote
def f(x):
    time.sleep(1)
    import pdb; pdb.set_trace()
# the stack trace: cannot see starter
#   /home/lzy/miniconda3/envs/vllm/lib/python3.9/site-packages/ray/_private/workers/default_worker.py(278)<module>()
# -> worker.main_loop()
#   /home/lzy/miniconda3/envs/vllm/lib/python3.9/site-packages/ray/_private/worker.py(782)main_loop()
# -> self.core_worker.run_task_loop()
#   /home/lzy/lzy/PythonNotes/ray/ex1.py(11)f()
# -> return x 
    return x

@ray.remote
def create_matrix(size):
    return np.random.normal(size=size)

@ray.remote
def multiply_matrices(x, y):
    return np.dot(x, y)

@ray.remote
def add(x, y):
    time.sleep(1)
    return x + y

@ray.remote
class Counter(object):
    def __init__(self):
        self.x = 0
    
    def inc(self):
        self.x += 1
    
    def get_value(self):
        return self.x

@ray.remote
class MessageActor(object):
    def __init__(self):
        self.messages = []
    
    def add_message(self, message):
        self.messages.append(message)
    
    def get_and_clear_messages(self):
        messages = self.messages
        self.messages = []
        return messages


# Define a remote function which loops around and pushes
# messages to the actor.
@ray.remote
def worker(message_actor, j):
    for i in range(100):
        time.sleep(1)
        message_actor.add_message.remote("Message {} from worker {}.".format(i, j))


def ex1():
    # Start 4 tasks in parallel. (function with ray.remote == task)
    result_ids = []
    for i in range(4):
        result_ids.append(
            f.remote(i)
        )

        
    # Wait for the tasks to complete and retrieve the results.
    # With at least 4 cores, this will take 1 second.
    results = ray.get(result_ids)  # [0, 1, 2, 3]
    print(results)

def ex2():
    # the multiply_matrices task uses the outputs of the two create_matrix tasks, so it will not begin executing until after the first two tasks have executed. 
    # The outputs of the first two tasks will automatically be passed as arguments into the third task and the futures will be replaced with their corresponding values)
    x_id = create_matrix.remote([1000, 1000])
    y_id = create_matrix.remote([1000, 1000])
    z_id = multiply_matrices.remote(x_id, y_id)
    # Get the results.
    z = ray.get(z_id)
    print(z)

def ex3():
    # ref pic: ex3.jpeg
    # tasks can be composed together with arbitrary DAG dependencies.

    # Aggregate the values slowly. This approach takes O(n) where n is the
    # number of values being aggregated. In this case, 7 seconds.
    id1 = add.remote(1, 2)
    id2 = add.remote(id1, 3)
    id3 = add.remote(id2, 4)
    id4 = add.remote(id3, 5)
    id5 = add.remote(id4, 6)
    id6 = add.remote(id5, 7)
    id7 = add.remote(id6, 8)
    result = ray.get(id7)
    print(result)

    # Aggregate the values in a tree-structured pattern. This approach
    # takes O(log(n)). In this case, 3 seconds.
    id1 = add.remote(1, 2)
    id2 = add.remote(3, 4)
    id3 = add.remote(5, 6)
    id4 = add.remote(7, 8)
    id5 = add.remote(id1, id2)
    id6 = add.remote(id3, id4)
    id7 = add.remote(id5, id6)
    result = ray.get(id7)
    print(result)

    # Slow approach.
    values = [1, 2, 3, 4, 5, 6, 7, 8]
    while len(values) > 1:
        values = [add.remote(values[0], values[1])] + values[2:]
    result = ray.get(values[0])


    # Fast approach.
    values = [1, 2, 3, 4, 5, 6, 7, 8]
    while len(values) > 1:
        values = values[2:] + [add.remote(values[0], values[1])]
    result = ray.get(values[0])

def ex4():
    # Create an actor process. Individual actors execute methods serially (each individual method is atomic) so there are no race conditions. Parallelism can be achieved by creating multiple actors.
    # class with ray.remote = actor
    c = Counter.remote()

    # Check the actor's counter value.
    print(ray.get(c.get_value.remote()))  # 0

    # Increment the counter twice and check the value again.
    c.inc.remote()
    c.inc.remote()
    print(ray.get(c.get_value.remote()))  # 2

def ex5():
    # Create a message actor.
    message_actor = MessageActor.remote()

    # Start 3 tasks that push messages to the actor.
    [worker.remote(message_actor, j) for j in range(3)]

    # Periodically get the messages and print them.
    for _ in range(100):
        new_messages = ray.get(message_actor.get_and_clear_messages.remote())
        print("New messages:", new_messages)
        time.sleep(1)

if __name__ == "__main__":
    ex3()