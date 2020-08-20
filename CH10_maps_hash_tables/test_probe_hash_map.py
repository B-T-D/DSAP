import unittest

from probe_hash_map import ProbeHashMap
from map_base_abc import MapBase

class TestSimpleMap(unittest.TestCase):
    """Basic-coverage tests."""

    def setUp(self):
        self.phmap = ProbeHashMap()

    def test_init(self):
        self.assertIsNotNone(self.phmap)
        self.assertIsInstance(self.phmap, ProbeHashMap)

    def test_underlying_table_is_list(self):
        """Is the table object a Python list?"""
        self.assertIsInstance(self.phmap._table, list)

    def test_bucket_element_is_underlying_element_type(self):
        """Is the type of the object stored at a given index in the main table
        the type of whatever primary-data element was stored there (rather than
        e.g. a nested list-bucket as in a chain hash map)?"""
        key = "test key"
        hash = self.phmap._hash_function(key)
        value = 7
        self.phmap[key] = value
        # the thing stored at table[hash] should be an internal _Item wrapper
        #   object, inherited from MapBase abc.
        self.assertIsInstance(self.phmap._table[hash], MapBase._Item)
        self.assertIsInstance(self.phmap._table[hash]._value,
                              int) # This is what accesses the element itself
            # One of _Item's instance variables is _value

    def test_is_available(self):
        """Does the _is_available method correctly return True and False when
        index position is and isn't already occupied?"""
        index = self.phmap._hash_function("test") # remember which index will
                                                    # be filled
        self.assertTrue(self.phmap._is_available(index))
        self.phmap["test"] = "test value"
        self.assertFalse(self.phmap._is_available(index))

    def test_find_slot(self):
        """Does the method return (True, {index at which key was found} when
        the key was in the bucket at the searched index?"""
        # First test on a key we know isn't in the table:
        key = "test key"
        hash = self.phmap._hash_function(key)
        value = "test value"
        # It takes the key itself as an argument, don't need to manually hash
        #   it here.
        checked_index = 0
        expected = (False, checked_index) # Checked index should be the value
                                            # of firstAvail index
        self.assertEqual(expected, self.phmap._find_slot(j=checked_index,
                                                         k=key))

        # Then put it in the table at a known index position:
        # it should go in at localvar "hash"
        #   (i.e. 4 as currently implemented)
        self.phmap[key] = value
        expected = (True, hash)
        self.assertEqual(expected, self.phmap._find_slot(j=hash,
                                                        k=key))

    def test_setitem_getitem(self):
        key = "test key"
        value = "test value"
        self.phmap[key] = value
        self.assertEqual(self.phmap[key], value)

    def test_getitem_raises_key_error(self):
        key = "missing"
        with self.assertRaises(KeyError):
            return self.phmap[key]

    def test_setitem_update_existing(self):
        key = "test"
        value = 0
        self.phmap[key] = value
        new_value = 1
        self.phmap[key] = new_value
        self.assertEqual(self.phmap[key], new_value)

    def test_delitem(self):
        assert len(self.phmap) == 0
        key = "delete me"
        value = 1
        self.phmap[key] = value
        del self.phmap[key]
        self.assertEqual(len(self.phmap), 0)
        with self.assertRaises(KeyError):
            return self.phmap[key]

    def test_delitem_raises_keyerror(self):
        """Does __delitem__ raise KeyError when trying to delete a key-value
        pair that's not in the map?"""
        key = "missing"
        with self.assertRaises(KeyError):
            del self.phmap[key]

    def test_len(self):
        self.phmap["key"] = 1
        self.assertEqual(len(self.phmap), 1)
        for i in range(3):
            self.phmap[i] = i
        self.assertEqual(len(self.phmap), 4)

    def test_iter(self):
        for i in range(5):
            self.phmap[i] = i
        for key, value in self.phmap.items():
            self.assertEqual(key, value)

if __name__ == '__main__':
    unittest.main()
