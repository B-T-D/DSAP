from priority_queue_abst_base import PriorityQueueBase

class HeapPriorityQueue(PriorityQueueBase): # base class defines _Item
    """A min-oriented priority queue implemented with a binary heap.

    Binary heap uses an array-based representation (not linked positions
    as in a tree). Utility methods compute level numbering of parents and
    children in a way that supports using tree-like terminology of "parent",
    "child", "left", and "right".
    """

    # -------------------------- nonpublic behaviors --------------------------
    def _parent(self, j):
        return (j - 1) // 2

    def _left(self, j):
        """See DSAP at 376 for arithmetic logic of this. Elements are stored in
        the array at increasingly distant positions from their parent (all
        children of left are listed, then all children of right).

        Returns:
            (int): The Python-list index position of the element representing
                the left child of element j. 
        """
        return 2 * j + 1

    def _right(self, j):
        # Right child is array-ed second, so add 2 rather than 1.
        return 2 * j + 2

    def _has_left(self, j):
        """Return True if element j has a left "child" in the "tree", else
        False."""
        return self._left(j) < len(self._data) # if the index returned by calling
                                            # self._left() utility method is
                                            # beyond the end of the list, then
                                            # element j has no left child.

    def _has_right(self, j):
        """Return True if element j has a right "child" in the "tree", else
        False."""
        return self._right(j) < len(self._data) # index beyond end of list?

    def _swap(self, i, j):
        """Swap the elements at indices i and j of the array."""
        self._data[i], self._data[j] = self._data[j], self._data[i]
        # NB you don't actually need to manually code-out a "temp".

    def _upheap(self, j: int):
        """Recursively up-heap bubble elements until heap-order property is
        restored (all parents less than or equal to their children)."""
        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent) # Recurse at position of parent

    def _downheap(self, j):
        """Recursively down-heap bubble an element until heap-order property
        is restored."""
        if self._has_left(j):
            left = self._left(j)
            small_child = left  # Right could still be smaller
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child) # recurse at position of small child

    # ------------------------ public behaviors -------------------------------
    def __init__(self):
        """Create a new empty HeapPriorityQueue."""
        self._data = []

    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._data)

    def add(self, key, value):
        """Add a key-value pair to the priority queue."""
        self._data.append(self._Item(key, value))
        self._upheap(len(self._data) - 1) # upheap the newly added position)

    def min(self):
        """Return but don't remove (key, value) tuple with minimum key.

        Raise Empty exception if empty.
        """
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        item = self._data[0]
        return (item._key, item._value)

    def remove_min(self):
        """Remove and return (key, value) tuple with minimum key.

        Raise Empty exception if empty.
        """
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        self._swap(0, len(self._data) - 1) # Put minimum item at end (list's representation of bottom-right)
        item = self._data.pop() # Then remove that item from the list
        self._downheap(0) # Then fix the new root to restore heap-order property
        return (item._key, item._value)
                
            

    
