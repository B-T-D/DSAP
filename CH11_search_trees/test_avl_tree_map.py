

import unittest

from avl_tree_map import AVLTreeMap

class TestBasics(unittest.TestCase):

    def test_init(self):
        """Can an AVLTreeMap instance be initialized?"""
        test_tree = AVLTreeMap()
        self.assertIsInstance(test_tree, AVLTreeMap)

class TestSimpleAVLTree(unittest.TestCase):
    """Basic-functionality tests using a small AVLTreeMap instance with specific
    hardcoded values for entries."""
    # page 484 diagram. Same tree as TreeMap example but rebalanced to comply
    #   with height-balance property so can be AVL tree. 

    def setUp(self):
        # Create the test tree with the hardcoded known keys.
        self.tree = AVLTreeMap()
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
        self.tree._add_left(temp1, self.tree._Item(87, self.val))
        self.pos89 = self.tree._add_right(temp1, self.tree._Item(89, self.val))
        

    def test_left_height_init_to_zero(self):
        # The height isn't initialized to the correct value, it's initialized
        #   to zero and only set to the real value on the first _recompute_height
        #   call. 
        self.assertEqual(0, self.tree.root()._node.left_height())

    def test_right_height(self):
        """Doest the right height initially return zero when called before
        a _recompute_height event?"""
        self.assertEqual(0, self.tree.root()._node.right_height())

    def test_recompute_height(self):
        """Does manually calling _recompute_height on root set that node's
        height to the tree's height?"""
        expected_tree_height = 1
        self.tree._recompute_height(self.tree.root())
        # left vs right doesn't matter, recompute height sets the height to
        #    max of left and right (per definition of height, you take the
        #   longest path to a leaf).
        self.assertEqual(expected_tree_height,
                         self.tree.root()._node._height)

    def test_isbalanced_returns_true(self):
        """Does the method return True when the subtree rooted at the position
        arg is balanced?"""
        position = self.tree.root()
        self.assertTrue(self.tree._isbalanced(position))

    def test_isbalanced_returns_false(self):
        """Does the method return False when called with a position that is
        the root of an unbalanced subtree?"""
        unbalanced_tree = AVLTreeMap()
        unbalanced_tree._add_root(unbalanced_tree._Item(10,
                                                        self.val))
        left_child = unbalanced_tree._add_left(unbalanced_tree.root(),
                                  unbalanced_tree._Item(7, self.val))
        right_child = unbalanced_tree._add_right(unbalanced_tree.root(),
                                    unbalanced_tree._Item(12, self.val))
        left_grandchild = unbalanced_tree._add_left(left_child,
                                  unbalanced_tree._Item(6, self.val))
        great_grandchild = unbalanced_tree._add_right(left_grandchild,
                                   unbalanced_tree._Item(8, self.val))
        # Manually recompute heights in starting with most recently added
        #   (bottom) and working up toward root.
        unbalanced_tree._recompute_height(great_grandchild)
        unbalanced_tree._recompute_height(left_grandchild)
        unbalanced_tree._recompute_height(right_child)
        unbalanced_tree._recompute_height(left_child)
        unbalanced_tree._recompute_height(unbalanced_tree.root())
        assert unbalanced_tree.root()._node._height == 4 # meant to be 4
        
        self.assertFalse(unbalanced_tree._isbalanced(unbalanced_tree.root()))

    def test_tall_child_favor_right(self):
        """Does the method return the right child when there's a tie, when
        called with default arg favorleft=False?"""
        # Left and right children of root are both height 3 in the test tree,
        #   so the method should return the right child, self.pos62
        self.assertEqual(self.pos62, self.tree._tall_child(self.tree.root()))

    def test_tall_child_favor_left(self):
        """Does the method return the left child when both left and right are
        same height and called with favorleft=True?"""
        # Left child of root is self.pos17
        self.assertEqual(self.pos17,
                         self.tree._tall_child(self.tree.root(),
                                               favorleft=True))

    def test_tall_grandchild(self):
        # 62 is right child of its parent, so _tall_grandchild should return
        #   its right-right grandchild, key=88
        expected = 88
        actual = self.tree._tall_grandchild(self.pos62).key()
        self.assertEqual(expected, actual)

    def test_delete(self):
        """Does the parent class's delete method, combined with the overridden
        rebalance hooks, rebalance after deletion?"""
        self.tree.delete(self.pos62)
        self.assertTrue(self.tree._isbalanced(self.tree.root()))

    def test_insert(self):
        """Does the parent class's insert method, combined with the overridden
        rebalance hooks, rebalance after an insertion?"""
        # Inserting a child and grandchild of one of 88's children would make
        #   root's children unbalanced. Right would have height 5.
        temp = self.tree._add_right(self.pos89,
                                    self.tree._Item(90, self.val))
        self.tree._add_right(temp, self.tree._Item(91, self.val))
        self.assertTrue(self.tree._isbalanced(self.tree.root()))
        self.tree[92] = self.val
        

    
        

    
        

    

    
    

if __name__ == '__main__':
    unittest.main()
