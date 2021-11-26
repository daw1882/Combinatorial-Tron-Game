from TronConfiguration import TronBike, TronConfiguration, Outcome
import copy
import time


def init_board():
    board_size = input("Enter in the board size (m n): ").split(" ")

    num_left = int(input("How many Left bikes do you want? "))
    left_bikes = []
    for i in range(num_left):
        bike_info = input(f"Bike {i+1} location (r c): ").split(" ")
        left_bikes.append(TronBike(int(bike_info[0]), int(bike_info[1]), 2))

    num_right = int(input("How many Right bikes do you want? "))
    right_bikes = []
    for i in range(num_right):
        bike_info = input(f"Bike {i+1} location (r c): ").split(" ")
        right_bikes.append(TronBike(int(bike_info[0]), int(bike_info[1]), 3))

    board = TronConfiguration(int(board_size[0]), int(board_size[1]),
                              left_bikes, right_bikes)
    return board


"""
Notes:
- will need to do game tree outcome classes to get outcome class of initial 
position, not just find if one of them can win (one person could use the 
nonoptimal strategy in the backtracking)
- backtrack to an end position or to a pruning condition to assign an outcome 
class to a position, as you go back up in depth then continue assigning 
outcome classes recursively)
- ending position is one person can't move at all (if neither can move then 
whoever is going next loses - P position)
"""


def find_outcome(position):
    """
    Find the outcome class for a board by simulating every possibility in the
    game. This should work by:
        1) get all children for board
        2) Base cases -
            if left_children is empty but right_children is not,
        right wins and vice versa. However, if both left and right children
        are empty, the outcome class is P.
            if all of left_children are R or N and all of right children are
        L or N, then outcome class is P.
            if all of left_children are R or N and some of right children are R
        or P (at least just one), then outcome class is R
            if all of right_children are L or N and some of left children are L
        or P (at least just one), then outcome class is L
            else if some of left_children are L or P and some of
        right_children are R or P, then outcome class is N
        3) Otherwise, when not at a base case (Outcome still unknown for at
        least one of the children) then recurse on that unknown board.
        4) As recursion ends, should follow stack all the way back until
        outcome class of original board is found.
    :param position: The board state to find the outcome class for.
    :return: An Outcome class type
    """
    left, right = get_children(position)
    some_LP = False
    some_RP = False

    # Initial base cases
    if len(left) == 0 and len(right) == 0:
        position.outcome = Outcome.PREVIOUS
        return Outcome.PREVIOUS
    if len(left) == 0 and not len(right) == 0:
        position.outcome = Outcome.RIGHT
        return Outcome.RIGHT
    if not len(left) == 0 and len(right) == 0:
        position.outcome = Outcome.LEFT
        return Outcome.LEFT

    # Find unknown outcome classes or prune branch if possible
    for child in left:
        if child.outcome == Outcome.UNKNOWN:
            find_outcome(child)
        if child.outcome == Outcome.LEFT or child.outcome == Outcome.PREVIOUS:
            some_LP = True
            break
    for child in right:
        if child.outcome == Outcome.UNKNOWN:
            find_outcome(child)
        if child.outcome == Outcome.RIGHT or child.outcome == Outcome.PREVIOUS:
            some_RP = True
            break

    # Last base cases based on what was found for child outcome classes
    if some_LP and some_RP:
        position.outcome = Outcome.NEXT
        return Outcome.NEXT
    elif not some_LP and some_RP:
        position.outcome = Outcome.RIGHT
        return Outcome.RIGHT
    elif some_LP and not some_RP:
        position.outcome = Outcome.LEFT
        return Outcome.LEFT
    else:
        position.outcome = Outcome.PREVIOUS
        return Outcome.PREVIOUS


def get_children(position):
    """
    This will get all the possible board states following a valid move by
    either player from the initial board.
    :param position: The board to get the children for
    :return: left_children, A list of all boards created after every valid
             left move.
             right_children, A list of all boards created after every valid
             right move.
    """
    left_children = []
    right_children = []

    for i in range(len(position.left_bikes)):
        # check east
        curr_col = position.left_bikes[i].col
        curr_row = position.left_bikes[i].row
        new_pos = copy.deepcopy(position)
        while curr_col+1 < position.ncols and position.board[curr_row][
            curr_col+1] == 1:
            bike = new_pos.left_bikes[i]
            new_pos.get_child(bike, bike.row, bike.col+1)
            left_children.append(new_pos)
            new_pos = copy.deepcopy(new_pos)
            curr_col += 1

        # check west
        curr_col = position.left_bikes[i].col
        new_pos = copy.deepcopy(position)
        while curr_col-1 >= 0 and position.board[curr_row][
            curr_col-1] == 1:
            bike = new_pos.left_bikes[i]
            new_pos.get_child(bike, bike.row, bike.col-1)
            left_children.append(new_pos)
            new_pos = copy.deepcopy(new_pos)
            curr_col -= 1

        # check north
        curr_col = position.left_bikes[i].col
        curr_row = position.left_bikes[i].row
        new_pos = copy.deepcopy(position)
        while curr_row-1 >= 0 and position.board[curr_row-1][
            curr_col] == 1:
            bike = new_pos.left_bikes[i]
            new_pos.get_child(bike, bike.row-1, bike.col)
            left_children.append(new_pos)
            new_pos = copy.deepcopy(new_pos)
            curr_row -= 1

        # check south
        curr_row = position.left_bikes[i].row
        new_pos = copy.deepcopy(position)
        while curr_row+1 < position.nrows and position.board[curr_row+1][
            curr_col] == 1:
            #print(new_pos.board[curr_row+1][curr_col], "", curr_row+1, "",
            #      curr_col)
            #print(position.nrows)
            bike = new_pos.left_bikes[i]
            new_pos.get_child(bike, bike.row+1, bike.col)
            left_children.append(new_pos)
            new_pos = copy.deepcopy(new_pos)
            curr_row += 1
        #print(left_children)

    for i in range(len(position.right_bikes)):
        # check east
        curr_col = position.right_bikes[i].col
        curr_row = position.right_bikes[i].row
        new_pos = copy.deepcopy(position)
        while curr_col+1 < position.ncols and position.board[curr_row][
            curr_col+1] == 1:
            bike = new_pos.right_bikes[i]
            new_pos.get_child(bike, bike.row, bike.col+1)
            right_children.append(new_pos)
            new_pos = copy.deepcopy(new_pos)
            curr_col += 1

        # check west
        curr_col = position.right_bikes[i].col
        new_pos = copy.deepcopy(position)
        while curr_col-1 >= 0 and position.board[curr_row][
            curr_col-1] == 1:
            bike = new_pos.right_bikes[i]
            new_pos.get_child(bike, bike.row, bike.col-1)
            right_children.append(new_pos)
            new_pos = copy.deepcopy(new_pos)
            curr_col -= 1

        # check north
        curr_col = position.right_bikes[i].col
        curr_row = position.right_bikes[i].row
        new_pos = copy.deepcopy(position)
        while curr_row-1 >= 0 and position.board[curr_row-1][
            curr_col] == 1:
            bike = new_pos.right_bikes[i]
            new_pos.get_child(bike, bike.row-1, bike.col)
            right_children.append(new_pos)
            new_pos = copy.deepcopy(new_pos)
            curr_row -= 1

        # check south
        curr_row = position.right_bikes[i].row
        new_pos = copy.deepcopy(position)
        while curr_row+1 < position.nrows and position.board[curr_row+1][
            curr_col] == 1:
            #print(new_pos.board[curr_row+1][curr_col], "", curr_row+1, "",
            #      curr_col)
            #print(position.nrows)
            bike = new_pos.right_bikes[i]
            new_pos.get_child(bike, bike.row+1, bike.col)
            right_children.append(new_pos)
            new_pos = copy.deepcopy(new_pos)
            curr_row += 1

    return left_children, right_children


if __name__ == "__main__":
    initial_board = init_board()
    start = time.time()
    answer = find_outcome(initial_board)
    end = time.time()
    print(answer)
    print("Runtime:", end-start)
    # left, right = get_children(initial_board)
    #
    # print("LEFT CHILDREN")
    # for board in left:
    #     print("=================")
    #     board.to_str()
    #
    # print()
    # print("RIGHT CHILDREN")
    # print()
    #
    # for board in right:
    #     print("=================")
    #     board.to_str()
