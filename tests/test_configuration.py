from unittest import TestCase

from os.path import dirname, realpath, join
from pipeml.config import load_config
import numpy as np

class TestConfiguration(TestCase):

    def setUp(self):
        dir_path = dirname(realpath(__file__))
        self.conf = load_config(join(dir_path, "./template.yaml"))

    def test_get_integer(self):
        self.assertEqual(
            self.conf.training.batch_size(), 
            10
        )

    def test_get_list(self):
        l = self.conf.training.classes()
        self.assertIsInstance(l, list)
        self.assertListEqual(l, [0,1,2,3,4])

    def test_instantiate_object(self):
        ar = self.conf.training.obj()
        self.assertIsInstance(ar, np.ndarray)
        self.assertListEqual(list(ar), [1,2])

    def test_get_object_parameter(self):
        self.assertListEqual(
            self.conf.training.obj.params.object(), 
            [1, 2]
        )

    def test_instantiate_list_objects(self):
        pass