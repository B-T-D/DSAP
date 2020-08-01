from linked_queue import LinkedQueue

class Tree:
    """Abstract base class representing a tree structure."""

    # ------------------------ nested Position class -------------
    class Position:
        """An abstraction representing the location of a single element."""

        def element(self):
            """Return the element stored at this Position."""
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            """Return True if other Position represents the same location."""
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            """Return True if other does not represent the same location."""
            return not (self == other) # opposite of __eq__

    # ------- abstract methods that concrete subclass must support ---------
    def root(self):
        """Return Position representing the tree's root (or None if empty)."""
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p):
        """Return Position representing p's parent (or None if p is root)."""
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """Return the number of children that Position p has."""
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """Return the total number of elements in the tree."""
        raise NotImplementedError('must be implemented by subclass')

    # --------- concrete methods implemented in this class -------------------
    def is_root(self, p):
        """Return True if Position p represents the root of the tree."""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if Position p does not have any children."""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0

    def _height1(self):
        # Illustrative example from DSAP, inferior O(n^2) running time
        """Return the height of the tree."""
        # return max(self.depth(p) for p in self.positions() if self.is_leaf(p))

        # commented out to remove it from "coverage" metric

    def _height2(self, p: Position) -> int:
        """Return the height of the subtree rooted at Position p."""
        # Runs in O(n) where n is number of positions in tree T
        if self.is_leaf(p):
            return 0 # base case: A leaf's height is zero because no children
        else:
            return 1 + max(self._height2(c) for c in self.children(p))
                # ^ return the height of the tallest child of p (plus one).

    def height(self, p: Position=None) -> int: # The public height method
            # Confirmed this is correct syntax for type hint where an arg
            #   has a default value.
        """Return the height of the subtree rooted at Position p. If p is None,
        return height of the entire tree."""
        # Basically a wrapper. Checks if value of p should default to root, then
        #   calls _height2(p) on the appropriate value of p.
        if p is None:
            p = self.root()
        return self._height2(p)

    def depth(self, p):
        """Return the number of levels separating Position p from the root."""
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        for p in self.positions(): # use same order as positions()
            yield p.element()       # but yield each element

    def preorder(self):
        """Generate a preorder-traversal iteration of positions in the tree (yield the positions
        in the order they'd be visited by the preorder traversal algorithm)."""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()): # start recursion
                yield p

    def _subtree_preorder(self, p):
        # utility method
        """Generate a preorder iteration of positions in subtree rooted at p."""
        yield p # Analogous to "perform the 'visit' action for position p" step of the pseudocode
            # (we just yield the Position object to visit, then let the caller perform the visit action)
        for c in self.children(p):  # for each child c...
            for other in self._subtree_preorder(c): # ...recursively do preorder of c's subtree...
                yield other # ...yielding each to our caller

    def positions(self):
        # Use a preorder traversal as the default order of iteration in the positions method.
        #   (Official tree ADT requires that all trees support a positions method that generates an
        #   iteration of all positions of the tree).
        """Generate an iteration of the tree's positions (not elements)."""
        return self.preorder() # return the entire preorder iterator

    def postorder(self):
        """Generate a postorder iteration of positions in the tree."""
        # Mainly a wrapper for _subtree_postorder
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()): # start recursion
                yield p

    def _subtree_postorder(self, p):
        """Generate a position iteration of positions in subtree rooted at p."""
        for c in self.children(p):  # for each child c
            for other in self._subtree_postorder(c): # do postorder of c's subtree
                yield other # yield each subtree to the caller
        yield p # visit p after its subtrees

    def breadthfirst(self):
        """Generate a breadth-first iteration of the positions of the tree."""
        # Add children to the queue when the "visits" learn of them, go back and actually visit
        #   them later once they reach head of the queue.
        if not self.is_empty():
            fringe = LinkedQueue() # Known postiions not yet yielded are placed in the queue
            fringe.enqueue(self.root())
            while not fringe.is_empty():
                p = fringe.dequeue() # remove from front of the queue
                yield p
                for c in self.children(p):
                    fringe.enqueue(c)  # add children to back of the queue
        
            
    
