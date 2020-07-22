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
    
    
    
    def bad__str__(self): # this is a dumb (memory inefficient) way to return the string.
        """A bad way to return the string representation of this data structure."""
        string = '' # start with an empty list, not an empty string. A list is an array of pointers to the primary values, 
                    # a string is a "literal" C array of the primary values themselves.
        for i in range(self._n): # You create one excess copy string of size n_current for every element in the array...
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
    
    def insert(self, k, value):
        """(DSAP 204 addition)
        #Insert value at index k, shifting subsequent values rightward.
        """
        # Assumes 0 <= k <= n, for simplicity
        if self._n == self._capacity: # if not enough room...
            self._resize(2 * self._capacity) #...resize to 2*current_capacity
        for j in range(self._n, k, -1): # First shift the rightmost, hence step of -1 back from end of the list data[self._n] (i.e. nothing after it to its right to worry about)
            self._A[j] = self._A[j-1] # it's relying on some builtin inherited __setitem__ method not defined in this class.
        self._A[k] = value # store newest element at keys
        self._n += 1 # length of the list has increased by 1, so update the instance variable self._n
    
    def remove(self, value):
        """Remove the first occurrence of value (or else rase ValueError)."""
        # DSAP's version doesn't consider the steps added by shrinking the dynamic array.
        for k in range(self._n): # iterate over every value in the sequence
            if self._A[k] == value: # if there's match
                for j in range(k, self._n - 1): # shift all subsequent elements rightward to fill the gap
                    self._A[j] = self._A[j+1]
                self._A[self._n - 1] = None # Manually helps / accelerates the garbage collection.
                self._n -= 1 # decerement instance variable that stores the length of the array
                return
        raise ValueError('value not found') # only reached if no match
                
    
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
    my_dynarr.insert(5, 77777)
    print(my_dynarr)
    my_dynarr.remove(77777)
    print(f"after remove call:")
    print(my_dynarr)
    print(f"remove call on nonexistent value:")
    try:
        printf("\n\t{my_dynarr.remove(4444)}")
    except:
        print("\tRaised error")
    
    print("---------")
    new = DynamicArray()
    for i in range(3):
        new.append(i)
    print(f"new dynarr after adds:\n\t{new}")
    
    t = 1
    new.remove(t)
    print(f"new after calling remove on {t}:\n\t{new}")
    
if __name__ == "__main__":
    main()
    