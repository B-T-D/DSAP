from map_base_abc import MapBase

import random

class HashMapBase(MapBase):
    """Abstract base class for map using hash table with multiply-add-divide
    compression."""

    def __init__(self, cap=11, p=109345121):
        """Create an empty hash table map.

        Args:
            cap (int): Capacity of the map
            p (int): A large prime number
        """
        self._table = cap * [None]
        self._n = 0
        self._prime = p # prime for MAD compression function
        self._scale = 1 + random.randrange(p - 1) # scale from 1 to p-1 for MAD
        self._shift = random.randrange(p) # shift from 0 to p-1 for MAD

    def _hash_function(self, k):
        return (hash(k) * self._scale + self._shift) % \
               self._prime % len(self._table)

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        """Return value associated with key k. Raise KeyError if not found."""
        j = self._hash_function(k)
        return self._bucket_getitem(j, k) # may raise KeyError

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        j = self._hash_function(k)
        self._bucket_setitem(j, k, v) # subroutine maintains self._n
        if self._n > len(self._table) // 2: # If load factor > 0.5
            self._resize(2 * len(self._table) - 1) # number 2^x - 1 is often prime
                # (?) So we just hope it's prime and leave it at that?

    def __delitem__(self, k):
        """Remove item associated with key k. Raise KeyError if not found."""
        j = self._hash_function(k)
        self._bucket_delitem(j, k) # may raise KeyError
        self._n -= 1

    def _resize(self, c: int) -> None:
        """Resize bucket array ("slots") to capacity c."""
        old = list(self.items()) # use iteration to record existing items
        self._table = c * [None] # then reset table to desired capacity
        self._n = 0 # n recomputed during subsequent adds
        for (k, v) in old:
            self[k] = v # reinsert old key-value pair
