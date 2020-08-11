class PriorityQueueBase:
    """Abstract base class for a priority queue."""

    class _Item:
        """Lightweight composite to store priority queue items. Composes a
        key-value pair into a single object."""
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __lt__(self, other):
            """Overload less-than operator."""
            return self._key < other._key # Compare items based on their keys

    def is_empty(self): # concrete method assuming abstract len
                        #   (len would need to be concreteley implemented in the
                        #   concrete subclass; not implemented here)
        """Return True if the priority queue is empty."""
        return len(self) == 0
