"""Implementing a stack using a singly linked list."""

class LinkedStack:
    """LIFO stack implementation using a singly linked list for storage."""
    
    #-------------------------- Nested _Node class ------------------
    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node."""

        # In a "real" implementation using C, _next would be a pointer to
        #   another instance of the same struct. A node struct. The role of this
        #   nonpublic class would instead be played by:

            # struct node
            # {
            #       int data;
            #       struct node * next;
            # };

        # The answer to "where's the pointer when you do a LL in python" is that
        #   this _Node helper object is basically a wrapper for the pointer.
        #   under the hood, the _Node's self._next (whose type is itself _Node)
        #   is the literal memory-address pointer to the next element. 

        __slots__ = '_element', '_next' # Streamline memory usage by declaring
                                        #   __slots__ so that python won't use a
                                        #   heavyweight dictionary object for the
                                        #   local namespace.
                                        
        def __init__(self, element, next): # initialize node's fields
            """
            Args:
                _next (_Node): another _Node object.
                _element (object): object of whatever type is stored in the LL stack.
            """
            self._element = element # reference to user's element
            self._next = next # reference to next node
    #-------------------------------------------------------------------

    def __init__(self):
        """Initialize an empty stack."""
        self._head = None # reference to the head node
        self._size = 0 # number of stack elements

    def __len__(self):
        """Return the number of elements in the stack."""
        return self._size

    def is_empty(self):
        """Return True if the stack is empty."""
        return self._size == 0

    def push(self, e):
        """Implement stack ADT's push method by adding element e to the head of the
        linked list."""
        self._head = self._Node(e, self._head) # create and link a new node
        self._size += 1

    def top(self):
        """Implement stack ADT's "top()" accessor method by returning the element
        at the head of the LL.
        
        Return (but don't remove) the element at the top of the stack. Raise Empty
        exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._head._element  # top of stack is head of the LL

    def pop(self):
        """Implement stack ADT's pop method by deleting the element at the head of
        the LL.

        Remove and return the element from the top of the stack (i.e. LIFO). Raise
        Empty exception if stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty')
        answer = self._head._element
        self._head = self._head._next # Set the former 'second' node to be the new head
        self._size -= 1 # decrement the instance variable that stores the len
        return answer

def test_is_empty():
    stack = LinkedStack()
    assert stack.is_empty() == True
    stack.push('something')
    assert stack.is_empty() == False
    print(f"is_empty() simple asserts ok")

def test_len():
    stack = LinkedStack()
    assert len(stack) == 0
    stack.push(1)
    assert len(stack) == 1
    for i in range(99):
        stack.push(i)
    assert len(stack) == 100
    print(f"__len__() simple asserts ok")

def test_push():
    # skipping, if is empty and len pass then push basics are fine
    pass

def test_top():
    stack = LinkedStack()
    stack.push(1)
    assert stack.top() == 1
    
    stack.push(2)
    assert stack.top() == 2
    stack.pop()
    assert stack.top() == 1
    print(f"top() simple asserts ok")

def test_pop():
    # covered by test_top()
    pass


def main():
    print(f"-----")
    print("When you manually declare __slots__ for a class, __slots__ is a tuple:")
    test = LinkedStack._Node(1, 2)
    print(test.__slots__)
    print(type(test.__slots__))
    print(f"------")
    test_is_empty()
    test_len()
    test_push()
    test_top()
    test_pop()

if __name__ == '__main__':
    main()
