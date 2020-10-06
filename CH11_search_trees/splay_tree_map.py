from tree_map import TreeMap

class SplayTreeMap(TreeMap):
    """Sorted map implementation using a splay tree."""
    # "zig" and "zag" terminology from p. 490 et seq
    
    # Given node x of binary search tree T:
        # x: the node to be splayed. Position "p" in splay method signature. 
        # y: parent of x
        # z: parent of y, grandparent of x
        
        # zig case: x has no grandparent.
        # zig-zag case: one of x and y is a left child and other is right.
        # zig-zig case: x and y are both left children or both right children.
    
    #### Splay operation
    def _splay(self, p):
        while p != self.root():
            parent = self.parent(p)
            grand = self.parent(parent)
            if grand is None:
                # zig case (no grandparent)
                self._rotate(p)
            elif (parent == self.left(grand)) == (p == self.left(parent)):
                # zig-zig case
                self._rotate(parent) # move parent up
                self._rotate(p) # then move p up
            else:
                # zig-zag case
                self._rotate(p) # move p up 
                self._rotate(p) # move p up again
                        
    #### Override balancing hook methods inherited from TreeMap
    def _rebalance_insert(self, p):
        self._splay(p) # if it was inserted under, splay it.

    def _rebalance_delete(self, p):
        # This will be called by TreeMap.delete() with parent of the deleted
        #   node (or its replacement) as Position p. 
        if p is not None:
            self._splay(p) # Splay the surviving parent to the top

    def _rebalance_access(self, p):
        self._splay(p)
