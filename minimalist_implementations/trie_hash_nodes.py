# My solution to LC 147. Took approach of having a hash table at each node 
#   rather than an array. Main solution used array (also was Java).
#   Mine here seemed to perform acceptably but not notably well. It was 
#   slightly worse than other python ones on both time and space, but 
#   not badly enough to suggest a major asymptotic complexity messup. 

# Might be able to hackily optimize the search method's running time by 
#   storing a separate hash set as an instance variable of Trie. I.e. 
#   just store a set of the words in the trie (add them as part of the 
#   insert method), then use that table as the search function. 
#   But seems more useful to illustrate a tree-traversal search (although startswith would still need that). 

class Trie:
    
    class TrieNode:
        
        def __init__(self, val: str):
            self.val = val
            self.children = {}
            self.is_word = False # Flag to indicate if this node terminates a string
            

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = self.TrieNode(val='')
        

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        node = self.root
        stroot = self.root # current subtree root
        i = 0
        while i < len(word):
            if word[i] in stroot.children:
                node = node.children[word[i]]
            else:
                node = self.TrieNode(val=word[i])
                stroot.children[word[i]] = node
            stroot = node
            i += 1
        node.is_word = True
        return
        

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return False
        if node.is_word:
            return True
        return False
        

    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        node = self.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return False
        return True
        