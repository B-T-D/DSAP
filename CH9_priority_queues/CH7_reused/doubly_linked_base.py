class _DoublyLinkedBase:
    """
    An internal base class providing doubly linked list representation (DSAP
    has a couple different DLL-based implementations share this by inheriting
    from it).
    """

    class _Node:
        """Lightweight, nonpublic class for storing a doubly linked node."""
        __slots__ = '_element', '_prev', '_next'

        def __init__(self, element, prev, next):
            """
            Args:
                _prev (_Node): Node object
                _next (_Node): Node object
                _element (object): Object of whatever type is stored in the LL's
                    primary data.
            """
            self._element = element # user's element (the data)
            self._prev = prev # link to previous node
            self._next = next # link to next node

    def __init__(self):
        """Create an empty list."""
        self._header = self._Node(None, None, None) # No element, no prev and no next (for now)
        self._trailer = self._Node(None, None, None) # Couldn't you pass _header as next here?
        self._header._next = self._trailer # header's init next is trailer
        self._trailer._prev = self._header # trailer's init prev is header
        self._size = 0

    def __len__(self):
        """Return the number of elements in the list."""
        return self._size

    def is_empty(self):
        """Return True if list is empty."""
        return self._size == 0

    def _insert_between(self, e, predecessor, successor):
        """Add element e between two existing nodes and return new node."""
        newest = self._Node(e, predecessor, successor) # linked to neighbors
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest

    def _delete_node(self, node):
        """Delete nonsentinel node from the list and return its element."""
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element # store deleted element so it can be returned
        node._prev = node._next = node._element = None # Deprecate the node.
            # Element was deleted (by writing node._element to None), but the node
            #   is merely deprecated--it still exists.
        return element # Return the deleted element

def test():
    DLB = _DoublyLinkedBase()
    assert len(DLB) == 0
    assert DLB.is_empty() == True
    inserted = DLB._insert_between('first insertion', DLB._header, DLB._trailer)
    assert len(DLB) == 1
    another_inserted = DLB._insert_between('second insertion', inserted, DLB._trailer)
    assert DLB.is_empty() == False
    assert len(DLB) == 2
    DLB._delete_node(inserted)
    assert len(DLB) ==1
    DLB._delete_node(another_inserted)
    assert len(DLB) == 0
    assert DLB.is_empty() == True
    print("Simple assert tests ok")

if __name__ == '__main__':
    test()
        
