from thing import Thing
# import unittest
# from unittest.mock import patch
from _mock import patch
_thing = Thing()

def fetch_thing2():
    print('new')
    return 1

# 1. wrong , have been imported
with patch('run.fetch_thing', fetch_thing2):
    data = _thing.run()

# handicraft
import run
run.fetch_thing = fetch_thing2
data = _thing.run()   

# 2. right
with patch('thing.fetch_thing', fetch_thing2) as mocked:
    data = _thing.run()

# handicraft
import thing
thing.fetch_thing = fetch_thing2
data = _thing.run()

# 3. however, when in multi-process scenaries it's useless because the process isolation 
# When using ray.remote to create and run actors, 
# the code for the remote actor is executed in a separate Python interpreter within the Ray worker process. Since the mock.patch is applied in the main process, it won't be able to patch objects inside the remote actor processes.
# simple patch can work ( in run3.py )
import ray
import thing
thing.fetch_thing = fetch_thing2
foo_actor = ray.remote(Thing).remote()
obj_ref = foo_actor.run.remote()
ray.get(obj_ref)


import ray
from thing import Thing
from _mock import patch
_thing = Thing()
def fetch_thing2():
    print('new')
    return 1
with patch('thing.fetch_thing', fetch_thing2) as mocked:
    foo_actor = ray.remote(Thing).remote()
    obj_ref = foo_actor.run.remote()
    ray.get(obj_ref)

