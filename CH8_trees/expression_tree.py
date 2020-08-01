from linked_binary_tree import LinkedBinaryTree

class ExpressionTree(LinkedBinaryTree):
    """Class for storing a binary tree to represent the structure of an
    arithmetic expression."""

    def __init__(self, token, left=None, right=None):
        """Create an expression tree.

        In a single parameter form, token should be a leaf value(e.g. '42'),
        and the expression tree will have that value as an isolated external
        node.

        In a three-parameter version, token should be an operator, and left
        and right should be existing ExpressionTree instances that become
        the operands for the binary operator.
        """
        super().__init__() # initialize a LinkedBinaryTree
