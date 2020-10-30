"""Developed from LC "Design Hashmap".
"""

# Broken--didn't pass one of the actual-submit test cases.
    # Best guess is that problem is something to do with re-linkage of the BST
    # on update. The LC "official" python solution didn't bother using a complex
    # auxiliary DS for the bucket, it just used an array.

# TODO break out the BST Bucket here and use that as minimalist implementation
#   of a BST. It seems to work, at least in my manual on paper testing (but the
#   hash map has some problem), and be less code than DSAP's, apparently at the
#   cost of becoming unbalanced worse and faster (worse even than DSAP baseline
#   TreeMap, not even talking about AVL/splay/red-black).

class MyHashMap:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.prime = 769
        self.bucket_array = [Bucket() for i in range(self.prime)]
    
    def _hash(self, key: int) -> int:
        return key % self.prime

    def put(self, key: int, val: int) -> None:
        """
        value will always be non-negative.
        """
        bucket_index = self._hash(key)
        #print(f"bucket_index for key={key} is {bucket_index}")
        self.bucket_array[bucket_index].insert(key, val)
        #print(len(self.bucket_array[bucket_index]))

    def get(self, key: int) -> int:
        """
        Returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key
        """
        bucket_index = self._hash(key)
        return self.bucket_array[bucket_index].get(key)
        

    def remove(self, key: int) -> None:
        """
        Removes the mapping of the specified value key if this map contains a mapping for the key
        """
        bucket_index = self._hash(key)
        self.bucket_array[bucket_index].delete(key)
        
class Bucket:
    """Should be fully modular and encapsulated, such that the Bucket's underlying
    data type can be changed (e.g. from BSTree to linked list or array) without
    requiring a single character of MyHashMap's code to change.
    """
    
    def __init__(self):
        self.tree = BSTree()
        self.elements = 0
    
    def insert(self, key, val):
        self.tree.root = self.tree.insert(self.tree.root, key, val)
        self.elements += 1
    
    def get(self, key):
        result = self.tree.search(self.tree.root, key)
        if (result is None or result.key != key):
            return -1
        return result.val
    
    def delete(self, key):
        self.tree.root = self.tree.delete(self.tree.root, key)
        self.elements -= 1
    
    def __len__(self):
        return max(self.elements, 0)

class TreeNode:
    
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.parent = None
        self.left = None
        self.right = None

class BSTree:
    
    #
    
    def __init__(self):
        self.root = None
    
    def search(self, root: TreeNode, key: int) -> TreeNode:
        """Search for key in subtree rooted at root, and return the 
            TreeNode with that key if found, else the final position
            searched.
        """
        if root is None or key == root.key:
            return root
        
        if key < root.key:
            return self.search(root.left, key)
        else: # if key > root.key search right 
            return self.search(root.right, key)
    
    def insert(self, root: TreeNode, key: int, val: int) -> TreeNode:
        """Attempt to insert key into BSTree subtree rooted at root and store value at it.
            If the key already exists, update its value.
            Return TreeNode at which key was inserted.
        """
        if not root: # base case: if empty subtree, insert as root and return
            return TreeNode(key, val)
        
        if key > root.key:
            root.right = self.insert(root.right, key, val)
        elif key == root.key:
            root.val = val # update value for same key
        else: # insert into left subtree
            root.left = self.insert(root.left, key, val)
        return root
    
    def successor(self, root: TreeNode) -> TreeNode:
        """Return TreeNode with least key strictly greater than root's key."""
        root = root.right
        while root.left: # keep walking left
            root = root.left
        return root
    
    def predecessor(self, root: TreeNode) -> TreeNode:
        """Return TreeNode with greatest key strictly less than root's key."""
        root = root.left
        while root.right: # keep walking right
            root = root.right
        return root
    
    def delete(self, root: TreeNode, key: int) -> TreeNode:
        """Delete node associated with key from subtree rooted at root, and re-link remaining nodes as needed
            to maintain correct BS tree properties.
        """
        if not root:
            return None
        
        # delete from right subtree
        if key > root.key:
            root.right = self.delete(root.right, key)
        # delete from left subtree
        elif key < root.key:
            root.left = self.delete(root.left, key)
        # base case--delete current node
        else:
            # node is a leaf:
            if not (root.left or root.right):
                root = None
            # node is not leaf and has right child (includes nodes with two children):
            elif root.right:
                root = self.successor(root) # Put the next greatest value where deleted node was
                root.right = self.delete(root.right, root.key)
                # (Greatest key in the tree would never have a right child, by definition. So there will always
                #   be a valid successor to use in this case.)
            # node has a left child only
            else:
                root = self.predecessor(root)
                root.left = self.delete(root.left, root.key)
        
        return root
