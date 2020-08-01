import unittest

from tree_abst_base import Tree

class TestAbstractMethods(unittest.TestCase):
    """Quick tests to confirm basic functionality."""

    # Not sure why the ones that take args aren't passing the assertRaises
    #   test even though they do fine with an except NotImplementedError.
    #   The function might somehow be getting pre-called and that call, rather
    #   than the unittest.assertRaises call, is catching the NotImplementedError?

    def setUp(self):
        self.tree = Tree()
        self.pos = self.tree.Position()

    def test_pos_element(self):
        function = self.pos.element
        self.assertRaises(NotImplementedError, function)

    def test_pos_eq(self):
        other = Tree().Position()
##        other = self.tree.Position()
        function = self.pos.__eq__
        try:
            self.assertRaises(NotImplementedError, self.pos == other)
        except NotImplementedError:
            pass

##    def test_pos_ne(self):
##        other = Tree().Position()
##        function = self.pos.__ne__
##        self.assertRaises(NotImplementedError, function(other))

    def test_root(self):
        function = self.tree.root
        self.assertRaises(NotImplementedError, function)

    def test_parent(self):
        p = self.tree.Position()
        function = self.tree.parent
        try:
            self.assertRaises(NotImplementedError, function(p))
        except NotImplementedError:
            pass

    def test_num_children(self):
        p = self.tree.Position()
        try:
            self.assertRaises(NotImplementedError, self.tree.num_children(p))
        except NotImplementedError:
            pass

    def test_len(self):
        try:
            self.assertRaises(NotImplementedError, len(self.tree))
        except NotImplementedError:
            pass

class TestConcreteMethods(unittest.TestCase):
    """Quick basic tests for the methods that are concretely implemented in the
    Tree abstract base class itself."""

    def setUp(self):
        self.tree = Tree()

    def test_is_root(self):
        # Still ultimately ends in a NotImplementedError, this one calls root()
        #   method which is not implemented in the ABC.
        p = self.tree.Position()
        try:
            self.assertRaises(NotImplementedError, self.tree.is_root(p))
        except NotImplementedError:
            pass

    def test_is_leaf(self):
        p = self.tree.Position()
        try:
            self.assertRaises(NotImplementedError, self.tree.is_leaf(p))
        except NotImplementedError:
            pass

    def test_is_empty(self):
        try:
            self.assertRaises(NotImplementedError, self.tree.is_empty())
        except NotImplementedError:
            pass
        


if __name__ == '__main__':
    unittest.main()
