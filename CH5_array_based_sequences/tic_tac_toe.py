class TicTacToe:
    """Management of a Tic Tac Toe game (doesn't have a computer-player that
    does strategy against a human player)."""

    def __init__(self):
        """Start a new game."""
        self._board = [[' '] * 3 for j in range(3)] # 3 x 3 2D array of space character strings
        self._player = 'X' # X moves first

    def mark(self, i, j):
        """Put an X or O mark at position (i, j) for next player's turn."""
        if not (0 <= i <= 2 and 0 <= j <= 2):
            raise ValueError('Invalid board position')
        if self._board[i][j] != ' ': # if there's already a mark at that square
            raise ValueError('Board position occupied')
        if self.winner() is not None:
            raise ValueError('Game is already complete')
        self._board[i][j] = self._player
        if self._player == 'X': # swap the active player
            self._player = 'O'
        else:
            self._player = 'X'

    def _is_win(self, mark):
        """Check whether current board configuration is a win for the given
        player

        Args:
            mark (str): 'X' or 'O'
        """

        board = self._board # local variable for code compactness here
        # (authors are manually checking all 8 of the possible ways you could
        #   get three in a row--2 diagonals + 3 full-row + 3 full-column = 8.
        return (mark == board[0][0] == board[0][1] == board[0][2] or    # row 0
                mark == board[1][0] == board[1][1] == board[1][2] or    # row 1
                mark == board[2][0] == board[2][1] == board[2][2] or    # row 2
                mark == board[0][0] == board[1][0] == board[2][0] or    # column 0
                mark == board[0][1] == board[1][1] == board[2][1] or    # column 1
                mark == board[0][2] == board[1][2] == board[2][2] or    # column 2
                mark == board[0][0] == board[1][1] == board[2][2] or    # diagonal
                mark == board[0][2] == board[1][1] == board[2][0])      # rev diag

    def winner(self):
        """Return mark of winning player, or None to indicate a tie."""
        for mark in 'XO':
            if self._is_win(mark):
                return mark
        return None

    def __str__(self):
        """Return string representation of the board in its current state."""
        rows = ['|'.join(self._board[r]) for r in range(3)]
        return '\n-----\n'.join(rows)

def main():
    board = TicTacToe()
    refresh_board(board)
    board.mark(1, 1)
    refresh_board(board)
    board.mark(0, 0)
    refresh_board(board)
    board.mark(2, 2)
    refresh_board(board)
    board.mark(0, 1)
    refresh_board(board)
    board.mark(0, 2)
    refresh_board(board)
    board.mark(1, 2)
    refresh_board(board)
    board.mark(2, 0)
    refresh_board(board)

def refresh_board(board):
    """
    Args:
        board (TicTacToe object): pass
    """
    print(board)
    print(f"winner: {board.winner()}")
    print("******MOVE******")
    

if __name__ == '__main__':
    main()
        
