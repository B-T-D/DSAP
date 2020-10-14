import unittest

from red_black_tree_map import RedBlackTreeMap

class TestSimpleRedBlackTree(unittest.TestCase):
    """Basic-functionality tests using small RedBlackTreeMap instance with
    hardcoded entries created in SetUp method."""
    # Test tree is running example at e.g. 532 figure 11.41(a)

    def setUp(self):
        self.tree = RedBlackTreeMap()
        self.val = self.tree._Node("filler value") # general filler value

        # Add root with key 14
        self.root_key = 14
        self.root_val = "root value"
        self.root = self.tree._add_root(self.tree._Item(self.root_key,
                                                        self.root_val))

        # Add root's children 7 and 16
        self.pos7 = self.tree._add_left(self.tree.root(),
                                        self.tree._Item(7, self.val))
        self.pos16 = self.tree._add_right(self.tree.root(),
                                          self.tree._Item(16, self.val))

    def test_init(self):
        self.assertIsInstance(self.tree, RedBlackTreeMap)

if __name__ == '__main__':
    unittest.main()


