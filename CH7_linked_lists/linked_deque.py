from doubly_linked_base import _DoublyLinkedBase

class LinkedDeque(_DoublyLinkedBase):
    """Double-ended queue implementation based on a doubly linked list."""

    def first(self):
        """Return (but don't remove) the element at the front of the deque."""
        if self.is_empty():
            raise Empty("Deque is empty")
        return self._header._next._element # real item just after header (the
                                            # literal first is sentinel)

    def last(self):
        """Return (but don't remove) the element at the back of the deque."""
        if self.is_empty():
            raise Empty("Deque is empty")
        return self._trailer._prev._element # real item just before trailer

    def insert_first(self, e):
        """Add an element to the front of the deque."""
        self._insert_between(e, self._header, self._header._next) # after header

    def insert_last(self, e):
        """Add an element to the back of the deque."""
        self._insert_between(e, self._trailer._prev, self._trailer) # before trailer

    def delete_first(self):
        """Remove and return the element from the front of the deque."""
        if self.is_empty():
            raise Empty("Deque is empty")
        return self._delete_node(self._header._next) # use inherited method

    def delete_last(self):
        """Remove and return the element from the back of the deque."""
        if self.is_empty():
            raise Empty("Deque is empty")
        return self._delete_node(self._trailer._prev) # use inherited method

def test():
    LD = LinkedDeque()
    assert len(LD) == 0
    assert LD.is_empty() == True
    LD.insert_first("first insertion")
    assert len(LD) == 1
    assert LD.is_empty() == False
    assert LD.first() == "first insertion"
    LD.insert_last("second insertion")
    LD.insert_last("third insertion")
    assert LD.last() == "third insertion"
    LD.delete_last()
    assert LD.last() == "second insertion"
    assert len(LD) == 2
    LD.delete_last()
    LD.delete_last()
    assert len(LD) == 0
    assert LD.is_empty() == True
    print("Simple asserts ok")


if __name__ == '__main__':
    test()
        

    
