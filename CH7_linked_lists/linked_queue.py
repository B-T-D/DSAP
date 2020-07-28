"""Implementing queue ADT with a singly linked list."""

class LinkedQueue:
    """FIFO queue implementation using a singly linked list for storage."""

    class _Node:
        # Same _Node subclass is shared for all of these LL implementations,
        #   because this self-referential _Node is how you use a pointer without
        #   Python directly having pointers in the way that C does.

        __slots__ = '_element', '_next'
                                        
        def __init__(self, element, next):
            """
            Args:
                _next (_Node): another _Node object.
                _element (object): object of whatever type is stored in the LL stack.
            """
            self._element = element # reference to user's element
            self._next = next # reference to next node

    def __init__(self):
        """Create an empty queue."""
        self._head = None
        self._tail = None
        self._size = 0 # number of queue elements

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return (but don't remove) the element at the front of the queue."""
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._head._element # front aligned with head of list

    def dequeue(self):
        """Remove and return the first element of the queue (i.e. FIFO). Raise Empty
        exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty(): # If completion of this dequeue emptied the queue
            self._tail = None # Removed head had been the tail.
        return answer

    def enqueue(self, e):
        """Add an element to the back of the queue."""
        newest = self._Node(e, None) # node will be new tail node bc it's going in at end
        if self.is_empty():
            self._head = newest
        else:
            self._tail._next = newest
        self._tail = newest # update reference to tail node
        self._size += 1

def test():
    """Tests the implementation with simple assert statements."""
    print("Simple-case tests:")
    queue = LinkedQueue()
    assert len(queue) == 0
    assert queue.is_empty() == True
    queue.enqueue("first in")
    assert len(queue) == 1
    print(f"\tlen(): ok")
    assert queue.is_empty() == False
    print(f"\tis_empty(): ok")
    for i in range(2, 101):
        queue.enqueue(f"{i} in")
    assert len(queue) == 100, f"len(queue) = {len(queue)}"
    print(f"\tenqueue(): ok")
    for i in range(100):
        queue.dequeue()
    assert queue.is_empty() == True
    print("\tdequeue(): ok")

if __name__ == '__main__':
    test()
        
