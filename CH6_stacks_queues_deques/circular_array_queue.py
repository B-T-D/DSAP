"""Python implementation of a FIFO queue using a "circular" Python-list array
as underlying storage."""

class ArrayQueue:
    """FIFO queue implementation using a Python list as underlying storage."""

    DEFAULT_CAPACITY = 10 # "moderate" (?) capacity for all new queues (DSAP)

    def __init__(self):
        """Create an empty queue."""
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        """Return the number of elements in the queue."""
        # Runs in amortized O(1) (because of resizes)
        return self._size

    def is_empty(self):
        """Return True if the queue is empty."""
        # Runs in amortized O(1) (because of resizes)
        return self._size == 0

    def first(self):
        """Return (but don't remove) the element at the front of the queue.
        Raise Empty exception if the queue is empty.
        """
        # Runs in O(1)
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._data[self._front]

    def dequeue(self):
        """Remove and return the first element in the queue (FIFO). Raise
        Empty exception if the queue is empty.
        """
        # Runs in amortized O(1) (because of resizes)
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None # help garbage collection
        self._front = (self._front + 1) % len(self._data) # Front-index only changes on dequeue
        self._size -= 1
        if 0 < self._size < len(self._data) // 4: # if array is less than 1/4th
                                                   # full, reduce capacity to 1/2
            self._resize(len(self._data) // 2)
        return answer

    def enqueue(self, e):
        """Add an element to the back of queue."""
        # Runs in amortized O(1) (because of resizes)
        if self._size == len(self._data):
            self._resize(2 * len(self._data)) # double the array size
        avail = (self._front + self._size) % len(self._data) # find the correct
                                            # ...index for the end of the queue
        self._data[avail] = e
        self._size += 1
        # (enqueing a new element doesn't change self._front, whichever element
        #   was already at the head of the queue remains there.

    def _resize(self, cap):
        """Resize to a new list of capacity >= len(self).

        Args:
            cap (int): integer >= len(self)
        """
        old = self._data # store the existing list temporarily
        self._data = [None] * cap # allocate new blank list of the new capacity
        walk = self._front
        for k in range(self._size): # Only consider existing elements for transfer to new list
            self._data[k] = old[walk] # Intentionally shift indices
            walk = (1 + walk) % len(old)
        self._front = 0 # The modular arithmetic elsewhere wouldn't work if
                        #   front isn't reset to 0 (because we take front mod size
                        #   of the array). 

    def __str__(self):
        """String method that returns the string repr of the underlying array, i.e.
        intentionally shows the Nones."""
        return str(self._data)

def walkthrough():
    queue = ArrayQueue()
    initial_elements = ["first in", "second in", "third in"]
    for element in initial_elements:
        queue.enqueue(element)
    print("Circularity in operation:")
    print(f"Right now, queue is \n\t{queue}")
    print("Enqueing a new element 'fourth' requires inserting it immediately after\
'third', can't just put it on the end of the underlying list:")
    queue.enqueue("fourth in")
    print(f"\t{queue}")
    print(f"Filling it up all the way to the end of the initial capacity of 10\
elements:")
    for i in range(4, 10):
        queue.enqueue(str(i+1) + "th in")
    print(f"\t{queue}")
    print(f"\tfront = {queue._front}")
    print(f"Adding an 11th element will not yet require a resize:")
    queue.enqueue("11th in")
    print(f"\t{queue}")
    print(f"\tfront = {queue._front}")
    print(f"\tInstead, 11th goes into the underlying list at self._data[0].\n\t\
Front is still at {queue._front}, so a dequeue call will return 2nd not 11th.")
    print("Adding a 12th will cause a resize to 20")
    queue.enqueue("12th in")
    print(f"\t{queue}")
    print(f"\tfront = {queue._front}")
    print(len(queue._data))
    # dequeue items til it's <= 25% capacity:
    for i in range(8): # dequeue until only 4/20 slots filled
        queue.dequeue()
        print(f"array capacity is now {len(queue._data)}")
    print(f"\t{queue}")
    
def main():
    queue = ArrayQueue()
    initial_elements = ["first in", "second in", "third in"]
    for element in initial_elements:
        queue.enqueue(element)
    assert queue.first() == initial_elements[0]
    queue.dequeue()
    assert queue.first() == initial_elements[1]
    print(f"ArrayQueue simple asserts ok.")
    print(f"-------")
    walkthrough()
    
          

if __name__ == '__main__':
    main()
