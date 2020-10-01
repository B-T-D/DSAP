import sys, os

this_directory = os.path.dirname(__file__)
ch8_directory = '../CH8_trees' # for LinkedBinaryTree
ch10_directory = '../CH10_maps_hash_tables' # for MapBase
sys.path.insert(0, os.path.abspath(ch8_directory))
sys.path.insert(1, os.path.abspath(ch10_directory))

import unittest

from tree_map import TreeMap

class TestBasics(unittest.TestCase):
    """Most-basic tests that don't even use a mock tree object."""

    def test_init(self):
        """Can an instance of a TreeMap object be initialized?"""
        test_tree = TreeMap()
        self.assertIsInstance(test_tree, TreeMap)

class TestSimpleTreeMap(unittest.TestCase):
    """Quick basic-functionality tests using a simple instance of a TreeMap
        object.
    """

    # The tree is the one from DSAP 463 figure 11.2(a). With root 44, "first"
    #   (min value leftmost external node) 8, "last" 97. 
    
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()
