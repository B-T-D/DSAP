import sys, os

this_directory = os.path.dirname(__file__)
ch8_directory = '../CH8_trees' # for LinkedBinaryTree
ch10_directory = '../CH10_maps_hash_tables' # for MapBase
sys.path.insert(0, os.path.abspath(ch8_directory))
sys.path.insert(1, os.path.abspath(ch10_directory))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

print("CH11 init.py ran")
print(os.path.abspath(ch10_directory))

