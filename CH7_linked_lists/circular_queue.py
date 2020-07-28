class CircularQueue:
    """Circular queue implementation using circularly linked list for
    storage."""

    class _Node: # Same object as prior python LL implementations
        
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
        self._tail = None # don't need to store head as an instance variable--can
                            #   always access it in O(1) by accessing tail's next
        self._size = 0

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self):
        """Return  True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return (but don't remove) the element at the front of the queue.
        Raise Empty exception if queue is empty."""
        if self.is_empty():
            raise Empty('Queue is empty')
        head = self._tail._next
        return head._element

    def dequeue(self):
        """Remove and return the first element of the queue (FIFO). Raise
        Empty exception if the queue is empty."""
        if self.is_empty():
            raise Empty('Queue is empty')
        oldhead = self._tail._next
        if self._size == 1: # special case where removing the sole element leaves queue empty
            self._tail = None
        else:
            self._tail._next = oldhead._next # bypass the old head
        self._size -= 1
        return oldhead._element

    def enqueue(self, e):
        """Add an element to the back of the queue."""
        newest = self._Node(e, None) # new node will become the tail node
        if self.is_empty():
            newest._next = newest # initialize circularly if this is the inaugural
                                # element
        else:
            newest._next = self._tail._next # new node points to head
            self._tail._next = newest # old tail points to new node
        self._tail = newest # new node becomes the tail
        self._size += 1

    def rotate(self):
        """Rotate front element to the back of the queue."""
        if self._size > 0:
            self._tail = self._tail._next # old head becomes new tail

def test():
    """Simple assert tests for the ADT implementation."""
    print("Simple-case tests:")
    cq = CircularQueue()
    assert len(cq) == 0
    assert cq.is_empty() == True
    cq.enqueue("1 in")
    assert len(cq) == 1
    assert cq.is_empty() == False
    assert cq.first() == "1 in"
    cq.dequeue() # Test the special case of dequeing the sole remaining element
    assert len(cq) == 0
    for i in range(100):
        cq.enqueue(i)
    assert cq.first() == 0
    cq.rotate()
    assert cq.first() == 1, f"cq.first() = {cq.first()}"

if __name__ == '__main__':
    test()
    

    
