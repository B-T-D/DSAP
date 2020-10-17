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

    def setUp(self):

        self.tree = RedBlackTreeMap()
        self.root_val = "value at initial root"
        self.val = "filler value"

        # DEBUG--Assert left/right/parent after each addition to confirm
        #   tree shape is as intended. 

        # Adding in the order depicted in figure 11.35 p.517
        self.tree[4] = self.root_val
        assert len(self.tree) == 1
        assert self.tree.root().key() == 4

        ## Adding the first two children:
        self.tree[7] = self.val
        assert len(self.tree) == 2
        # Should have gone in as right child:
        assert self.tree.right(self.tree.find_position(4)).key() == 7,\
        f"Actual right child was {self.tree.right(self.tree.find_position(4)).key()}"
        # And should be black
        assert self.tree._is_red(self.tree.find_position(7))

    
        self.tree[12] = self.val
            # ^ Should go in momentarily as 7's right child, then 7 should become root with 4 as
            #   7's left child.
        assert len(self.tree) == 3
        # Should initially go in as right child of 7
        pos12init = self.tree.right(self.tree.find_position(7))
        assert pos12init.key() == 12
        assert self.tree.root().key() == 7 # 7 should now be root
        assert self.tree.left(self.tree.root()).key() == 4 # 4 should be left child
        assert (self.tree._is_red(pos12init) and self.tree._is_red(self.tree.find_position(12)))
            # ^ Both children of root should be red

        ## Adding 15:
        self.tree[15] = self.val
        assert len(self.tree) == 4
        # Should be the right child of 12:
        assert self.tree.right(self.tree.find_position(12)).key() == 15
        assert self.tree._is_red(self.tree.find_position(15)) # 15 should be red

        ## Adding 3:
        self.tree[3] = self.val
        assert len(self.tree) == 5
        # Should be left child of 4:
        assert self.tree.left(self.tree.find_position(4)).key() == 3
        # And should be red:
        assert self.tree._is_red(self.tree.find_position(3))

        # Confirming tree is in order before attempting to add 5:
            # (confirming the tree looks like fig 11.35(g))
        assert not self.tree._is_red(self.tree.root()) # root should be black
        assert self.tree.root().key() == 7 # 7 should be at root
        assert not self.tree._is_red(self.tree.find_position(4)) # 4 should be black
        assert not self.tree._is_red(self.tree.find_position(12)) # 12 should be black
        assert self.tree.right(self.tree.root()).key() == 12 # 12 should still be right child of root
        assert self.tree.left(self.tree.root()).key() == 4 # 4 should still be left child

        assert self.tree.right(self.tree.find_position(4)) is None,\
        f"tree.right(pos4) expected None, actual {self.tree.right(self.tree.find_position(4)).key()}"

        ## Adding 5
        self.tree[5] = self.val



        ## Adding 14
        self.tree[14] = self.val

        ## Adding 18
        self.tree[18] = self.val

        ## Adding 16
        self.tree[16] = self.val

        ## Adding 17
        self.tree[17] = self.val

        assert len(self.tree) == 10
        assert self.tree.root().key() == 14

        first = self.tree.first()
        assert first.key() == 3
        assert self.tree._is_red(first) # 3 should be red

        last = self.tree.last()
        assert last.key() == 18
        assert not self.tree._is_red(last) # 18 should be black
        
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

##    def test_rebalance_delete_one_child(self):
##        initial_num_elements = len(self.tree)
##        # Where surviving parent has one child:
##        del self.tree[8]
##        self.assertEqual(initial_num_elements - 1, len(self.tree))

##    def test_rebalance_delete_two_children(self):
##        initial_num_elements = len(self.tree)
##        # Where surviving parent has two children:
##        del self.tree[5]
##        self.assertEqual(initial_num_elements - 1, len(self.tree))

    def test_delete_nonexistent_element(self):
        """Does attempting to delete a key that isn't in the tree raise
        KeyError?"""
        delete_me_key = 9001
        with self.assertRaises(KeyError):
            del self.tree[delete_me_key]

    def test_fix_deficit_case_2(self):
        initial_num_elements = len(self.tree)
        # Removal of key=18 should cause this, see Figure 11.41
        del self.tree[18]
        self.assertEqual(initial_num_elements - 1, len(self.tree))

        

if __name__ == '__main__':
    unittest.main()


