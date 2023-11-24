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