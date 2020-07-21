"""Empirical demonstration that Python builtin list class resizes using a
"dynamic array" strategy of replacing the entire old array with a new, larger
array.

Prints the array's bytes size for different numbers of elements, showing Python
allocating more memory in steps, filling that up, then stepping up again.
"""


import sys
data = []
n = 27
for k in range(n):
    a = len(data)
    b = sys.getsizeof(data)
    print('Length: {0:3d}; Size in bytes: {1:4d}'.format(a, b))
    data.append(None) # add another None element to the data

# test idle issue
# test
