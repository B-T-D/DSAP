import unittest

from unsorted_table_map import UnsortedTableMap

class TestSimpleTable(unittest.TestCase):
    """Basic functionality tests using a simple table."""

    def setUp(self):
        self.table = UnsortedTableMap()

    def test_init(self):
        self.assertIsNotNone(self.table)
        self.assertIsInstance(self.table, UnsortedTableMap)

    def test_setitem_getitem(self):
        key = "test key"
        value = "test value"
        self.table[key] = value
        self.assertEqual(self.table[key], value)

    def test_getitem_raises_keyerror(self):
        """Does __getitem__ raise KeyError when the key isn't in the table?"""
        key = "missing"
        with self.assertRaises(KeyError):
            return self.table[key]

    def test_setitem_update_existing(self):
        key = "test"
        value = 0
        self.table[key] = value
        new_value = 1
        self.table[key] = new_value
        self.assertEqual(self.table[key], new_value)

    def test_delitem(self):
        assert len(self.table) == 0
        key = "delete me"
        value = 1
        self.table[key] = value
        del self.table[key]
        self.assertEqual(len(self.table), 0)
        with self.assertRaises(KeyError):
            return self.table[key]

    def test_delitem_raises_keyerror(self):
        """Does __delitem__ raise KeyError when trying to delete a key-value
        pair that's not in the map?"""
        key = "missing"
        with self.assertRaises(KeyError):
            del self.table[key]

    def test_iter(self):
        items = {"a": 1, "b": 2, "c": 3}
        for key in items.keys():
            self.table[key] = items[key]
        assert len(self.table) == 3
        for key in self.table.keys():
            self.assertIsNotNone(self.table[key])

if __name__ == '__main__':
    unittest.main()
