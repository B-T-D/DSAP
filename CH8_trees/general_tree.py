# todo: style intent = shorthand in private methods but not publics. E.g.
#   "p" vs. "position"

# Mine from tic tac toe, not "official" DSAP

"""
GeneralTree class as well as a LinkedQueue class used for GeneralTree's
implementation of breadth-first traversal.
"""

class GeneralTree:
    """Concrete implementation of a general tree data structure. Intended to be
    reusable."""

    # ----------------------- nested nonpublic Node class --------------------

    class _Node:
        """Structure storing the underlying data and relevant links for
        use by the tree class's methods."""
        __slots__ = '_element', '_parent', '_children' # to make lighter in memory
        #   Will the _children thing work for an arbitrary number of children?

        # Is there some smarter data structure to use than a list-array for
        # children? Maybe a hash table since we're assuming nonordered
        # children?
        def __init__(self, element, parent=None, children=None):
            """
            Args:
                element (object): Data of whatever type is to be stored in the
                    tree.
                parent (_Node): _Node object representing the parent 
                children (list): list containing other _Node objects
                
            Returns:
                None
            """
            self._element = element
            self._parent = parent
            self._children = children if children is not None else []

    # ----------------------- nested Postiion class --------------------------

    # Public because we want the element() accessor method to be public, per
    #   the ADT. 

    class Position:
        """Abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor not meant to be invoked by external user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same
            location.

            Args:
                other (object): Any type of object

            Returns:
                (bool): True if other is a Postition representing the same
                    location, else False.
            """
            return type(other) is type(self) and other._node is self._node

    def _validate(self, p):
        """Validate position and return the associated node if valid.

        Returns:
            (_Node): the _Node object at position, if position validly exists
                in the tree.
        """
        if not isinstance(p, self.Position):
            raise TypeError("'p' arg must be proper Position type")
        if p._container is not self:
            raise ValueError("'p' arg does not belong to this container")
        if p._node._parent is p._node: # convention for deprecated nodes
            raise ValueError("'p' is no longer valid")
        return p._node

    def _make_position(self, node):
        """
        Return Position instance for given node (or None if no node).

        Args:
            node (_Node): _Node object

        Returns:
            (Position): New Position instance with node as the value of its
                _node instance variable.
        """
        return self.Position(self, node) if node is not None else None

    def _height_func(self, p):
        """Return the height of the subtree rooted at Position p.
        Args:
            p (Position): position in the tree

        Returns:
            (int): height of the relevant subtree
        """
        if self.is_leaf(p):
            return 0 # base case
        else:
            return 1 + max(self._height_func(c) for c in self.children(p))

    # ----------------------- general tree constructor ----------------------
    def __init__(self):
        """Create an initially empty general tree."""
        self._root = None
        self._size = 0

    # ------------------------- nonpublic updaters ---------------------------

    def _add_root(self, e):
        """
        Place element e at the root of an empty tree and return new Position.
        Raise ValueError if tree nonempty.

        Args:
            e (object): Element to be stored at root.

        Returns:
            (Position): New Position object represnting tree's root.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_child(self, p: Position, e):
        """Create a new child for Position p, storing element e. Raise
        ValueError if Position p is invalid. 
        
        Returns:
            (Position): Position of the new Node.
        """
        # append the new Position obj to p._Node._children list
        node = self._validate(p)
        self._size += 1
        new_node = self._Node(element=e, parent=node) # new child _Node object
        node._children.append(new_node) # add it to parent node's children list
        return self._make_position(new_node) # make a position object

    def _replace(self, p, e):
        raise NotImplementedError

    def _attach(self, p: Position, other_tree) -> None:
        """Attach tree other_tree as a child-subtree of Position p."""

        # Unlike in LBT, we don't care about whether p was external, right?
        #   Because no limitation on number of children.
        raise NotImplementedError
    
    def _delete(self, p):
        """
        Delete the node at Position p, and replace it with its child, if
        it has exactly one child.

        Return the element that had been stored at Position p. RaiseValueError
        if Position p is invalid or has more than 1 child.
        """
        child = None
        node = self._validate(p)
        if self.num_children(p) > 1:
            raise ValueError("p has multiple children")
        if self.num_children(p) == 1:
            child = node._children[0] # better for time or space to list.pop()?
        if child is not None:
            child._parent = node._parent # child's grandparent becomes parent
        if node is self._root:
            self._root = child # child becomes root
        else:
            parent = node._parent
            # todo not sure the adaptation from the LBT code is correct here,
            #   wrt skipping the if node is parent._left stuff
            # Might be fine though. This child's child would be "pulled up"
            #   with it by the promotion, without any further action, right?
        self._size -= 1
        if node._parent is not None: # if the node was not root...
            node._parent._children.remove(node) # ...delete node from list of its
                                            # ...parent's child nodes
        node._parent = node # convention for deprecated node (make it its own parent)
        return node._element

    def _recursively_delete(self, p):
        # Should this be a public method instead / also?
        """
        Delete Position p and all its children.
        
        """
        
        # Return the element stored at p? Or return the whole subtree that was
        #   deleted?
        if self.is_leaf(p):
            self._delete(p)
            return
        self._recursively_delete(self._make_position(
            p._node._children[0]))
        return self._recursively_delete(p)
        
    # ----------------------- public accessor methods ------------------------

    def root(self):
        """
        Return Position representing the tree's root (or None if empty).

        Args:
            None

        Returns:
            (Position): Position object located at the root, or None if
                tree is empty.
        """
        return self._make_position(self._root)

    def is_root(self, position):
        """

        Args:
            position (Position): Position object located in this tree.

        Returns:
            (bool): True if position is the root of the tree, else False.
        """
        return self.root() == position

    def parent(self, position):
        """

        Args:
            position (Position): Position object located in this tree.

        Returns:
            (Position): Position object that is position's parent, or None if
                position is the root of the tree.
        """
        node = self._validate(position)
        return self._make_position(node._parent)

    def num_children(self, position):
        """

        Args:
            position (Position): Position object located in this tree.

        Returns:
            (int): Number of chidren nodes of position.
        """
        # Hasty implementation bc needed to test delete, may not be smartest
        #   But builtin len(list) should run in O(1) no different from
        #   storing an instance variable num_children for each node.
        return len(position._node._children)

    def is_leaf(self, position):
        """

        Args:
            position (Position): Position object located in this tree.

        Returns:
            (bool): True if position has no children, else False.
        """
        return self.num_children(position) == 0

    def __len__(self):
        """
        Returns:
            (int): Total number of Positions, i.e. elements, in the tree
        """
        return self._size

    def is_empty(self):
        """
        Returns:
            (bool): True if tree is empty, else False.
        """
        return len(self) == 0

    def height(self, position=None):
        """
        Return the height of the subtree rooted at position. If position is
        None, return height of the entire tree.

        Returns:
            (int): height of the subtree or else the full tree if position
                was None
        """
        if position is None:
            position = self.root()
        return self._height_func(position) # Call the recursive nonpublic
                                            # height method.

    def depth(self, position):
        """Return the number of levels separating the Position from tree's
        root.

        Args:
            position (Position): Position in the tree

        Returns:
            (int): int indicating position's height
        """
        if self.is_root(position):
            return 0
        else:
            return 1 + self.depth(self.parent(position))

    def preorder(self):
        """Generate a preorder-traversal iteration of all positions in the tree.

        Yields:
            (Position): The next position in the tree reached by a preorder
                traversal.
        """
        if not self.is_empty():
            for position in self._subtree_preorder(self.root()): # start recursion
                yield position

    def postorder(self):
        """Generate a postorder iteration of all positions in the tree.

        Args:
            position (Position): Position object located in this tree.

        Yields:
            (Position): The next position reached by a postorder traversal.
        """
        if not self.is_empty():
            for position in self._subtree_postorder(self.root()): # start recursion
                yield position

    def breadthfirst(self):
        """Generate a breadth-first iteration of all positions in the tree.

        Yields:
            (Position): The next position reached by a breadth-first traversal.
        """
        # Add chilcren to queue when the "visits" learn of them by visiting
        #   their parent, then go back and actually visit them later once they
        #   reach the head of the queue (as higher-height nodes are visited and
        #   FIFO-ed out of the queue).
        if not self.is_empty():
            fringe = LinkedQueue() # Enqueue positions that are known but not yet
            fringe.enqueue(self.root()) #   ...visited.
            while not fringe.is_empty():
                position = fringe.dequeue() # remove from front of queue
                yield position
                for child in self.children(position):
                    fringe.enqueue(child) # Add each child of the newly visited
                                            #  ...position to the queue

    def children(self, position):
        """Generate an iteration of Positions representing the children nodes
        of position.

        Args:
            position (Position): Position object located in this tree.

        Yields:
            (Position): The next Position object among position's children.
        """
        node = self._validate(position)
        # In current implementation, children are already stored as a python list
        for child in node._children:
            yield self._make_position(child) # yield it back as a Position,
                                                # rather than a _Node
        
    def positions(self):
        """
        Generate an iteration of all Positions of the tree. Uses preorder
        traversal.

        Args:
            None

        Yields:
            (Position): The next Postion object in the tree.
        """
        return self.preorder()

    def __iter__(self):
        """
        Generate an iteration of the tree's elements (i.e. the underlying
        data, not their Positions).

        Yields:
            (object): The next object stored as an element of a tree Position.
                Of whatever type that data is.
        """
        for position in self.positions(): # Use same order as positions()
            yield position.element()   # ...but yield elements instead of Positions

    # --------------------- nonpublic traversal methods ----------------------

    def _subtree_preorder(self, p):
        """Generate a preorder iteration of positions in subtree rooted at
        Position p."""
        yield p # yielding p to the caller (other method in this class)
                #   implements performing the "visit".
        for c in self.children(p):
           for other in self._subtree_preorder(c): # recursively do preorder on c's subtree
               yield other # ...and yield each to the caller
        
    def _subtree_postorder(self, p):
        """Generate a postorder iteration of positions in subtree rooted at
        Position p."""
        for c in self.children(p): # for each child c
            for other in self._subtree_postorder(c): # do postorder of child's
                yield other         # ...subtrees, yielding each subtree to caller
        yield p # perform visit action "post" recursing over all children

    # ------------------------- visual output methods --------------------------
    def parenthesize(self, position):
        """Print parenthetic representation of the subtree rooted at position.

        Returns:
            (str): String representation of the tree.
        """
        characters = []
        characters.append(str(position.element()))
        if not self.is_leaf(position):
            first_time = True
            for c in self.children(position):
                sep = ' (' if first_time else ', '
                characters.append(sep)
                first_time = False # any future passes won't be first
                characters.append(self.parenthesize(c)) # recurse
            characters.append(')')
        return ''.join(characters)
        

class LinkedQueue:
    """FIFO queue implementation using a singly linked list for storage."""

    class _Node:

        __slots__ = '_element', '_next'
                                        
        def __init__(self, element, next):
            """
            Args:
                _next (_Node): another _Node object.
                _element (object): object of whatever type is stored in the LL stack.
            """
            self._element = element # reference to user's element
            self._next = next # reference to next node

    def __init__(self):
        """Create an empty queue."""
        self._head = None
        self._tail = None
        self._size = 0 # number of queue elements

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return (but don't remove) the element at the front of the queue."""
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._head._element # front aligned with head of list

    def dequeue(self):
        """Remove and return the first element of the queue (i.e. FIFO). Raise Empty
        exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty(): # If completion of this dequeue emptied the queue
            self._tail = None # Removed head had been the tail.
        return answer

    def enqueue(self, e):
        """Add an element to the back of the queue."""
        newest = self._Node(e, None) # node will be new tail node bc it's going in at end
        if self.is_empty():
            self._head = newest
        else:
            self._tail._next = newest
        self._tail = newest # update reference to tail node
        self._size += 1    
