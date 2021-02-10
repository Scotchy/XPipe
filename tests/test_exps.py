import unittest

from pipeml.client import connect
import pipeml
unittest.TestLoader.sortTestMethodsUsing = None

class TestExp(unittest.TestCase): 
    

    def setUp(self):
        self.path = "/"
        self.exp_name = "unittest"
        self.session = connect("http://localhost:5000")

    def test_exp(self):
        # Test create
        exp = self.session.start_run(self.path, self.exp_name)
        id_exp = exp.id
        
        # Test load
        exp = self.session.get_run(id_exp)
        self.assertEqual(exp.id, id_exp)
        self.assertEqual(exp.name, self.exp_name)

        # Test remove
        r = self.session.delete_run(id_exp)
        self.assertEqual(r["success"], True)
        load_exp = lambda : self.session.get_run(id_exp)
        self.assertRaises(ValueError, load_exp)