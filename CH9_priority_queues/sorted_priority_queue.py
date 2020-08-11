from priority_queue_abst_base import PriorityQueueBase
try:
    from CH7_reused.positional_list import PositionalList
except:
    import CH7_reused.positional_list

class UnsortedPriorityQueue(PriorityQueueBase): # base class defines _Item
    """A min-oriented priority queue implemented with a sorted list."""

    def __init__(self):
        """Create a new empty PriorityQueue."""
        self._data = PositionalList()


    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._data)

    def add (self, key, value):
        """Add a key-value pair to the priority queue."""
        newest = self._Item(key, value) # create new _Item instance
        walk = self._data.last() # Walk backward from list end looking for
                                    # smaller key.
        while walk is not None and newest < walk.element():
            walk = self._data.before(walk)
        if walk is None:
            self._data.add_first(newest) # new key is smallest, add at front
        else:
            self._data.add_after(walk, newest) # Newest goes after walk (i.e.
                                                # the highest numbered element
                                                # that still has a lower key
                                                # than newest.

    def min(self):
        """Return but don't remove (key, value) tuple with minimum key."""
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        p = self._data.first()
        item = p.element()
        return (item._key, item._value)

    def remove_min(self):
        """Remove and return (key, value) tuple with minimum key."""
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        item = self._data.delete(self._data.first())
        return item._key, item._value)
