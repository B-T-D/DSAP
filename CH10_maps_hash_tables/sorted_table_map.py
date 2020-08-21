from map_base_abc import MapBase

class SortedTableMap(MapBase):
    """Map implementation using a sorted table."""

    ### nonpublic behaviors ###
    def _find_index(self, k, low: int, high: int) -> int:
        # A binary search implementation. Does the main work for almost all of
        #   the public accessor methods. 
        """Return index of the leftmost item with key greater than or equal to
        k. Return high + 1 if no such item qualifies.

        That is, j will be returned such that:
            all items of slice table[low:j] have key < k
            all items of slice table[j:high+1] have key >= k

        Args:
            k (suitable object): Object of type suitable for use as a key in
                a sorted table--must support comparison operators.
        """
        if high < low:  # no element qualifies
            return high + 1 # base case 1: found no match
        else:
            mid = (low + high) // 2
            if k == self._table[mid]._key:
                return mid # base case 2: found exact match
            elif k < self._table[mid]._key:
                return self._find_index(k, low, mid - 1) # NB may return mid
            else:
                return self._find_index(k, mid + 1, high) # answer is right of mid

    ### public behaviors ###
    def __init__(self):
        """Create an empty map."""
        self._table = [] # underlying table is a Python list

    def __len__(self):
        """Return number of items in the map."""
        return len(self._table)

    def __getitem__(self, k):
        """Return value associated with key k (raise KeyError if not found)."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError('Key Error: ' + repr(k))
        return self._table[j]._value

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table) and self._table[j]._key == k: # if key k is already in the table
            self._table[j]._value = v # reassign value
        else:
            self._table.insert(j, self._Item(k, v)) # add new item

    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError('Key Error: ' + repr(k))
        self._table.pop(j) # use list object's pop method to delete item

    def __iter__(self):
        """Generate the keys of the map ordered from minimum to maximum."""
        for item in self._table:
            yield item._key

    def __reversed__(self):
        """Generate keys of the map ordered from maximum to minimum."""
        # We're telling Python that reversed() should generate the keys as
        #   opposed to something else. Same as our __iter__ specifying that
        #   we want to generate the keys.
        for item in reversed(self._table): # can call reversed() here because
                                            #   self._table is a list, so it
                                            # already has a __reversed__ method.
            yield item._key

    def find_min(self):
        """Return (key, value) pair with minimum key (or None if empty)."""
        if len(self._table) > 0:
            return (self._table[0]._key, self._table[0]._value)
        else:
            return None

    def find_max(self):
        """Return (key, value) pair with maximum key (or None if empty)."""
        if len(self._table) > 0:
            return (self._table[-1]._key, self._table[-1]._value)
        else:
            return None

    def find_ge(self, k): # "ge" -> "greater than or equal to"
        """Return (key, value) pair with least key greater than or equal to k."""
        j = self._find_index(k, 0, len(self._table) - 1) # j's key >= k
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_lt(self, k): # "less than"
        """Return (key, value) pair with greatest key strictly less than k."""
        j = self._find_index(k, 0, len(self._table) - 1) # j's key >= k
        if j > 0:
            return (self._table[j-1]._key, self._table[j-1]._value) # Note use of j - 1
        else:
            return None

    def find_gt(self, k):
        """Return (key, value) pair with least key strictly greater than k."""
        j = self._find_index(k, 0, len(self._table) - 1) # j's key >= k
        if j < len(self._table) and self._table[j]._key == k:
            j += 1 # advance it one more to reach first item after match, i.e.
                    # the least key strictly greater than target key k
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_range(self, start, stop):
        """Iterate all (key, value) pairs such that start <= key < stop.

        If start is None, iteration begins with minimum key of map.
        If stop is None, iteration continues through the maximum key of map.
        """
        if start is None:
            j = 0
        else:
            j = self._find_index(start, 0, len(self._table) - 1) # find first result
        while j < len(self._table) and\
              (stop is None or self._table[j]._key < stop):
            yield (self._table[j]._key, self._table[j]._value)
            j += 1
            
        
