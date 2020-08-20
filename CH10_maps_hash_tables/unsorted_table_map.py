from map_base_abc import MapBase

class UnsortedTableMap(MapBase):
    """Map implementation using an unordered list."""

    def __init__(self):
        """Create an empty map."""
        self._table = [] # list of _Item objects

    def __getitem__(self, k):
        """Return value associated with key k. Raise KeyError if not found."""
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError('Key Error: ' + repr(k))

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        for item in self._table:
            if k == item._key: # Found a match:
                item._value = v # reassign value
                return          # then end execution
        # Didn't find match for key:
        self._table.append(self._Item(k, v))

    def __delitem__(self, k):
        """Remove item associated with key k. Raise KeyError if not found."""
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                self._table.pop(j) # remove item with list's pop method
                return              # then end execution
        raise KeyError('Key Error: ' + repr(k))

    def __len__(self):
        """Return number of items in the map."""
        return len(self._table)

    def __iter__(self):
        """Generate iteration of the map's keys."""
        for item in self._table:
            yield item._key
