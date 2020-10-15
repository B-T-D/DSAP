import unittest

from red_black_tree_map import RedBlackTreeMap

class TestFoundationalCases(unittest.TestCase):
    """Basic-functionality tests that don't require a large test tree."""

    def test_set_color(self):
        tree = RedBlackTreeMap()
        tree[1] = "test value"
        assert tree.root().key() == 1
        tree._set_color(tree.root(), make_red=True)
        # Root should have been black by default; this should manually turn
        #   it red breaking the correct RBT properties.
        self.assertEqual(True, tree.root()._node._red)
        # Calling set color again with make_red=False should set it back to
        #   black:
        tree._set_color(tree.root(), make_red=False)
        self.assertEqual(False, tree.root()._node._red)

    def test_is_red_leaf(self):
        # The first child of root in a fresh tree should be a red leaf.
        tree = RedBlackTreeMap()
        tree[1] = "test value"
        tree[2] = "a value at child"
        self.assertEqual(True, tree._is_red_leaf(tree.right(tree.root())))

    def test_get_red_child(self):
        tree = RedBlackTreeMap()
        tree[1] = "test value"
        child_value = "a value at child"
        tree[2] = child_value
        # Calling get red child with root as it's position argument should
        #   return a position with key and value matching root's child's
        #   key and value.
        self.assertEqual(child_value,
                         tree._get_red_child(tree.root()).value())
        # Calling with the child as the position argument should return None
        #   since that child has no red child or any other child.
        child_pos = tree._get_red_child(tree.root())
        self.assertIsNone(tree._get_red_child(child_pos))

class TestSimpleRedBlackTree(unittest.TestCase):
    """Basic-functionality tests using small RedBlackTreeMap instance with
    hardcoded entries created in SetUp method."""
    # Test tree is running example at e.g. 532 figure 11.41(a)

    def setUp(self):

        self.tree = RedBlackTreeMap()
        self.root_val = self.tree._Node("value at initial root (key=4)")
        self.val = self.tree._Node("filler value") # general filler value

        # Adding in the order depicted in figure 11.35 p.517
        self.tree[4] = self.root_val
        assert len(self.tree) == 1

        self.tree[7] = self.val
        assert len(self.tree) == 2

        self.tree[12] = self.val
        assert len(self.tree) == 3
        
        self.tree[15] = self.val
        assert len(self.tree) == 4
        
        self.tree[3] = self.val
        assert len(self.tree) == 5

        self.tree[8] = self.val # TODO why does key=5 cause recursion depth
                                #   error??
##        self.tree[5] = self.val
##        assert len(self.tree) == 6

        self.tree[14] = self.val

        self.tree[18] = self.val

        self.tree[16] = self.val
        # TODO key=16 also causes the recursion error. It's about where it's
        #   being inserted in the tree, not what the key is specifically.

        self.tree[17] = self.val

        
    def test_init(self):
        self.assertIsInstance(self.tree, RedBlackTreeMap)

    def test_setitem_new_key(self):
        value = "new key's value"
        new_key = 20
        self.tree[new_key] = value
        self.assertEqual(value, self.tree[new_key])

    def test_delete_root(self):
        initial_num_elements = len(self.tree)
        # Get key of whatever node is currently at root
        delete_me_key = self.tree.root().key()
        # Then call delete() on that key:
##        self.tree.delete(delete_me_key)
        del self.tree[delete_me_key]
        # Assert len decreased by one, just so that there's a unittest assert
        #   method to call:
        self.assertEqual(initial_num_elements - 1, len(self.tree))

    def test_delete_leaf(self):
        initial_num_elements = len(self.tree)

        # Highest-numbered key should always be a leaf
        delete_me_key = self.tree.last().key()
        del self.tree[delete_me_key]
        self.assertEqual(initial_num_elements - 1, len(self.tree))

    def test_delete_root_where_len_is_one(self):
        """Does the delete method behave as intended in the special case where
        the surviviing tree has only one element?"""
        tree = RedBlackTreeMap()
        tree[1] = "root"
        tree[2] = "child" # this child should be red
        del tree[tree.root().key()]
        self.assertEqual(False, tree.root()._node._red) # The rebalance delete
            #   method should set root to black

    def test_rebalance_delete_one_child(self):
        initial_num_elements = len(self.tree)
        # Where surviving parent has one child:
        del self.tree[8]
        self.assertEqual(initial_num_elements - 1, len(self.tree))

    def test_rebalance_delete_two_children(self):
        initial_num_elements = len(self.tree)
        # Where surviving parent has two children:
        del self.tree[15]
        self.assertEqual(initial_num_elements - 1, len(self.tree))

    def test_fix_deficit_case_2(self):
        initial_num_elements = len(self.tree)
        # Removal of key=18 should cause this, see Figure 11.41
        del self.tree[18]
        self.assertEqual(initial_num_elements - 1, len(self.tree))

        

if __name__ == '__main__':
    unittest.main()


