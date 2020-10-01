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
        
        if k == p.key(): # base case 1: found match
            return p
        elif k < p.key(): # search left subtree recursively
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
        else: # search right subtree recursively
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        return p # base case 2: No match, return the root position of the
                    # searched subtree.

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

def main():
    print("imports ok")

if __name__ == '__main__':
    main()
