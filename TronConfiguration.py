"""
author: Dade Wood, daw1882
filename: TronConfiguration.py
description: This file contains the code for a board configuration of the
Tron game. This will be used in the backtracking to store the board state and
find game solutions. Testing of this is found below for making simple moves
as a rook would for a piece.
"""

from enum import Enum


class Outcome(Enum):
    LEFT = 1
    RIGHT = 2
    PREVIOUS = 3
    NEXT = 4
    UNKNOWN = 5


class TronBike:
    def __init__(self, row, col, player):
        self.row = row
        self.col = col
        self.player = player


class TronConfiguration:
    def __init__(self, num_rows, num_cols, left_bikes, right_bikes):
        self.board = []
        self.nrows = num_rows
        self.ncols = num_cols
        self.left_bikes = left_bikes
        self.right_bikes = right_bikes
        self.outcome = Outcome.UNKNOWN
        self.init_board()

    # def __init__(self, board, num_rows, num_cols, left_bikes, right_bikes):
    #     self.board = board
    #     self.nrows = num_rows
    #     self.ncols = num_cols
    #     self.left_bikes = left_bikes
    #     self.right_bikes = right_bikes
    #     self.outcome = Outcome.UNKNOWN

    def init_board(self):
        self.board = [[1 for i in range(self.ncols)] for j in range(self.nrows)]
        for bike in self.left_bikes:
            self.board[bike.row][bike.col] = bike.player
        for bike in self.right_bikes:
            self.board[bike.row][bike.col] = bike.player

    def get_child(self, bike, new_row, new_col):
        if new_row <= bike.row and new_col <= bike.col:
            for i in range(new_row, bike.row+1):
                for j in range(new_col, bike.col+1):
                    self.board[i][j] = 0
        elif new_row <= bike.row and not new_col <= bike.col:
            for i in range(new_row, bike.row+1):
                for j in range(bike.col, new_col+1):
                    #print(i, " ", j)
                    self.board[i][j] = 0
        elif not new_row <= bike.row and new_col <= bike.col:
            for i in range(bike.row, new_row+1):
                for j in range(new_col, bike.col+1):
                    self.board[i][j] = 0
        else:
            for i in range(bike.row, new_row+1):
                for j in range(bike.col, new_col+1):
                    self.board[i][j] = 0
        self.board[new_row][new_col] = bike.player
        bike.row = new_row
        bike.col = new_col

    def to_str(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.board[i][j] == 0:
                    print("X", end=" ")
                if self.board[i][j] == 1:
                    print("+", end=" ")
                if self.board[i][j] == 2:
                    print("L", end=" ")
                if self.board[i][j] == 3:
                    print("R", end=" ")
            print()


if __name__ == "__main__":
    # Testing initial configuration and some movement
    left_bikes = [TronBike(0,2,2)]
    right_bikes = [TronBike(2,0,3)]
    test = TronConfiguration(3, 3, left_bikes, right_bikes)
    test.to_str()
    print("-------------")
    test.get_child(left_bikes[0], 0, 0)
    test.to_str()
    print("-------------")
    test.get_child(left_bikes[0], 1, 0)
    test.to_str()
    print("-------------")
    test.get_child(left_bikes[0], 1, 2)
    test.to_str()
