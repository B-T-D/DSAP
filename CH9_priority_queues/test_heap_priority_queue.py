import unittest

from heap_priority_queue import HeapPriorityQueue


class TestMainExample(unittest.TestCase):
    """Basic-coverage tests of the main methods, using the running example
    heap introduced at DSAP 371."""

    def setUp(self):
        self.heap = HeapPriorityQueue()
        self.heap.add(key=4, value="C")
        self.heap.add(key=5, value="A")
        self.heap.add(key=6, value="Z")

        # left and right children of depth 1 right child (5, A):
        self.heap.add(key=15, value="K")
        self.heap.add(key=9, value = "F")

        # left and right children of depth 1 left child (6, Z):
        self.heap.add(key=7, value="Q")
        self.heap.add(key=20, value="B")

        # depth 3 children
        self.heap.add(17, "X")
        self.heap.add(25, "J")
        self.heap.add(14, "E")
        self.heap.add(12, "H")
        self.heap.add(11, "S")
        self.heap.add(13, "W")

    def test_init(self):
        """Was an object of the intended type initialized?"""
        self.assertIsInstance(self.heap, HeapPriorityQueue)

    def test_left(self):
        """Does the _left method correctly return the list entry represnting
        the left child of data_list[j] on the pretend tree?"""
        expected = 1 # First layer left child should be at _data[1]
        self.assertEqual(self.heap._left(0), expected) # root is _data[0]

    def test_right(self):
        """Does the _right method correctly return the _data list index position
        of the _data list element that represents the right child on the pretend
        tree?"""
        expected = 2 # First layer right child should be at _data[2]
        self.assertEqual(self.heap._right(0), expected) # root is _data[0]

    def test_has_left(self):
        """Does the _has_left method return True for an element that has a
        left child and false for one that doesn't?"""
        # (15, K) should be an internal node at _data[3] (both L and R children):
        self.assertTrue(self.heap._has_left(3))
        # (20, B) should be a leaf at _data[6]:
        self.assertFalse(self.heap._has_left(6))

    def test_has_right(self):
        """Does the _has_right method return True for an element that has a
        right child and false for one that doesn't?"""
        # (15, K) has both left and right:
        self.assertTrue(self.heap._has_right(3))
        # (20, B) should be a leaf at _data[6]:
        self.assertFalse(self.heap._has_right(6))

    def test_upheap(self):
        """Does the _upheap method bubble an out-of-heap-order item up the
        tree as intended?"""
        # Element added with lower key than initial minimum of 4 should require
        #   calling upheap to bubble it all the way to the top:
        new = (1, "upheap-bubbling test")
        self.heap.add(key=new[0], value=new[1]) 
        self.assertEqual(new, self.heap.min()) # new item should now be at top

    def test_downheap(self):
        """Does the _downheap method bubble an out-of-heap-order ite down
        the tree as intended?"""
        # Directly set the top _data[0]'s key to an integer higher than any
        #   in the setUp heap:
        self.heap._data[0]._key = 50
        # min() method should now incorrectly return (50, "C")
        expected = (50, "C")
        assert self.heap.min() == expected
        self.heap._downheap(0)
        # new min should be (5, A)
        new_top = (5, "A")
        self.assertEqual(new_top, self.heap.min())
        # Should have bubbled down to where (12, H) was, at data[8]
        self.assertEqual("C", self.heap._data[10]._value)

    def test_swap(self):
        """Does the _swap method swap the elements at indices i and j of
        the array?"""
        i = 1 # For test, will swap i=1, j=2. Left and right children of root
        j = 2
        starting_data_i = self.heap._data[i]  
        starting_data_j = self.heap._data[j]
        self.heap._swap(i, j)
        self.assertEqual(self.heap._data[i], starting_data_j)
        self.assertEqual(self.heap._data[j], starting_data_i)

    def test_min_raises_empty_error(self):
        """Does the public min() method raise an error when the queue is
        empty?"""
        empty_queue = HeapPriorityQueue()
        with self.assertRaises(NameError):
            empty_queue.min()
        # Todo kludge -- Need either a custom exception class to make
        #   EmptyError a real thing, or else do it as ValueError or similar.
        #   As coded in the book's implementation, it raises NameError due to
        #   "Empty" not being defined.

    def test_remove_min(self):
        """Does the public remove_min() method correctly remove and return
        the top element?"""
        initial_top = self.heap.min()
        initial_len = len(self.heap)
        self.heap.remove_min()
        # (5, A) should become the new top.
        expected_top = (5, "A")
        self.assertEqual(expected_top, self.heap.min())
        # Len should have decremented by 1
        self.assertEqual(initial_len - 1, len(self.heap))

    def test_remove_min_raises_empty_error(self):
        """Does remove_min() raise an error when the queue is empty?"""
        empty_queue = HeapPriorityQueue()
        with self.assertRaises(NameError): # Same workaround
            empty_queue.remove_min()

if __name__ == '__main__':
    unittest.main()



