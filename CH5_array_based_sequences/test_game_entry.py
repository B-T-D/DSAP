import unittest
import random

import game_entry as ge

letters = "abcdefghijklmnopqrstuvwxyz"

class TestStr(unittest.TestCase):
    """Test the __str__ method."""

    def test_simple_string(self):
        entry = ge.GameEntry("Brian", 98)
        string = str(entry)
        self.assertEqual(string, "(Brian, 98)")

class TestScoreboard(unittest.TestCase):
    """Simple tests for the Scoreboard class."""

    def setUp(self):
        random.seed(1)
        self.myboard = ge.Scoreboard()
        # add initial entries
        for i in range(0, 19, 2):
            self.myboard.add(ge.GameEntry(
                random.choice([(3 * chr(n)) for n in range(ord("a"), ord("z"))]),
                i))
        print(self.myboard)
        print("test")

    def test_init(self):
        """Does constructor return a board with 10 None entries when no capacity
        argument is provided?"""
        newboard = ge.Scoreboard()
        self.assertEqual(newboard._board, [None] * 10) # internal ._board attribute
            # is the allocated number of slots, object._n (or __len__ if it had one)
            # would return zero because it only counts non-None entries. 

    def test_str(self):
        pass

    def test_add(self):

        # Add should allow in a new high score that's higher than 18
        new_high_score = 19
        self.myboard.add(ge.GameEntry("player1", new_high_score))
        self.assertEqual (self.myboard[0].get_score(), new_high_score)
        print(self.myboard)

        # Add() should reject a high score lower than the now lowest high, 2
        new_attempt = 1
        self.myboard.add(ge.GameEntry("player2", new_attempt))
        for i in range(10):
            self.assertNotEqual(new_attempt, self.myboard[i].get_score())

if __name__ == '__main__':
    unittest.main()
