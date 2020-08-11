import unittest
import random

from tic_tac_toe.general_tree import GeneralTree

class TestNode(unittest.TestCase):
    """Tests for the _Node nested nonpublic class."""

    def setUp(self):
        self.test_node = GeneralTree._Node("Test element")

    def test_init(self):
        """Confirm that a _Node object can be initialized."""
        self.assertIsInstance(self.test_node, GeneralTree._Node)

    def test_children_datatype(self):
        """Confirm that the children instance variable is a list."""
        self.assertIsInstance(self.test_node._children, list)
        
class TestPosition(unittest.TestCase):
    """Tests for the Position nested class."""

    def setUp(self):
        self.test_element = "Test element"
        self.node = GeneralTree._Node(self.test_element)
        container = [] # Temporary. Just needs something to pass as container 
        self.test_position = GeneralTree.Position(container, self.node)

    def test_init(self):
        self.assertIsNotNone(self.test_position)
        self.assertIsInstance(self.test_position, GeneralTree.Position)

    def test_element(self):
        """Confirm that the element() method returns the test element's
        string data."""
        self.assertEqual(self.test_position.element(), "Test element")

    def test_eq(self):
        """Confirm that the __eq__ operator overloader method works as
        intended."""
        # create new position with object as its node:
        other_container = []
        new_position = GeneralTree.Position(other_container, self.node)
        self.assertEqual(self.test_position, new_position)

class TestValidate(unittest.TestCase):
    """Tests for the _validate utility method."""

    def setUp(self):
        self.tree = GeneralTree()
        self.root = self.tree._add_root("Root element")
        for i in range(3):
            self.tree._add_child(self.tree.root(), i)

    def test_not_a_position(self):
        """Does _validate raise TypeError when "p" is not a Position object?"""
        with self.assertRaises(TypeError):
            self.tree._validate("spam")

    def test_wrong_container(self):
        """Does _validate raise ValueError when "p" is a Position object from
        a container other than the tree instance whose _validate method is being
        called?"""
        position_from_other_container = GeneralTree()._add_root("spam root")
        with self.assertRaises(ValueError):
            self.tree._validate(position_from_other_container)

    def test_node_is_own_parent(self):
        """Does _validate raise ValueError when the _Node corresponding to Position
        "p" is its own parent (the convention for a deprecated node)?"""
        position = self.tree._add_child(self.tree.root(),
                                        "deprecated node's element")
        position._node._parent = position._node
        with self.assertRaises(ValueError):
            self.tree._validate(position)
        

class TestTreeConstructors(unittest.TestCase):
    """Test __init__ and add_root."""

    def setUp(self):
        self.test_tree = GeneralTree()

    def test_init(self):
        self.assertIsInstance(self.test_tree, GeneralTree)
        self.assertIsNone(self.test_tree._root) # root should initialize to None
        self.assertEqual(self.test_tree._size, 0) # size should be zero

    def test_add_root(self):
        root = self.test_tree._add_root("Root element")
        self.assertEqual(self.test_tree._root, root._node)
        self.assertEqual(self.test_tree._size, 1)

    def test_add_root_already_exists(self):
        """Does _add_root() raise ValueError when trying to add a root to a tree
        that already has one?"""
        root = self.test_tree._add_root("Root element")
        with self.assertRaises(ValueError):
            self.test_tree._add_root("Interloping root element")

class TestAddChild(unittest.TestCase):
    """Test _add_child internal method."""

    def setUp(self):
        self.test_tree = GeneralTree()
        self.root = self.test_tree._add_root("Root element")

    def test_add_one_child(self):
        """Confirm that a single child can be added."""
        child = self.test_tree._add_child(self.root, "First child element")
        self.assertEqual(self.test_tree._root._children,
                         [child._node])
                                    # root's _Node._children should now be a
                                    # a single-element list containing the
                                    # node object of the Position child

    def test_add_many_children(self):
        """Confirm that several children can be added with a shared parent."""
        expected_children_values = [1, 2, 3, 4, 5]
        for n in expected_children_values:
            self.test_tree._add_child(self.root, n)
        self.assertEqual(len(self.test_tree._root._children), 5)
        # Confirm the values of the underlying elements in the children list
        #   match the expected ones:
        for i in range(len(expected_children_values)):
            self.assertEqual(self.test_tree._root._children[i]._element,
                             expected_children_values[i])

class TestDelete(unittest.TestCase):
    """Tests for the _delete internal method."""

    def setUp(self):
        self.tree = GeneralTree()
        self.root = self.tree._add_root("Root element")
        # add one child
        self.first_child = self.tree._add_child(
            self.root, "First child element")

    def test_delete_one(self):
        """Test the simplest case of deleting a leaf that isn't the root."""
        self.tree._delete(self.first_child)
        self.assertEqual(self.tree._size, 1)

    def test_delete_node_with_exactly_one_child_leaf(self):
        """Test that when a node with exactly one child is deleted, that
        child is promoted to become the child of node that had been its
        grandparent."""
        grandchild = self.tree._add_child(self.first_child,
                                         "grandchild element")
        self.tree._delete(self.first_child)
        self.assertEqual(self.tree._size, 2) # Should be 2 nodes now
        self.assertEqual(grandchild._node._parent, self.root._node)

    def test_delete_node_with_exactly_one_nonleaf_child(self):
        """Does the 'promotion' still work correctly if the promoted node has
        multiple layers of its own children and grandchildren?"""
        random.seed(3)
        grandchild = self.tree._add_child(self.first_child,
                                         "grandchild element")
        # give grandchild multiple children
        great_grandchildren = [] # list to store these positions for later
        for i in range(5):
            ggc = self.tree._add_child(grandchild, i) # Element is just the int
            great_grandchildren.append(ggc)
        size_check = self.tree._size
        for ggc in great_grandchildren:
            randval = random.random() # Make some be leaves, others not
            if randval >= 0.5:
                for i in range(3):
                    self.tree._add_child(ggc, i)
        peak_size = self.tree._size
        assert self.tree._size == size_check + 9, f"size was {self.tree._size}"
        # with seed 3, should have added 3 (3 of the vals should've been over 0.5)
        #   Should have added 9 total, 3 * 3.
        self.tree._delete(self.first_child)
        self.assertEqual(self.tree._size, peak_size - 1) # Should only have
                                                        # decreased by 1
        self.assertEqual(grandchild._node._parent, self.root._node)
        for ggc in great_grandchildren: # all greatgrandchildren should have same
                                        #   parent they started with.
            self.assertEqual(ggc._node._parent, grandchild._node)

    def test_delete_node_with_multiple_children(self):
        """Does the _delete method raise ValueError when attempting to delete
        a node whose Position has more than one child?"""
        for i in range(3):
            self.tree._add_child(self.first_child, i)
        assert self.tree.num_children(self.first_child) == 3
        with self.assertRaises(ValueError):
            self.tree._delete(self.first_child)

    def test_delete_root(self):
        """Does the delete method properly handle deletion of root?"""
        self.tree._delete(self.root)
        # Object stored as instance variable self.first_child should now be
        #   the root. 
        self.assertEqual(self.tree.root(), self.first_child)
        

class TestRecursivelyDelete(unittest.TestCase):
    """Tests for _recursively_delete."""

    def setUp(self):
        """Create same 12-element, 4-layer tree used in TestPublicAccessors."""
        # Build 12-element test tree
        self.tree, self.positions = twelve_element_test_tree()

    def test_recursively_delete_leaf(self):
        """The base case."""
        # Position 12 is a leaf at depth 4
        starting_length = len(self.tree)
        position = self.positions[12]
        node = position._node
        parent = position._node._parent
        self.tree._recursively_delete(position)
        self.assertEqual(len(self.tree), starting_length - 1)
        self.assertEqual(node, node._parent) # confirm convention for deprecated
                                                # nodes was applied

    def test_recursively_delete_node_with_one_child(self):
        starting_length = len(self.tree)
        # Position 2 is a child of root with one child of its own, position 5.
        position = self.positions[2]
        node_2 = position._node
        node_5 = self.positions[5]._node
        self.tree._recursively_delete(position)
        self.assertEqual(len(self.tree), starting_length - 2)

        # confirm convention for deprecated nodes applied to both deleted nodes
        self.assertEqual(node_2, node_2._parent)
        self.assertEqual(node_5, node_5._parent)

    def test_recursively_delete_node_with_multiple_leaf_children(self):
        """Node to be recursively deleted has multiple children, but those
        have no children of their own."""
        starting_length = len(self.tree)
        position = self.positions[4]
        node_4 = position._node
        node_10 = self.positions[10]._node
        node_11 = self.positions[11]._node
        self.tree._recursively_delete(position)
        self.assertEqual(len(self.tree), starting_length - 3) # 3 nodes should be gone

        # confirm nodes deprecated
        self.assertEqual(node_4, node_4._parent)
        self.assertEqual(node_10, node_10._parent)
        self.assertEqual(node_11, node_11._parent)

    def test_recursively_delete_node_with_multiple_child_layers(self):
        """Node to be recursively deleted has multiple children, and at least one
        of those children has a child of its own."""
        # Node 3 has four children. One of those children, node 6, has one child
        #   of its own, node 12. Others are leaves.
        start_length = len(self.tree)
        position = self.positions[3]
        nodes_for_deletion = [position._node]
        for i in [6, 7, 8, 9, 12]:
            nodes_for_deletion.append(self.positions[i]._node)
        self.tree._recursively_delete(position)

        self.assertEqual(len(self.tree), start_length - 6) # 6 nodes should be gone

        # confirm nodes deprecated:
        for node in nodes_for_deletion:
            self.assertEqual(node, node._parent)
        
        
class TestPublicAccessors(unittest.TestCase):
    """Test that the main public accessor methods work for a simple test
    tree with 3 layers.
    """

    def setUp(self):
        self.tree = GeneralTree()
        self.root = self.tree._add_root("Root element")
        self.first_child = self.tree._add_child(self.root,
                                                "First child element")
        self.large_tree, self.positions = twelve_element_test_tree()

    def test_height(self):
        """Does the height method correctly return the height of various nodes
        in the large 12-element test tree?"""
        # height of root should be 3 (3 levels below it)
        self.assertEqual(self.large_tree.height(), 3)

        # height of position 2 should be 1:
        self.assertEqual(self.large_tree.height(self.positions[2]), 1)
        # height of position 3 should be 2:
        self.assertEqual(self.large_tree.height(self.positions[3]), 2)
        # height of a leaf should be 0:
        self.assertEqual(self.large_tree.height(self.positions[10]), 0)

    def test_depth(self):
        """Does the depth() method return the correct height for various nodes in
        the 12-element test tree?"""
        # depth of root should be 0
        self.assertEqual(self.large_tree.depth(self.large_tree.root()), 0)
        # depth of position 2 (first layer child) should be 1
        self.assertEqual(self.large_tree.depth(self.positions[2]), 1)
        # depth of position 8 (second layer child) should be 2
        self.assertEqual(self.large_tree.depth(self.positions[8]), 2)
        # depth of 12 (third layer child) should be 3
        self.assertEqual(self.large_tree.depth(self.positions[12]), 3)
        
    def test_root(self):
        """Does root() return a Position referencing the same node as
        the tree's root?"""
        self.assertEqual(self.tree.root(),
                         self.tree._make_position(self.tree._root))

    def test_is_root(self):
        """Does is_root() correctly return True when called on a Position
        that is root, and false when called on a Position that is not root?"""
        self.assertTrue(self.tree.is_root(self.root))
        self.assertFalse(self.tree.is_root(self.first_child))

    def test_parent(self):
        """Does parent() correctly return the Position object corresponding to
        the parent node of arg position when position is not root, and None
        when called on a Position that is root?"""
        self.assertEqual(self.tree.parent(self.first_child), self.root)
        self.assertIsNone(self.tree.parent(self.root))

    def test_is_leaf(self):
        """Does is_leaf() correctly return True when called on a position that
        has no children, and False when called on a position that has at least
        one child?"""
        self.assertTrue(self.tree.is_leaf(self.first_child))
        self.assertFalse(self.tree.is_leaf(self.root))

    def test_len(self):
        """Obvious-case tests for len(tree) where the method is being called
        in isolation, not used in combination with anything else."""
        # len() should be 2 with the 2 elements added to self.tree by setUp
        self.assertEqual(len(self.tree), 2)
        # len of a new tree should be 0
        new_tree = GeneralTree()
        self.assertEqual(len(new_tree), 0)
        # Add root and 5 children of root, len should be 6
        new_tree._add_root("NT root element")
        for i in range(5):
            new_tree._add_child(new_tree.root(), i)
        self.assertEqual(len(new_tree), 6)
        # Add 10 children to each of those children, len should be 56
        for child in new_tree.root()._node._children: # todo (the GeneralTree.children() iterator isn't implemented yet)
            child = new_tree._make_position(child)
            for i in range(10):
                latest_child = new_tree._add_child(child, i) # For expediency
                                                            # in using one leaf
                                                            # below
        self.assertEqual(len(new_tree), 56)
        # Confirm the _delete method decrements length
        prior_length = len(new_tree)
        new_tree._delete(latest_child)
        self.assertEqual(len(new_tree), prior_length - 1)

    def test_is_empty(self):
        """Does is_empty() return True if tree is empty, False if not?"""
        self.assertFalse(self.tree.is_empty())
        # Try it on a tree that was nonempty, then was emptied out:
        self.tree._delete(self.first_child)
        self.tree._delete(self.root)
        self.assertTrue(self.tree.is_empty())
        # Try it on a new blank tree:
        new_tree = GeneralTree()
        self.assertTrue(new_tree.is_empty())

    def test_parenthesize(self):
        expected_string = '1 (2 (5), 3 (6 (12), 7, 8, 9), 4 (10, 11))'
        self.assertEqual(self.large_tree.parenthesize(self.large_tree.root()),
                         expected_string)
        

class TestGenerators(unittest.TestCase):
    """Tests for the public methods that generate an iteration, and the nonpublic
    tree-traversal methods they rely on."""

    def setUp(self):
        # Build 12-element test tree
        self.tree = GeneralTree()
        self.tree._add_root(1)
        for i in range(2, 5): # Children of root with elements 2, 3, 4
            self.tree._add_child(self.tree.root(), i)

        # 2 has one leaf-child with element=5
        node_2 = self.tree.root()._node._children[0]
        assert node_2._element == 2 # double check correct node, this isn't an
                                    #   ordered tree, so relying on list's
                                    #   ordering to access a specific node for now
        self.leaf_node_5 = self.tree._add_child( # save for when need a leaf
                             self.tree._make_position(node_2), 5)

        # 3 has 4 children, 6, 7, 8, and 9
        self.node_3 = self.tree.root()._node._children[1]
        assert self.node_3._element == 3
        for i in range(6, 10):
            self.tree._add_child(self.tree._make_position(self.node_3), i)
        # Among 3's children, 6 has one child, 12; other 3 are leaves
        node_6 = self.node_3._children[0]
        assert node_6._element == 6
        self.tree._add_child(self.tree._make_position(node_6), 12)

        # Node 4 has two children, 10 and 11, both leaves
        node_4 = self.tree.root()._node._children[2]
        assert node_4._element == 4
        for i in range(10, 12):
            self.tree._add_child(self.tree._make_position(node_4), i)
        assert len(self.tree) == 12 # confirm all 12 elements in the tree

    def test_children_of_root(self):
        """Does the children() method allow caller to iterate over the Positions
        that represent the children of root when children is called with root
        as its Position arg?
        """
        expected_root_children_elements = set([2, 3, 4]) # Values stored at root's
                                                        # children
        expected_root_children_positions = [self.tree._make_position(i) for i in
                                            self.tree.root()._node._children]
        actual_root_children_elements = set()
        actual_root_children_positions = [] # positions not hashable so this works
                                            #   for now, should ignore order though.
        for child in self.tree.children(self.tree.root()):
            actual_root_children_elements.add(child._node._element)
            actual_root_children_positions.append(child)
        actual_root_children_elements = set(actual_root_children_elements)
        
        self.assertEqual(actual_root_children_elements, # compare the elements sets
                         expected_root_children_elements)
        self.assertEqual(actual_root_children_positions, # compare the positions lists
                         expected_root_children_positions)

    def test_children_of_general_node(self):
        """Does children() method yield the correct Positions and elements
        when called on a non-root Position that has several children?"""
        expected_children_positions = [self.tree._make_position(i) for i in
                                       self.node_3._children]
        # Can't cast it to set because positions not hashable
        assert len(expected_children_positions) == 4, "node 3 should have 4\
children from setUp"
        actual_children_positions = []
        for child in self.tree.children(self.tree._make_position(self.node_3)):
            actual_children_positions.append(child)
        self.assertEqual(actual_children_positions, expected_children_positions)
        # todo: works for now but should ignore order. 
        
    def test_children_of_leaf(self):
        """Does children() return None when called on a leaf?"""
        leaf_position = self.leaf_node_5
        for child in self.tree.children(leaf_position):
            self.assertIsNone(child)

    def test_subtree_preorder(self):
        """Does _subtree_preorder yield the tree's elements in the correct
        order?"""
        expected_elements = [1, 2, 5, 3, 6, 12, 7, 8, 9, 4, 10, 11]
            # Nodes (storing these elements) should be yielded in this order when
            #   preorder traversing the entire tree by passing root as the Position
            #   arg.
        assert len(expected_elements) == len(self.tree)
        yielded_elements = []
        for position in self.tree._subtree_preorder(self.tree.root()):
            yielded_elements.append(position._node._element)
        self.assertEqual(yielded_elements, expected_elements)

    def test_preorder(self):
        """Does the public preorder method yield the tree's elements in the same,
        correct order as nonpublic _subtree_preorder?"""
        # Confirm that the two separate generator objects yield same objects
        expected_order = [i for i in self.tree._subtree_preorder(self.tree.root())]
        actual_order = [i for i in self.tree.preorder()]
        self.assertEqual(actual_order, expected_order)

    def test_positions(self):
        """Does positions() yield the tree's elements in the same order as its
        traversal method?"""
        # Test should break if default traversal method changes away from preorder
        expected_order = [i for i in self.tree.preorder()]
        actual_order = [i for i in self.tree.positions()]
        self.assertEqual(actual_order, expected_order)

    def test_iter(self):
        """Does __iter__ yield the tree's elements in the same order as the
        positions() method?"""
        # __iter__ uses whatever traversal positions() uses--encapsulation.
        expected_order = [i._node._element for i in self.tree.positions()]
        actual_order = [i for i in self.tree]
        self.assertEqual(actual_order, expected_order)

    def test_subtree_postorder(self):
        """Does _subtree_postorder yield the tree's elements in the intended
        order?"""
        expected_order_elements = set([5, 2, 12, 6, 7, 8, 9, 3, 10, 11, 4, 1])
        actual_order_elements = set()
        for position in self.tree._subtree_postorder(self.tree.root()):
            actual_order_elements.add(position._node._element)
        self.assertEqual(expected_order_elements, actual_order_elements)
        
    def test_postorder(self):
        """Does postorder yield the tree's elements in the same order as its
        nonpublic traversal method?"""
        expected_order = [i for i in self.tree._subtree_postorder(self.tree.root())]
        actual_order = [i for i in self.tree.postorder()]
        self.assertEqual(expected_order, actual_order)

    def test_breadthfirst(self):
        """Does breadthfirst() yield the tree's Positions in the expected order?"""
        # Expedient to test by element values for now.
        expected_order_elements = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual_order_elements = [i._node._element for i in self.tree.breadthfirst()]
        self.assertEqual(actual_order_elements, expected_order_elements)

def twelve_element_test_tree():
    """Helper function to generate the same 12-element, 4-layer test tree in a way
    that's callable by setUp methods throughout this test module.

    Returns:
        (tuple): (GeneralTree, Dict) GeneralTree object an a dictionary for use
            as node-access shortcuts.
    """
    
    tree = GeneralTree()
    positions = {}
    positions[1] = tree._add_root(1)
    for i in range(2, 5): # Children of root with elements 2, 3, 4
        positions[i] = tree._add_child(tree.root(), i)

    # 2 has one leaf-child with element=5
    node_2 = tree.root()._node._children[0]
    assert node_2._element == 2 # double check correct node, this isn't an
                                #   ordered tree, so relying on list's
                                #   ordering to access a specific node for now
    positions[5] = tree._add_child( # save for when need a leaf
                         tree._make_position(node_2), 5)

    # 3 has 4 children, 6, 7, 8, and 9
    node_3 = tree.root()._node._children[1]
    assert node_3._element == 3
    for i in range(6, 10):
        positions[i] = tree._add_child(tree._make_position(node_3), i)
    # Among 3's children, 6 has one child, 12; other 3 are leaves
    node_6 = node_3._children[0]
    assert node_6._element == 6
    positions[12] = tree._add_child(tree._make_position(node_6), 12)

    # Node 4 has two children, 10 and 11, both leaves
    node_4 = tree.root()._node._children[2]
    assert node_4._element == 4
    for i in range(10, 12):
        positions[i] = tree._add_child(tree._make_position(node_4), i)
    assert len(tree) == len(positions) == 12 # confirm all 12 elements in the tree and all 12
                            # positions captured in the dict.
    

    # confirm all the dict's key match the actual underlying element values:
    for key in positions.keys():
        assert key == positions[key]._node._element

    return tree, positions

if __name__ == '__main__': unittest.main() # one-liner so coverage will ignore
