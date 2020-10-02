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
        self.tree = TreeMap()
        self.val = self.tree._Node("filler value") # filler value
            # NB these keys must be numbers (or else ._node objects?)
    
        self.root_key = 44
        self.root_val = self.tree._Node("root value")
        self.root = self.tree._add_root(self.tree._Item(self.root_key, self.root_val))

        # First layer: 44 with children 17 and 88
        self.pos17 = self.tree._add_left( # Todo this shouldn't be necessary
            self.tree.root(), self.tree._Item(17, self.val)) # setitem is supposed to know left vs right
        self.pos88 = self.tree._add_right(
            self.tree.root(), self.tree._Item(88, self.val))

        # Children of 17: 8 and 32
        self.pos8 = self.tree._add_left(
            self.pos17, self.tree._Item(8, self.val))
        self.pos32 = self.tree._add_right(
            self.pos17, self.tree._Item(32, self.val))

        # Children of 88: 65 and 97
        self.val_65 = self.tree._Node("value at key 65")
        self.tree[65] = self.val_65
        self.tree[97] = self.tree._Node("value at key 97")

    ### TreeMap.__getitem__

    def test_getitem(self):
        """Does TM's __getitem__ method return the value associated with
        a key?"""
        expected = self.root_val
        self.assertEqual(expected, self.tree[self.root_key])

    def test_getitem_for_external_setitem_call(self):
        """Does getitem return the expected value for an item that was added
        through dictionary-style syntax rather than by directly calling
        internal setter methods?"""
        expected = self.val_65
        self.assertEqual(expected, self.tree[65])

    def test_getitem_raises_key_error_for_empty(self):
        """ Does __getitem__ raise KeyError when called on an empty tree?"""
        empty_tree = TreeMap()
        with self.assertRaises(KeyError):
            item = empty_tree[12] 

    def test_getitem_raises_key_error(self):
        """Does __getitem__ raise KeyError when called with a key that isn't
        in the tree?"""
        with self.assertRaises(KeyError):
            item = self.tree[9001]

    ### TreeMap.__setitem__
            
    def test_setitem_adds_root(self):
        """Does __setitem__ correctly add the tree's root when called on an
        empty tree?"""
        empty_tree = TreeMap()
        test_key = 12
        empty_tree[test_key] = "test value"
        self.assertEqual(test_key, empty_tree.root().key())

    ### TreeMap._subtree_search
        
    def test_subtree_search_left_case(self):
        # subtree search for key k=8 on subtree from position with key=17 should
        #   return Position of 8.
        expected = self.pos8
        actual = self.tree._subtree_search(p=self.pos17, k=8)
        self.assertEqual(expected, actual)

    def test_subtree_search_right_case(self):
        expected = self.pos32
        actual = self.tree._subtree_search(p=self.pos17, k=32)
        self.assertEqual(expected, actual)

    def test_subtree_search_no_match(self):
        """Does the method return the subtree's root position when the searched-
        for key isn't in the subtree?"""
        expected = self.pos32
        actual = self.tree._subtree_search(p=self.pos17, k=9001)
        self.assertEqual(expected, actual)

    ### TreeMap._subtree_first_position

    def test_subtree_first_position_full_tree(self):
        """Does it correctly return 8, the minimum value in this test tree?"""
        expected = self.pos8
        actual = self.tree._subtree_first_position(self.tree.root())
        self.assertEqual(expected, actual)

    def test_subtree_first_position_not_tree_min(self):
        # Todo test will break if more layers added to build the full tree
        #   from the diagram. 
        """When called on a subtree that isn't root, and whose "last" key
        is greater than the full tree's last, does the method correctly return
        the subtree last?"""
        # Min for subtree at 88 is 65
        expected = 65
        actual = self.tree._subtree_first_position(self.pos88).key()
            # Call key() method to return the actual int rather than a position
            #   object.
        self.assertEqual(expected, actual)

    ### TreeMap._subtree_last_position

    def test_subtree_last_position_full_tree(self):
        """When called on the full tree, does the method return the key with the
        max value in the tree?"""
        # max is 97 right now
        expected = 97
        actual = self.tree._subtree_last_position(self.tree.root()).key()
        self.assertEqual(expected, actual)

    def test_subtree_first_position_not_tree_max(self):
        """When called on a subtree whose "last" isn't the same as the full tree's
        last, does the method correctly return the subtree's last?"""
        # max on the 17 subtree is 32
        expected = 32
        actual = self.tree._subtree_last_position(self.pos17).key()
        self.assertEqual(expected, actual)

    ###

    def test_first(self):
        """Does the method return the first position in the tree?"""
        expected = self.pos8
        actual = self.tree.first()
        self.assertEqual(expected, actual)

    def test_last(self):
        """Does the method return the last position in the full tree?"""
        expected = 97
        actual = self.tree.last().key()
        self.assertEqual(expected, actual)

    ### TreeMap.before

    def test_before_root(self):
        """Does the method correctly return the position just before root
        when called on root?"""
        expected = 32
        actual = self.tree.before(self.tree.root()).key()
        self.assertEqual(expected, actual)

    def test_before_first(self):
        """Does the method return None when called with the first position?"""
        self.assertIsNone(self.tree.before(self.tree.first()))

    ### TreeMap.after

    def test_after_root(self):
        expected = 65
        assert self.tree.root().key() == 44
        actual = self.tree.after(self.tree.root()).key()
        self.assertEqual(expected, actual)

    def test_after_last(self):
        """Does the method return None when called with the last position?"""
        self.assertIsNone(self.tree.after(self.tree.last()))

    ###
    def test_find_position_root(self):
        """Does the method return root when called with root's key?"""
        self.assertEqual(self.tree.root(), self.tree.find_position(44))

    def test_find_position_midlevel(self):
        """Does the method return the correct key when called with the key
        of an internal node with two children?"""
        self.assertEqual(self.pos17, self.tree.find_position(17))

    def test_find_position_leaf(self):
        """Does the method return the correct key when called with a leaf?"""
        self.assertEqual(self.pos8, self.tree.find_position(8))

    def test_find_position_empty(self):
        """Does the method return None when called on an empty tree?"""
        empty_tree = TreeMap()
        self.assertIsNone(empty_tree.find_position(44))

    ###
    def test_find_min(self):
        val_8 = self.tree._Node("value at 8")
        self.tree[8] = val_8 # put a distinct value at 8
        expected = (8, val_8)
        self.assertEqual(expected, self.tree.find_min())

    def test_find_min_empty(self):
        """Does the method return None when called on an empty tree?"""
        empty_tree = TreeMap()
        self.assertIsNone(empty_tree.find_min())

    ### TreeMap.find_ge
    def test_find_ge_no_exact_match(self):
        # Least key greater than or equal to 45 should be 65
        expected = (65, self.tree.find_position(65).value())
        self.assertEqual(expected, self.tree.find_ge(45))

    def test_find_ge_first_pos_tried_less_than_k(self):
        # Searching for ge 31 should land on 32, via 32's parent 17
        expected = (32, self.tree.find_position(32).value())
        self.assertEqual(expected, self.tree.find_ge(31))

    def test_find_ge_target_would_become_last(self):
        """Does the method return None when there's no existing key in the
        tree greater than or equal to the search target?"""
        self.assertIsNone(self.tree.find_ge(98))

    def test_find_ge_empty(self):
        """Does the method return None when called on an empty tree?"""
        empty_tree = TreeMap()
        self.assertIsNone(empty_tree.find_ge(44))

    ### TreeMap.find_range

    def test_find_range_full_tree(self):
        """Does the method iterate over all key-value pairs in the tree when
        both start and stop are None?"""
        count = 0
        for node in self.tree.find_range():
            self.assertIsInstance(node, tuple)
                                    # Just a rando thing to do to each, point
                                    # here is to confirm they can all be iterated
                                    # over, IMU no need to do anything fancy on
                                    # successfully touching each.
            count += 1
        self.assertEqual(len(self.tree), count) # Confirm actually touched all

    def test_find_range_root_is_start(self):
        # If iteration starts at root with key=44, then it should iterate over
        #    a total of 4 nodes given the setup of the hardcoded test tree.
        #   That is, keys 44, 65, 88, and 97
        count = 0
        expected_keys = [44, 65, 88, 97]
        actual_keys = []
        for node in self.tree.find_range(start=44):
            actual_keys.append(node[0])
            count += 1
        self.assertEqual(expected_keys, actual_keys)
        self.assertEqual(4, count)

    def test_find_range_root_is_stop(self):
        # If iteration stops at root of this hardcoded test tree, then it
        #   should iterate over a total of 3 elements. Keys 8, 17 and 32.
        #   It won't reach the "stop" value, same as builtin Python range.
        count = 0
        expected_keys = [8, 17, 32]
        actual_keys = []
        for node in self.tree.find_range(stop=44):
            actual_keys.append(node[0])
            count += 1
        self.assertEqual(expected_keys, actual_keys)
        self.assertEqual(3, count)

    def test_find_range_start_not_exact_match(self):
        """Does the method behave as intended when the start value isn't equal
        to any actual key in the tree?"""
        # In the hardcoded test tree, start value of 40 should yield same elements
        #   as starting at 44.
        start = 40
        count = 0
        expected_keys = [44, 65, 88, 97]
        actual_keys = []
        for node in self.tree.find_range(start):
            actual_keys.append(node[0])
            count += 1
        self.assertEqual(expected_keys, actual_keys)
        self.assertEqual(4, count)

    ###
    def test_iter(self):
        """Does __iter__ method yield the keys in order?"""
        expected_keys = [8, 17, 32, 44, 65, 88, 97]
        actual_keys = []
        for key in self.tree:
            actual_keys.append(key)
        self.assertEqual(expected_keys, actual_keys)

    ###
    def test_delete(self):
        # If 44 is deleted, 32 should become the new root
        del self.tree[44]
        self.assertEqual(32, self.tree.root().key())

    def test_delete_raises_key_error(self):
        """Does delete method raise KeyError when called with a nonexistent
        key?"""
        with self.assertRaises(KeyError):
            del self.tree[9001]
    
if __name__ == '__main__':
    unittest.main()
