# Tests with unittest

from positional_list import PositionalList

class FavoritesList:
    """List of elements ordered from most frequently accessed to least."""

    # ------------------- nested _Item class --------------------------------
    class _Item:
        __slots__ = '_value', '_count' # make the object lighter-weight in memory

        def __init__(self, e):
            self._value = e # the user's element
            self._count = 0 # access count initially zero

    # -------------------- nonpublic utilities --------------------------------
    def _find_position(self, e):
        """Search for element e and return its Position (or None if not found).

        Returns:
            walk (Position): Position object.
        """
        walk = self._data.first() # a Position object
        while walk is not None and walk.element()._value != e:
            walk = self._data.after(walk)
        return walk

    def _move_up(self, p):
        """Move item at Position p earlier in the list based on access count."""
        if p != self._data.first(): # If it's not first, consider moving it...
            cnt = p.element()._count
            walk = self._data.before(p)
            if cnt > walk.element()._count: # must shift p forward (it's more
                                             # frequently accessed)
                while (walk != self._data.first() and # Walk leftward til reach front of list...
                       cnt > self._data.before(walk).element()._count): #...or an element that sorts
                                                                        # to a higher position than the element that's being sorted
                    walk = self._data.before(walk) # Walk one step left
                self._data.add_before(walk, self._data.delete(p)) # delete/reinsert

    # ------------------------- public methods -------------------------------
    def __init__(self):
        """Create empty list of favorites."""
        self._data = PositionalList() # will be list of _Item instances

    def __len__(self):
        """Return number of entries on favorites list."""
        return len(self._data)

    def is_empty(self):
        """Return True if list is empty."""
        return len(self._data) == 0
        # Presumably, this can't (or shouldn't) just use _DLB's
        #   inherited-inherited is_empty method because that entire class
        #   is meant to be nonpublic.

    def access(self, e):
        """
        Access element e, thereby increasing its access count.

        e (object): The actual stored item--the _value attribute of the _Item object.
                    Not the _Item object itself (that's not to be accessed from outside the
                    class) and not the Position object. Need not be the identical
                    object in memory; e.g. separate string or int object with same
                    value will be accessed successfully. 
        """
        p = self._find_position(e) # try to locate existing element
        if p is None:
            p = self._data.add_last(self._Item(e)) # if new, place at end
        p.element()._count += 1 # always increment count
        self._move_up(p) # Move element forward if needed

    def remove(self, e):
        """Remove element e from the list of favorites."""
        p = self._find_position(e) # try to locate existing element
        if p is not None:
            self._data.delete(p) # delete, if found

    def top(self, k):
        """Generate sequence of top k elements in terms of access count.
        Yields an iterator that can be used in a for loop; doesn't return
        anything. 

        Args:
            k (int): Number of elements to include in the list. Must be a
                positive nonzero integer no greater than the length of the list.

        Returns:
            None
        """
        if not 1 <= k <= len(self):
            raise ValueError('Illegal value for k')
        walk = self._data.first()
        for j in range(k):
            item = walk.element() # element of list is _Item
            yield item._value # report user's element
            walk = self._data.after(walk)

        
                    
        
