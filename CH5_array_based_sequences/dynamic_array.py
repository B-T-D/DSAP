import ctypes

class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""
    
    def __init__(self):
        """Initialize empty array."""
        self._n = 0 # count actual elements
        self._capacity = 1 # default array capacity (number of elements)
        self._A = self._make_array(self._capacity) # low-level array
       
    def __len__(self):
        """Return number of elements stored in the array."""
        return self._n
    
    def __str__(self):
        string = ''
        for i in range(self._n):
            string += str(self._A[i]) + ', '
        return '[' + string.rstrip(', ') + ']' 
    
    def __getitem__(self, k):
        """Return element at index k."""
        if not 0 <= k < self._n: # If k isn't between 0 and the size of the array
            raise IndexError('invalid index')
        return self._A[k]
    
    def append(self, obj):
        """Add object to end of the array."""
        if self._n == self._capacity: # If current array has run out of capacity
            self._resize(2 * self._capacity) # Double the capacity
        self._A[self._n] = obj
        self._n += 1
    
    def _resize(self, c): # private method that calls the cytpes wrapper method to implement the resize
        B = self._make_array(c) # create a separate, new array of capacity callable
        for k in range(self._n):
            B[k] = self._A[k] # Copy each existing value into the new list at the same index
        self._A = B # Reassign the original array name to be the new bigger array. Original self._A array is now dark in memory with no callable name assigned to that data--garbage.
        self._capacity = c
    
    def _make_array(self, c): # private wrapper method that calls the ctypes function that actually allocates the memory
        """Return new array with capacity of c objects."""
        return (c * ctypes.py_object)() # C (or CPython) has a "PyObject *" datatype--pointer to a PyObject.

def main():
    my_dynarr = DynamicArray()
    print(my_dynarr)
    my_dynarr.append(1)
    print(my_dynarr)
    print(str(my_dynarr))
    for i in range(10):
        my_dynarr.append(i)
    print(my_dynarr)
    
if __name__ == "__main__":
    main()
    