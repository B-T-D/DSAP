

array = [1, 2, 3, 4, "x", "x", "initial last"]

array.append(array[-1])
print(array)

for i in range(len(array)- 2, 2, -1):
    array[i] = array[i-1]

print(array)

array = [1, 2, 3, 4, "x", "x", "initial last"]

print(array)
for i in range(len(array) - 1, 2, -1):
    array[i] = array[i-1]
print(array)


print("--------------")

array2 = [1, 2, 3, 4]
# shifting elements [1:] left one position, as you'd do after deletion from the
#   start of the array:

print(f"array2 start:\n\t{array2}")

for i in range(1, len(array2)):
    array2[i-1] = array2[i]
    
# It'll have a copy of the last (rightmost) element, same as shift-right ends up
#   with a copy of the leftmost element of the shifted region.

print(f"array2 after:\n\t{array2}")

print("--------------")

array3 = [1, 2, 3, 4, 999]

print(f"before:\n\t{array3}")

for i in range(len(array3) - 1, 0, -1):
    array3[i] = array3[i-1]

print(f"after:\n\t{array3}")



