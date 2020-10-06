import unittest

from splay_tree_map import SplayTreeMap

class TestInitialization(unittest.TestCase):

    def test_init(self):
        test_tree = SplayTreeMap()
        self.assertIsInstance(test_tree,SplayTreeMap)

class TestSimpleSplayTree(unittest.TestCase):
    """Basic-functionality tests using a small SplayTreeMap instance with
    hardcoded entries created in setUp method."""
    # These only guarantee non-brokenness, they don't necessarily guarantee
    #   expected behavior and otherwise correct implementation of the ADT. 
    
    # same hardcoded test tree from test_avl_tree_map.py

    def setUp(self):
        # manually copied from the AVL tree tests, any changes will diverge.
        
        # Create the test tree with the hardcoded known keys.
        self.tree = SplayTreeMap()
        self.val = self.tree._Node("filler value") # general filler value
        self.root_key = 44
        self.root_val = self.tree._Node("root value")

        self.root = self.tree._add_root(self.tree._Item(self.root_key,
                                                        self.root_val))
        self.pos17 = self.tree._add_left(self.tree.root(),
                                         self.tree._Item(17, self.val))
        
        self.pos62 = self.tree._add_right(self.tree.root(),
                                          self.tree._Item(62, self.val))

        # Building the left subtree of root:
        self.tree._add_left(self.pos17, self.tree._Item(16, self.val))
        temp = self.tree._add_right(self.pos17, self.tree._Item(32, self.val))
            # need a temporary name by which to reference this new Position
        self.tree._add_left(temp, self.tree._Item(31, self.val))
        self.tree._add_right(temp, self.tree._Item(33, self.val))

        # Building right subtree of root:
            # Subtree rooted at left child 50:
        temp1 = self.tree._add_left(self.pos62, self.tree._Item(50, self.val))
        temp2 = self.tree._add_left(temp1, self.tree._Item(48, self.val))
        self.tree._add_left(temp2, self.tree._Item(47, self.val))
        self.tree._add_right(temp2, self.tree._Item(49, self.val))
        temp2 = self.tree._add_right(temp1, self.tree._Item(54, self.val))
        self.tree._add_left(temp2, self.tree._Item(53, self.val))
        self.tree._add_right(temp2, self.tree._Item(55, self.val))
            # Subtree rooted at right child 78:
        temp1 = self.tree._add_right(self.pos62, self.tree._Item(78, self.val))
        self.tree._add_left(temp1, self.tree._Item(77, self.val))
        temp1 = self.tree._add_right(temp1, self.tree._Item(88, self.val))
        self.val87 = "value at 87"
        self.pos87 = self.tree._add_left(temp1, self.tree._Item(87, self.val87))
        self.pos89 = self.tree._add_right(temp1, self.tree._Item(89, self.val))

    def test_insertion(self): # "coverage"s all of _splay except zig-zag case
        inserted_key = 90
        self.tree[inserted_key] = self.val
        last_key = self.tree._subtree_last_position(self.tree.root()).key()
        # 90 should be the greatest key in the tree at this point. 
        self.assertEqual(inserted_key, last_key)
        # 90 should have been splayed up to become root
        expected_root_key = 90
        actual_root_key = self.tree.root().key()
        self.assertEqual(expected_root_key, actual_root_key)

    def test_splay_zig_zag_case(self):
        # self.pos87 is a left child, its parent (key=88) is a right child.

        # calling getitem(key = 87) should cause _rebalance_access(self.pos87) to
        #   be called
        accessed_val = self.tree[87]
        assert accessed_val == self.val87

        # Position with key=87 should have been splayed up to root
        expected_root_key = self.pos87.key()
        actual_root_key = self.tree.root().key()
        self.assertEqual(expected_root_key, actual_root_key)

    def test_deletion(self):
        """On deletion of a position, does the data structure splay the deleted
        position's parent such that it becomes the root of the full tree?"""

        # If key=87 is deleted, key=88 should become root
        self.tree.delete(self.pos87)
        expected_root_key = 88
        actual_root_key = self.tree.root().key()
        self.assertEqual(expected_root_key, actual_root_key)
        
        
        
        
        

if __name__ == '__main__':
    unittest.main()
