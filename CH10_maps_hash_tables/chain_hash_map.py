from hash_map_base_abc import HashMapBase
from unsorted_table_map import UnsortedTableMap


class ChainHashMap(HashMapBase):
    """Hash map implemented with separate chaining for collision resolution."""

    
    def _bucket_getitem(self, j, k):
        """
        Args:
            j (int): the hash value for key k.
        """
        bucket = self._table[j] # Each bucket gets its own table (python list).
                                #   This is the heart of what makes this a chaining
                                #   implementation. In non-chaining, there's only
                                #   one _table.
        if bucket is None:
            raise KeyError('Key Error: ' + repr(k)) # no match found
        return bucket[k] # may raise KeyError

    def _bucket_setitem(self, j, k, v) -> None:
        """
        Args:
            v (object): The new value to set. 
        """
        if self._table[j] is None:
            self._table[j] = UnsortedTableMap() # bucket is new to the table
        oldsize = len(self._table[j])
        self._table[j][k] = v
        if len(self._table[j]) > oldsize: # key was new to the table
            self._n += 1 # increase overall map size

    def _bucket_delitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error: ' + repr(k)) # no match found
        del bucket[k] # may raise KeyError (this recursively calls this function

    def __iter__(self):
        for bucket in self._table:
            if bucket is not None: # a nonempty slot
                for key in bucket:
                    yield key
        
        


