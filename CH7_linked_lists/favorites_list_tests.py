import unittest

from favorites_list import FavoritesList

class TestObviousCases(unittest.TestCase):
    """Quick, easy tests for basics."""

    def setUp(self):
        self.favs = FavoritesList()

    def test_len(self):
        self.assertEqual(0, len(self.favs))

    def test_is_empty(self):
        self.assertTrue(self.favs.is_empty())
        self.favs._data.add_last("added")
        self.assertFalse(self.favs.is_empty())

    def test_access(self): 
        # Add 5 elements
        for i in range(5):
            added = self.favs._data.add_last(self.favs._Item(f"Entry {str(i)}"))
        assert len(self.favs) == 5
        # Access the last element 5 times
        fifth = added.element() # an _Item object with attributes ._value and ._count
        for i in range(5):
            self.favs.access(fifth._value) # you access the value itself,
                                            # not the containing _Item
        self.assertEqual(fifth._count, 5)

    def test_remove(self):
        string = "test element"
        element = self.favs._data.add_last(self.favs._Item(string))
        assert len(self.favs) == 1
        #self.favs.remove("test element") # This would also work, doesn't need
                                            # to be the same string in memory
        self.favs.remove(string)
        self.assertEqual(len(self.favs), 0)

    def test_top(self):
        elements = [f"Entry {str(i)}" for i in range(5)]
        for element in elements:
            self.favs._data.add_last(self.favs._Item(element))
        assert len(self.favs) == 5
        # Access them in "oppposite order"--#5 accessed 5 times, 4, 3, 2, 1
        for i in range(len(elements) - 1, 0, -1):
            for j in range(i):
                self.favs.access(elements[i])
        top_3 = [] * 3
        for e in self.favs.top(3):
            top_3.append(e)
        expected = ['Entry 4', 'Entry 3', 'Entry 2']
        self.assertEqual(top_3, expected)
        
            
if __name__ == "__main__":
    unittest.main()

