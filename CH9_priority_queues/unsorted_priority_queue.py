from priority_queue_abst_base import PriorityQueueBase
try:
    from CH7_reused.positional_list import PositionalList
except:
    import CH7_reused.positional_list

class UnsortedPriorityqQueue(PriorityQueueBase): # base class defins _Item
    """A min-oriented priority queue implemented with an unsorted list."""

    def _find_min(self):
        """Return Position of item with minimum key."""
        if self.is_empty(): # is.empty() inherited from abst base class
            raise Empty('Priority queue is empty')
        small = self._data.first()
        walk = self._data.after(small)
        while walk is not None:
            if walk.element() < small.element():
                small = walk
            walk = self._data.after(walk)
        return small

    def __init__(self):
        """Create a new empty priority queue."""
        self._data = PositionalList()

    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._data)

    def add(self, key, value):
        """Add a key-value pair to the priority queue."""
        self._data.add_last(self._Item(key, value))

    def min(self):
        """Return, but don't remove, (key, value) tuple with minimum key."""
        p = self._find_min()
        item = p.element()
        return (item._key, item._value)

    def remove_min(self):
        """Remove and return (key, value) tuple with minimum key."""
        p = self._find_min()
        item = self._data.delete(p)
        return (item._key, item._value)
