from favorites_list import FavoritesList

class FavoritesListMTF(FavoritesList):
    """List of elements ordered with move-to-front heuristic (most recently
    accessed element is at front)."""

    # override _move_up method to provide move-to-front semantics
    def _move_up(self, p):
        """Move accessed item at Position p to front of list."""
        if p != self._data.first():
            self._data.add_first(self._data.delete(p)) # delete / reinsert

        # (The old _move_up insertion-sort reinserted the accessed item at its
        #   new access-count-ordered position).

    # override top because the list isn't pre-sorted now
    def top(self, k):
        """Generate sequence of top k most accessed elements."""
        if not 1 <= k <= len(self):
            raise ValueError('Illegal value for k')

        # Begin by making a copy of the original list:
        temp = PositionalList()
        for item in self._data: # the PositionalList class supports iteration
            temp.add_last(item)

        # Repeatedly find, report, and remove element with the largest count:
        for j in range(k):
            # find and report next highest from temp
            highPos =  temp.first()
            walk = temp.after(highPos)
            while walk is not None:
                if walk.element()._count > highPos.element()._count:
                    highPos = walk
                walk = temp.after(walk)
            # have now found the element with the highest count
            yield highPos.element()._value # report element to user
            temp.delete(highPos) # remove from temp list
