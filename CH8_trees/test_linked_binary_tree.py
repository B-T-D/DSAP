# Also need to test the public methods inherited from the abstract classes,
#   e.g. height and depth are public and defined in tree abstract base class,
#   but couldn't easily be tested there because they'd have interacted with
#   other abstract methods not yet implemented (if they were in Tree's tests).

import unittest

from linked_binary_tree import LinkedBinaryTree

class TestSimpleCases(unittest.TestCase):
    """
    Test obvious cases to confirm basic functionality and syntax
    correctness.
    """

    def setUp(self):
        self.tree = LinkedBinaryTree()
        # Create a proper balanced tree with 3 levels (8 elements)
        self.root = self.tree._add_root("Root")
        self.left = self.tree._add_left(self.root, "L2 left child")
        self.right = self.tree._add_right(self.root, "L2 right child")
        self.lev3_first_left = self.tree._add_left(self.left, "L3 left-1")
        self.tree._add_right(self.left, "L3 right-1")
        self.tree._add_left(self.right, "L3 left-2")
        self.tree._add_right(self.right, "L3 right-2")

    def test_validate(self):
        # Passing an object of type other than Position should raise TypeError
        with self.assertRaises(TypeError):
            self.tree._validate("spam")
        # Wrong container should raise value error
        position_from_other_container = LinkedBinaryTree()._add_root("spam root")
        with self.assertRaises(ValueError):
            self.tree._validate(position_from_other_container)
        # If node was deprecated, meaning it was set to be its own parent per
        #   the internal convention for deprecated nodes, then should raise
        #   value error.
        p = self.lev3_first_left
        p._node._parent = p._node
        with self.assertRaises(ValueError):
            self.tree._validate(p)



    # ---------------------------------- public methods --------------------
     
    def test_root(self):
        blank_tree = LinkedBinaryTree()
        root = blank_tree.root()
        self.assertEqual(root, None) # Should return None for an empty tree.
        root = self.tree.root()
        self.assertEqual(root.element(), "Root")

    def test_parent(self):
        # should return None when called on p = root
        parent_of_root = self.tree.parent(self.tree.root())
        self.assertEqual(parent_of_root, None)
        parent_of_left = self.tree.parent(self.left) # Position object from
                                            # setUp, name self.left references
                                            # root's left child.
        self.assertEqual(parent_of_left, self.root)
        # Try the next level down
        parent_of_node = self.tree.parent(self.lev3_first_left)
        self.assertEqual(parent_of_node, self.left)

    def test_left(self):
        left = self.tree.left(self.root) # parent's left should be the object
                                        #   stored as self.left
        self.assertEqual(left, self.left)

    def test_right(self):
        right = self.tree.right(self.root) # root's right should be the object
                                            # stored as self.right
        self.assertEqual(right, self.right)

    def test_num_children(self):
        self.assertEqual(self.tree.num_children(self.root), 2) # Root has 2 children
        self.assertEqual(self.tree.num_children(self.right), 2) # Right has 2
        self.assertEqual(
            self.tree.num_children(self.lev3_first_left), 0) # This node should be in the
                                                     # bottom level of the setUp
                                                     # tree and therefore have
                                                        # no children.

    # ------------------- tests for concrete methods inherited from Tree ------

    def test_is_root(self):
        """Concrete method implemented in the Tree abstract base class and
        inherited through to LBT class."""
        # Should be true for root
        self.assertTrue(self.tree.is_root(self.root))
        # Should be false for a node from the middle or bottom layer
        self.assertFalse(self.tree.is_root(self.right))
        self.assertFalse(self.tree.is_root(self.lev3_first_left))

    def test_is_leaf(self):
        # testing _attach will "coverage" this
        pass

    def test_is_empty(self):
        # testing _attach will "coverage this
        pass
        
    def test_height(self):
        """
        Test the height method defined in the Tree abstract base class
        that LBT class has through inheritance.
        """
        # Calling it on root should return 2, the height of the full three-level
        #   tree.
        self.assertEqual(self.tree.height(self.root), 2)
        # Height of a node in the middle layer should be 1
        self.assertEqual(self.tree.height(self.right), 1)
        # Height of a node in the bottom layer should be 0
        self.assertEqual(self.tree.height(self.lev3_first_left), 0)

    def test_depth(self):
        """
        Test the depth method defined in the Tree abstract base class and
        inherited in the LBT class.
        """
        # Depth of a node in the bottom later should be 2 (2 levels separating
        #   that Position from root Position).
        self.assertEqual(self.tree.depth(self.lev3_first_left), 2)
        # Depth of node in middle layer should be 1
        self.assertEqual(self.tree.depth(self.left), 1)
        # Depth of root should be zero
        self.assertEqual(self.tree.depth(self.root), 0)

    def test_attach(self):
        """Tests for the nonpublic _attach method, mainly to hit inherited public
        methods that it will call."""
        new_tree = LinkedBinaryTree()
        ntroot = new_tree._add_root("New tree root")
        new_tree._add_left(ntroot, "NT left")
        new_tree._add_right(ntroot, "NT right")
        new_tree2 = LinkedBinaryTree()
        nt2root = new_tree2._add_root("2nd new tree root")
        new_tree2._add_left(nt2root, "left")
        new_tree2._add_right(nt2root, "right")
        self.tree._attach(self.lev3_first_left, new_tree, new_tree2)
        # For now just pass if none of these calls raised an error, no
        #   unittest.assertSomething method call

    def test_positions(self): # This covers postorder() method for purposes
                                # of the "coverage" metric.
        for position in self.tree.positions(): # Test that they can be iterated
            self.assertIsInstance(position, LinkedBinaryTree.Position) # and that
                                                        # they're all Positions

##    def test_preorder(self): # placeholder
##        pass

    def test_postorder(self):
        for position in self.tree.postorder():
            self.assertIsInstance(position, LinkedBinaryTree.Position)
        # TODO: This only tests that the iterator works, doesn't prove that the
        #   nodes are being visited in the intended order.
        
class TestTraversalMethods(unittest.TestCase):
    # Separate class with a setUp tree designed for easy testing of intended
    #   traversal order.

    def setUp(self):
        self.tree = LinkedBinaryTree()
        self.root = self.tree._add_root(1)
        self.element2 = self.tree._add_left(self.root, 2)
        self.element3 = self.tree._add_right(self.root, 3)
        self.element4 = self.tree._add_left(self.element2, 4)
        self.element5 = self.tree._add_right(self.element2, 5)
        self.element6 = self.tree._add_left(self.element3, 6)
        self.element7 = self.tree._add_right(self.element3, 7)

    def test_preorder(self):
        visits_expected = [1, 2, 4, 5, 3, 6, 7]
        visits_actual = [] * 7 # List to store the visits in the order they happened
        for position in self.tree.preorder():
            visits_actual.append(position.element())
        self.assertEqual(visits_actual, visits_expected)

    def test_postorder(self):
        visits_expected = [4,5,2,6,7,3,1]
        visits_actual = [] * 7 # List to store the visits in order
        for position in self.tree.postorder():
            visits_actual.append(position.element())
        self.assertEqual(visits_actual, visits_expected)

    def test_breadthfirst(self):
        visits_expected = [1, 2, 3, 4, 5, 6, 7]
        visits_actual = [] * 7
        for position in self.tree.breadthfirst():
            visits_actual.append(position.element())
        self.assertEqual(visits_actual, visits_expected)

##    def test_parenth_print(self):
##        # putting here for expediency, not meant as a proper test of that method
##        #   (which isn't even nec meant to be in the LBT class)
##        self.tree.parenthesize(self.root)
        
    
        
if __name__ == '__main__':
    unittest.main()
