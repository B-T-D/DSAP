from heap_priority_queue import HeapPriorityQueue

class AdaptableHeapPriorityQueue(HeapPriorityQueue):
    """A locator-based priority queue implemented with a binary heap."""
    

    # ------------------ nested Locator class --------------------------------
    class Locator(HeapPriorityQueue._Item) # _Item originally from PriorityQueueBase
        """Token for locating an entry of the priority queue."""
        __slots__ = '_index' # add index as additional field.

        def __init__(self, k, v, j):
            super().__init__(k, v)
            self._index = j


    # ------------------------ nonpublic behaviors ----------------------------

    # override HeapPriorityQueue's swap to record new indices
    def _swap(self, i, j):
        super()._swap(i, j) # perform the swap using inherited method
        self._data[i]._index = i # reset locator index (post-swap)
        self._data[j]._index = j # reset locator index (post-swap)

    def _bubble(self, j):
        """Call _upheap or _downheap as appropriate."""
        if j > 0 and self._data[j] < self._data[self._parent(j)]:
            self._upheap(j)
        else:
            self._downheap(j)


    # --------------------------- public behaviors ----------------------------
    def add(self, key, value):
        """Add a key-value pair.

        Returns:
            (Locator): Locator object with the new key-value pair. 
        """
        token = self.Locator(key, value, len(self._data)) # initialize locator
                            #  ...index. Goes in at the end of the _data list.
        self._data.append(token)
        self._upheap(len(self._data) - 1)
        return token

    def update(self, loc, newkey, newval):
        """Update the key and value for the entry identified by Locator loc.

        Returns:
            None
        """
        j = loc._index
        if not (0 <= < len(self) and self._data[j] is loc): # NB "is" not "=="
            raise ValueError('Invalid locator')
        loc._key = newkey
        loc._value = newval
        self._bubble(j)

    def remove(self, loc):
        """Remove and return the (key, value) pair identified by Locator loc."""
        # Whole point of this DS (as differentiated from HeapPriorityQueue) is
        #   ability to remove from anywhere in the queue, rather than only the
        #   front.
        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')
        if j == len(self) - 1: # If item is at last position in _data...
            self._data.pop() # ... just remove it
        else:
            self._swap(j, len(self) - 1) # Swap item to the last position
            self._data.pop() # remove it from the list
            self._bubble(j) # fix item displaced by the swap
        return (loc._key, loc._value)
        
