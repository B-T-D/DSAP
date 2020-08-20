import unittest

from chain_hash_map import ChainHashMap
from unsorted_table_map import UnsortedTableMap

class TestSimpleMap(unittest.TestCase):
    """Basic-coverage functionality tests."""

    def setUp(self):
        self.chmap = ChainHashMap()

    def test_init(self):
        self.assertIsNotNone(self.chmap)
        self.assertIsInstance(self.chmap, ChainHashMap)

    def test_underlying_table_is_list(self):
        """Is the primary table object (whose elements are the buckets that
        can themselves hold multiple colliding elements) a Python list?"""
        self.assertIsInstance(self.chmap._table, list)

    def test_bucket_is_nested_unsorted_table(self):
        """Is the bucket object to be used to hold multiple colliding keys
        an unsorted table map item, rather than e.g. a pyhon list or the type
        of whatever element is stored there?"""
        key = "test key"
        hash = self.chmap._hash_function(key)
        value = "test value"
        self.assertIsNone(self.chmap._table[hash]) # Should be None, before anything's stored
                                    # there.
        self.chmap[key] = value
        self.assertIsInstance(self.chmap._table[hash],
                              UnsortedTableMap)
        
        

    def test_setitem_getitem(self):
        key = "test key"
        value = "test value"
        self.chmap[key] = value
        self.assertEqual(self.chmap[key], value)

    def test_getitem_raises_key_error(self):
        key = "missing"
        with self.assertRaises(KeyError):
            return self.chmap[key]

    def test_setitem_update_existing(self):
        key = "test"
        value = 0
        self.chmap[key] = value
        new_value = 1
        self.chmap[key] = new_value
        self.assertEqual(self.chmap[key], new_value)

    def test_delitem(self):
        assert len(self.chmap) == 0
        key = "delete me"
        value = 1
        self.chmap[key] = value
        del self.chmap[key]
        self.assertEqual(len(self.chmap), 0)
        with self.assertRaises(KeyError):
            return self.chmap[key]

    def test_delitem_raises_keyerror(self):
        """Does __delitem__ raise KeyError when trying to delete a key-value
        pair that's not in the map?"""
        key = "missing"
        with self.assertRaises(KeyError):
            del self.chmap[key]

    def test_len(self):
        self.chmap["key"] = 1
        self.assertEqual(len(self.chmap), 1)
        for i in range(3):
            self.chmap[i] = i
        self.assertEqual(len(self.chmap), 4)

    def test_resize(self):
        # default capacity should be 11
        assert len(self.chmap._table) == 11
        # adding 6 elements should cause a resize. Resize should happen when
        #   load factor drops below 0.5 (fewer than two slots per element stored).
        for i in range(5):
            self.chmap[i] = i
        self.assertEqual(len(self.chmap._table), 11) # shouldn't have changed yet
        self.chmap[6] = 6 # adding the 6th should cause the resize
        expected_new_size = 11 * 2 - 1
        self.assertEqual(len(self.chmap._table), expected_new_size)

if __name__ == '__main__':
    unittest.main()
