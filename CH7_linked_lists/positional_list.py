from doubly_linked_base import _DoublyLinkedBase

class PositionalList(_DoublyLinkedBase):
    """A sequential container of elements allowing positional access."""

    # NB PositionalList doesn't have its own init method.

    #----------------nested Position class----------------------------------
    class Position:
        """Abstraction representing the location of a sincle element."""
        # Presumably it's all just C pointers under the hood, same as with the
        #   _DLB class's _Node object.

        # DSAP doesn't make this non-public like _Node, even though it's nested

        def __init__(self, container, node):
            """Constructor shouldn't be invoked by the user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element # Returning basically ' *node_pointer'.
                                        # The data in memory that the pointer
                                        #   points to.

        def __eq__(self, other):
            """
            Overloading the '==' operator.

            Return True if other is a Position representing the same location.

            Args:
                other (Position): A Position object. 
            """
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            """Overloading the '!=' operator.

            Return True if other does not represent the same location.
            """
            return not (self == other) # opposite of __eq__

    # ----------------utility method--validate node----------------------------
    def _validate(self, p):
        """Return position's node, or raise appropriate error if invalid.
        """
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self: # if it's a position from some other instance of a DS that uses Positions
            raise ValueError('p does not belong to this container')
        if p._node._next is None:
            raise ValueError('p is no longer valid') # if the node was already deprecated
        return p._node

    # -----------------utility method--make position-----------------------\
    def _make_position(self, node):
        """Return Position instance for given node (or None if sentinel.)"""
        if node is self._header or node is self._trailer:
            return None # boundary violation
        else:
            return self.Position(self, node) # Create a new position instance

    # -----------------accessors ------------------------------------------
    def first(self):
        """
        Return the first Position in the list (or None if list is empty).
        """
        return self._make_position(self._header._next)

    def last(self):
        """Return the last Position in the list (or None if empty)."""
        return self._make_position(self._trailer._prev)

    def before(self, p):
        """Return the Position just before Position p (or None if p is
        first)."""
        node = self._validate(p)
        return self._make_position(node._prev)

    def after(self, p):
        """Return the Position just after Position p (or NOne if p is last).
        """
        node = self._validate(p)
        return self._make_position(node._next)

    def __iter__(self):
        """Generate a forward iteration of the elements in the list."""
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            # trailer sentinel's element is assigned None in _DLB's init
            # method, so cursor.element() will return None upon reaching
            # end of the list.
            cursor = self.after(cursor)

    #------------------------- mutators ------------------------------------
    # override inherited version to return Position, rather than Node:
    def _insert_between(self, e, predecessor, successor):
        """Add element between existing nodes and return new Position."""
        node = super()._insert_between(e, predecessor, successor)
        return self._make_position(node)

    def add_first(self, e):
        """Insert element e at the front of the list and return new Position."""
        return self._insert_between(e, self._header, self._header._next)

    def add_last(self, e):
        """Insert element e at the back of the list and return new Position."""
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def add_before(self, p, e):
        """Insert element e into list before Position p and return new Position.
        """
        original = self._validate(p)
        return self._insert_between(e, original._prev, original)

    def add_after(self, p, e):
        """Insert element e into list after Position p and return new Position."""
        original = self._validate(p)
        return self._insert_between(e, original, original._next)

    def delete(self, p):
        """Remove and return the element at Position p."""
        original = self._validate(p)
        return self._delete_node(original) # inherited method returns element

    def replace(self, p, e):
        """Replace the element at Position p with e. Return the element formerly
        at Position p."""
        # Don't have to change anything besides the pointed-to data. The prev and
        #   next linkages were already in place for the original node, and aren't
        #   changed by anything we're doing here.
        original = self._validate(p)
        old_value = original._element # temporarily store old element
        original._element = e # replace with the new data element
        return old_value

def test():
    # _DLB has its own builtin mini unit tests so don't need to test that here
    #   e.g. len(), is_empty().
    PL = PositionalList()
    assert PL.first() == None
    assert PL.last() == None
    PL.add_first("from add first")
    assert PL.first().element() == "from add first", f"actual: {PL.first().element()}"
    expected = "from add last"
    PL.add_last(expected)
    actual = PL.last().element()
    assert actual == expected, f"Actual: {actual}; Expected: {expected}"
    
    expected = "from add before"
    PL.add_before(PL.last(), expected)
    PL.delete(PL.last())
    actual = PL.last().element() # Element added by add_before() should be the last now.
    assert actual == expected, f"Actual: {actual}; Expected: {expected}"

    expected = "from replace"
    PL.replace(PL.last(), expected)
    actual = PL.last().element()
    assert actual == expected, f"Actual: {actual}; Expected: {expected}"

    for i in range(10):
        PL.add_last(str(i))
    assert len(PL) == 12
    print("Simple asserts ok")
    # Testing the __iter__ method:
    for position in PL: # the __iter__ method handles the .element() call, that's why you would print
                        #   just position not position.element(). 
        print(position)
    print("manual print test ok")
    

if __name__ == '__main__':
    test()
        
        
        
