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
        searched."""
        if k == p.key():
            return p
        elif k < p.key():
            if self.left(p) is not None

def main():
    print("imports ok")

if __name__ == '__main__':
    main()
