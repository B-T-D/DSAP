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
        if not isinstance(token, str):
            raise TypeError('Token must be a string')
        self._add_root(token) # use inherited, nonpublic method
        if left is not None: # presumably three-parameter form
            if token not in '+-*x/': # will accept either 'x' or '*' as
                                        # multiplication operator
                raise ValueError('token must be valid operator')
            self._attach(self.root(), left, right) # use the inherited nonpublic
                                                    # _attach method

    def __str__(self):
        """Return string representation of the expression."""
        pieces = [] # sequence of piecewise strings to compose
        self._parenthesize_recur(self.root(), pieces)
        return ''.join(pieces)

    def _parenthesize_recur(self, p, result):
        """Append piecewise representation of p's subtree to resulting list."""
        if self.is_leaf(p):
            result.append(str(p.element())) # leaf value as a string
        else:
            result.append('(') # opening parenthesis
            self._parenthesize_recur(self.left(p), result) # left subtree
            result.append(p.element()) # operator
            self._parenthesize_recur(self.right(p), result) # right subtree
            result.append(')') # closing parenthesis

    def evaluate(self):
        """Return the numeric result of the expression."""
        # wrapper for the nonpublic method that evaluates a subtree. The basic
        #   algorithm is if p is a leaf, return its value, else recursively
        #   return the value of each side of the subtree (i.e. evaluate the
        #   parenthesized expression first).
        return self._evaluate_recur(self.root())

    def _evaluate_recur(self, p):
        """Return the numeric result of subtree rooted at p.

        Args:
            p (Position): Root of the subtree that's being evaluated.

        Returns:
            (float): the value of the expression
        """
        
        if self.is_leaf(p):
            return float(p.element()) # we assume element is numeric
        else:
            op = p.element()
            left_val = self._evaluate_recur(self.left(p))
            right_val = self._evaluate_recur(self.right(p))
            if op == '+':
                return left_val + right_val
            elif op == '=':
                return left_val - right_val
            elif op == '/':
                return left_val / right_val
            else: # only remaining chars in the operators string are x and *
                return left_val * right_val

# ----- standalone function ------------

def build_expression_tree(tokens):
    """Returns an ExpressionTree based on a tokenized expression.
    Tokenization requires that e.g. the int 568 has been atomized into the
    number 568 rather than each of its digits being treated as a separate
    integer.

    Args:
        tokens (iterable): an iterable of string tokens

    Returns:
        (ExpressionTree): ...
    """
    S = [] # Python list object to use as a stack
    for t in tokens:
        if t in '+-x*/': # if t is an operator symbol
            S.append(t) # push the operator symbol
        elif t not in '()': # if t isn't a parenthesis character
            S.append(ExpressionTree(t)) # push a trivial tree storing the value
        elif t == ')': # compose a new tre efrom three constituent parts if
                        #   t has just closed a parenthesized stretch of characters
            right = S.pop() # right subtree as per LIFO
            op = S.pop() # operator symbol
            left = S.pop() # left subtree
            S.append(ExpressionTree(op, left, right)) # repush tree
        # ignore a open-parenthesis character
    return S.pop()

def main():
    tokens = '(((3+1)x4)/((9-5)+2))' # each character is a complete token
    tokens = list(tokens)
    print(tokens)
    etree = build_expression_tree(tokens)
    print(etree)
    print(etree.evaluate()) # evaluates wrong.

    etree = build_expression_tree('((2+1)/(4-1))')
    print(etree)
    print(etree.evaluate())

if __name__ == '__main__':
    main()
                
