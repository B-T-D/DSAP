import unittest

from tree_map import TreeMap

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
