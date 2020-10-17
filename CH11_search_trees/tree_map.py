import sys, os

this_directory = os.path.dirname(__file__)
ch8_directory = '../CH8_trees' # for LinkedBinaryTree
ch10_directory = '../CH10_maps_hash_tables' # for MapBase
sys.path.insert(0, os.path.abspath(ch8_directory))
sys.path.insert(1, os.path.abspath(ch10_directory))

from linked_binary_tree import LinkedBinaryTree
from map_base_abc import MapBase

class TreeMap(LinkedBinaryTree, MapBase):
    """Sorted map implementation using a binary search tree."""

    #### override LinkedBinaryTree's Position class ####
    class Position(LinkedBinaryTree.Position):
        def key(self):
            """Return value from the position's key-value pair."""
            return self.element()._key

        def value(self):
            """Return value from the position's key-value pair."""
            return self.element()._value

    #### nonpublic utilities ####
    def _subtree_search(self, p, k):
        """Return Position of p's subtree having key k, or last node
        searched.

        Args:
            p (Position): Root Position of the subtree that will be searched.
            k (any): Value of key to search for. Of appropriate type for the tree.
        """
            # TODO ^ or won't the keys actually always be hashed to ints for
            #   purposes of the ultimate, underlying tree?
        print(f"SEARCHING p.key()={p.key()} FOR k={k}")
        if k == p.key(): # base case 1: found match
            return p
        elif k < p.key(): # search left subtree recursively
            if self.left(p) is not None:
                print(f"****LEFT subtree recursive search: self.left(p) had key {self.left(p).key()}")
                return self._subtree_search(self.left(p), k)
        else: # search right subtree recursively
            if self.right(p) is not None:
                print(f"****RIGHT subtree recursive search: self.right(p) had key {self.right(p).key()}")
                return self._subtree_search(self.right(p), k)
        print(f"Reached no-match base case FOR k={k}")
        return p # base case 2: No match, return the final node searched

    def _subtree_first_position(self, p):
        """Return Position of first item (item with minimum key in the tree)
        in subtree rooted at p."""
        walk = p
        while self.left(walk) is not None: # If there are further left children,
            walk = self.left(walk)      #  then not at the min yet.
        return walk

    def _subtree_last_position(self, p):
        """Return Position of last item (item with max key) in subtree rooted
        at p."""
        walk = p
        while self.right(walk) is not None: # If there are further right children,
            walk = self.right(walk)         # then can't be at max yet.
        return walk

    def first(self):
        """Return the first Position in the tree (or None if empty)."""
        return self._subtree_first_position(self.root()) if len(self) > 0 else None

    def last(self):
        """Return the last Position in the tree (or None if empty)."""
        return self._subtree_last_position(self.root()) if len(self) > 0 else None

    def before(self, p):
        """Return the Position just before p in the natural order. Return None if p is the
        first Position."""
        self._validate(p) # inherited from LinkedBinaryTree
        if self.left(p):
            return self._subtree_last_position(self.left(p))
        else:
            # walk upward
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.left(above):
                walk = above
                above = self.parent(walk)
            return above

    def after(self, p):
        """Return the Position just after p in the natural order (least key in the tree that
        is strictly greater than p's key).
        Return None if p is the last
        Position.
        
        """
        # Authors don't implement this one, they just say "symmetrical with TreeMap.before()"
        self._validate(p)
        if self.right(p):
            return self._subtree_first_position(self.right(p))
        else:
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.right(above): # IMU just need to change
                                                            # this to self.right(above) instead
                                                            # of self.left(above)
                walk = above
                above = self.parent(walk)
            return above

    def find_position(self, k):
        """Return position with key k, or else neighbor (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)  # hook for balanced-tree subclasses
            return p

    def find_min(self):
        """Return (key, value) pair with minimum key (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self.first()
            return (p.key(), p.value())

    def find_ge(self, k):
        """Return (key, value) pair with least key greater than or equal to k. Return None
        if no such key exists."""
        if self.is_empty():
            return None
        else:
            p = self.find_position(k) # May not find exact match
            if p.key() < k: # if p's key is too small...
                p = self.after(p) # ...then look at immediate next greatest value
            return (p.key(), p.value()) if p is not None else None

    def find_range(self, start=None, stop=None):
        """Iterate all (key, value) pairs such that start <= key , stop.

        If start is None, iteration begins with minimum key in the map.
        If stop is None, iteration continues through the maximum key in the map.
        """
        if not self.is_empty():
            if start is None:
                p = self.first()
            else:
                # Initialize p with logic similar to find_ge().
                p = self.find_position(start)
                if p.key() < start: # If there's no key exactly equal to start 
                    p = self.after(p)
            while p is not None and (stop is None or p.key() < stop):
                yield (p.key(), p.value())
                p = self.after(p)

    #### Accessor and updater methods ####

    def __getitem__(self, k):
        """Return value associated with key k (raise KeyError if not found)."""
        if self.is_empty():
            raise KeyError(f'KeyError: {repr(k)}')
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p) # hook for balanced-tree subclass
            if k != p.key():
                raise KeyError(f'KeyError: {repr(k)}')
            return p.value()

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        if self.is_empty(): # Easy case where new kvp is simply the root
            leaf = self._add_root(self._Item(k, v)) # from LinkedBinaryTree
        else:
            print(f"-----TreeMap.__setitem__ is calling subtree search at subtree rooted p.key() = {self.root().key()}-----")
            p = self._subtree_search(self.root(), k)
            if p.key() == k: # If that key is already in the tree
                p.element()._value = v # Replace existing item's value
                self._rebalance_access(p) # hood for balanced-tree subclass
                return
            else: # If key k is new to the tree...
                item = self._Item(k, v)
                if p.key() < k: # Decide whether to add as left or right child of p
                    leaf = self._add_right(p, item) # inherited from LBT
                else:
                    leaf = self._add_left(p, item)
        self._rebalance_insert(leaf) # hook for balanced-tree subclasses

    def __iter__(self):
        """Generate an iteration of all keys in the map in order."""
        p = self.first() # Abstractions from the traversal methods have already done nearly
        while p is not None: # all the work. 
            yield p.key()
            p = self.after(p)

    def delete(self, p):
        """Remove the item at given Position."""
        self._validate(p) # inherited from LBT
        if self.left(p) and self.right(p): # p has two children
            replacement = self._subtree_last_position(self.left(p))
            self._replace(p, replacement.element()) # from LBT
            p = replacement
        # now p has at most one child
        parent = self.parent(p)
        self._delete(p) # inherited from LBT
        self._rebalance_delete(parent) # If root was deleted, parent is now None.
            # ^ hook, LBT doesn't have this method.

    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""
        if not self.is_empty():
            p = self._subtree_search(self.root(), k)
            if k == p.key():
                self.delete(p) # rely on positional version
                return # successful deletion complete
            self._rebalance_access(p) # hook for balanced tree subclasses
        raise KeyError(f'KeyError: {repr(k)}')

    #### Hooks for rebalancer methods ####

    def _rebalance_access(self, p):
        pass

    def _rebalance_insert(self, p): # empty hook
        """
        Args:
            p (Position): A Position object.
        """
        pass

    def _rebalance_delete(self, p):
        pass

    #### Nonpublic methods for rotating and restructuring
        # Factory-ed here for reusability in inheritor classes

    def _relink(self, parent, child, make_left_child: bool) -> None:
        """Relink parent node with child node (supports child being None).

        Args:
            parent (Position):
            child (Position):
            make_left_child (bool):
        """
        if make_left_child: # make it a left child
            parent._left = child
        else: # make it a right child
            parent._right = child
        if child is not None: # make child point to parent
            child._parent = parent

    def _rotate(self, p):
        """Rotate Position p above its parent."""
        x = p._node
        y = x._parent # we assume this exists
        z = y._parent # grandparent (may be None)
        if z is None:
            self._root = x # x becomes root
            x._parent = None
        else: # x becomes a direct child of z
            self._relink(z,
                         x,
                         y == z._left) # passing an expression that will evaluate to False as the make_left_child argument
        # Now rotate x and y, including transfer of middle subtree:
        if x == y._left:
            self._relink(y, x._right, True) # x._right becomes left child of y
            self._relink(x, y, False) # y becomes right child of x
        else:
            self._relink(y, x._left, False) # x._left becomes right child of y
            self._relink(x, y, True) # y becomes left child of x

    def _restructure(self, x) -> Position:
        """Perform trinode restructure of Position x with parent/grandparent."""
        y = self.parent(x)
        z = self.parent(y)
        assert type(x) == self.Position
        assert type(y) == self.Position
        assert type(z) == self.Position, f"z was {z} with type {type(z)}"
        if (x == self.right(y)) == (y == self.right(z)): # matching alignments
            self._rotate(y) # single rotation (of y)
            return y # y is the new subtree root
        else: # double rotation
            self._rotate(x)
            self._rotate(x)
            return x
