import unittest

from sorted_table_map import SortedTableMap

class TestBasicTable(unittest.TestCase):
    """Basic-coverage tests."""

    def setUp(self):
        self.stmap = SortedTableMap()

    def test_init(self):
        self.assertIsInstance(self.stmap, SortedTableMap)

    def test_len(self):
        self.assertEqual(len(self.stmap), 0)
        for i in range(5):
            self.stmap[i] = i
        self.assertEqual(len(self.stmap), 5)

    def test_setitem_getitem(self):
        test_key = "key"
        test_value = "value"
        with self.assertRaises(KeyError):
            returned = self.stmap[test_key] # not in the table yet
        self.stmap[test_key] = test_value
        self.assertEqual(self.stmap[test_key], test_value)
        # cover the overwrite-existing case in __setitem__:
        updated_value = "updated value"
        self.stmap[test_key] = updated_value
        self.assertEqual(self.stmap[test_key], updated_value)

    def test_delitem(self):
        test_key = "key"
        test_value = "value"
        # Should raise key error if not in table
        with self.assertRaises(KeyError):
            del self.stmap[test_key]
        self.stmap[test_key] = test_value
        del self.stmap[test_key]
        self.assertEqual(len(self.stmap), 0)

    def test_iter(self):
        for i in range(5):
            self.stmap[i] = f"value for key {i}"
        assert len(self.stmap) == 5
        i = 0
        for key in self.stmap.keys():
            self.assertEqual(key, i)
            i += 1

    def test_reversed(self):
        for i in range(4, -1, -1):
            self.stmap[i] = f"value for key {i}"
        assert len(self.stmap) == 5
        i = 4
        for key in reversed(self.stmap):
            self.assertEqual(key, i)
            i -= 1

class TestAccessorsWithAlphabetTable(unittest.TestCase):
    """Uses a table containing 26 (number, letter) k-v pairs to test the
    methods that return min, max, less than, etc."""

    def setUp(self):
        self.stmap = SortedTableMap()
        for i in range(ord("a"), ord("a") + 26):
            key = i - ord("a")
            self.stmap[key] = chr(i)

    def test_find_min(self):        
        expected_min = (0, "a")
        actual_min = self.stmap.find_min()
        self.assertEqual(expected_min, actual_min)

    def test_find_max(self):
        expected_max = (25, "z")
        actual_max = self.stmap.find_max()
        self.assertEqual(expected_max, actual_max)

    def test_find_ge(self):
        # least key greater than or equal to 15 should be 15.
        key = 15
        expected = (15, "p")
        actual = self.stmap.find_ge(key)
        self.assertEqual(expected, actual)

    def test_find_lt(self):
        # Greatest key strictly less than 15 should be 14
        key = 15
        expected = (14, "o")
        actual = self.stmap.find_lt(key)
        self.assertEqual(expected, actual)

    def test_find_gt(self):
        # Least key strictly greater than 15 should be 16.
        key = 15
        expected = (16, "q")
        actual = self.stmap.find_gt(key)
        self.assertEqual(expected, actual)

    def test_find_range(self):
        # No start and stop=14 should yield all kvps from (0, "a") to (14, "o")
        expected = []
        for i in range(ord("a"), ord("a") + 15):
            expected_key = i - ord("a")
            expected_value = chr(i)
            expected.append((expected_key, expected_value))
        actual = [i for i in self.stmap.find_range(start=None, stop=15)]
        assert len(actual) == 15
        self.assertEqual(expected, actual)

        # start=10 and stop=20 should yield all k-v pairs from (10, "k") to
        #   (19, "t")
        expected = []
        for i in range(ord("a") + 10, ord("a") + 20):
            expected_key = i - ord("a")
            expected_value = chr(i)
            expected.append((expected_key, expected_value))
        actual = [i for i in self.stmap.find_range(start=10, stop=20)]
        assert len(actual) == 10
        self.assertEqual(expected, actual)

    def test_find_key_methods_return_none_when_table_empty(self):
        """Do the methods that find a key based on an arithmetic comparison
        criterion return None when the table is empty?"""
        empty_stmap = SortedTableMap()
        k = 1
        self.assertIsNone(empty_stmap.find_min())
        self.assertIsNone(empty_stmap.find_max())
        self.assertIsNone(empty_stmap.find_ge(k))
        self.assertIsNone(empty_stmap.find_lt(k))
        self.assertIsNone(empty_stmap.find_gt(k))
        

if __name__ == '__main__':
    unittest.main()
