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
        """Search for element e and return its Position (or None if not found)."""
        walk = self._data.first()
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
        """Access element e, thereby increasing its access count."""
        p = self._find_position(e) # try to locate existing element
        if p is None:
            p = self._data.add_last(self._Item(e)) # if new, place at end
        p.element()._count += 1 # always increment count
        self._move_up(p) # Move element forward if needed

    def access(s
                    
        
