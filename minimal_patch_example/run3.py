from unittest.mock import patch
import unittest
import ray
from run import Foo

def fake_bar(self):
    print("In fake method")
    assert True

class TestFooCase(unittest.TestCase):
    """Test cases for Foo module"""

    @patch("run.Foo.bar", new=fake_bar)
    def test_bar(self):
        Foo().bar()

    @patch("run.Foo.bar", new=fake_bar)
    def test_bar_remote(self):
        foo_actor = ray.remote(Foo).remote()
        obj_ref = foo_actor.bar.remote()
        ray.get(obj_ref)

if __name__ == '__main__':
    unittest.main()