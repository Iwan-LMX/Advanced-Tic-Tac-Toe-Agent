#!/usr/bin/python3
#  agent.py
#  Nine-Board Tic-Tac-Toe Agent starter code
#  COMP3411/9814 Artificial Intelligence
#  CSE, UNSW

import socket
import sys
import numpy as np

from simple1 import *

EMPTY = 0

MAX_MOVE = 9

MIN_EVAL = -1000000
MAX_EVAL = 1000000

# a board cell can hold:
#   0 - Empty
#   1 - We played here
#   2 - Opponent played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
s = [".", "X", "O"]
curr = 0  # this is the current board to play in


# print a row
def print_board_row(bd, a, b, c, i, j, k):
    print(
        " "
        + s[bd[a][i]]
        + " "
        + s[bd[a][j]]
        + " "
        + s[bd[a][k]]
        + " | "
        + s[bd[b][i]]
        + " "
        + s[bd[b][j]]
        + " "
        + s[bd[b][k]]
        + " | "
        + s[bd[c][i]]
        + " "
        + s[bd[c][j]]
        + " "
        + s[bd[c][k]]
    )


# Print the entire board
def print_board(board):
    print_board_row(board, 1, 2, 3, 1, 2, 3)
    print_board_row(board, 1, 2, 3, 4, 5, 6)
    print_board_row(board, 1, 2, 3, 7, 8, 9)
    print(" ------+-------+------")
    print_board_row(board, 4, 5, 6, 1, 2, 3)
    print_board_row(board, 4, 5, 6, 4, 5, 6)
    print_board_row(board, 4, 5, 6, 7, 8, 9)
    print(" ------+-------+------")
    print_board_row(board, 7, 8, 9, 1, 2, 3)
    print_board_row(board, 7, 8, 9, 4, 5, 6)
    print_board_row(board, 7, 8, 9, 7, 8, 9)
    print()


# **********************************************************
#   Return True if game won by player p on board bd[]
#
def game_won(p, bd):
    # print("@73", bd)
    return (
        (bd[1] == p and bd[2] == p and bd[3] == p)
        or (bd[4] == p and bd[5] == p and bd[6] == p)
        or (bd[7] == p and bd[8] == p and bd[9] == p)
        or (bd[1] == p and bd[4] == p and bd[7] == p)
        or (bd[2] == p and bd[5] == p and bd[8] == p)
        or (bd[3] == p and bd[6] == p and bd[9] == p)
        or (bd[1] == p and bd[5] == p and bd[9] == p)
        or (bd[3] == p and bd[5] == p and bd[7] == p)
    )


# **********************************************************
#   Negamax formulation of alpha-beta search
#
def alphabeta(player, m, board, alpha, beta, best_move, eval_list):
    # print("@90", eval_list)
    best_eval = MIN_EVAL

    if game_won(3 - player, board):  # LOSS
        return -1000 + m
        # better to win faster (or lose slower)

    this_move = 0
    for r in range(1, 10):
        if board[r] == EMPTY:  # move is legal
            this_move = r
            board[this_move] = player  # make move
            this_eval = -alphabeta(
                3 - player, m + 1, board, -beta, -alpha, best_move, eval_list
            )
            board[this_move] = EMPTY
            # undo move
            if this_eval > best_eval:
                best_move[m] = this_move
                best_eval = this_eval
                eval_list[m][this_move] = this_eval
                if best_eval > alpha:
                    alpha = best_eval
                    if alpha >= beta:  # cutoff
                        return alpha

    if this_move == 0:  # no legal moves
        return 0  # DRAW
    else:
        return alpha


# choose a move to play
def play():
    print("Agent state:")
    print_board(boards)

    best_eval = MIN_EVAL * 100
    player = 1
    print(f"At board {curr}:", boards[curr])
    if one_step_win(player, boards[curr]):
        for x in one_step_win(player, boards[curr]):
            if boards[curr][x] == EMPTY:
                n = x
                break
    else:
        for i in [5, 1, 3, 7, 9, 2, 4, 6, 8]:
            if boards[curr][i] == EMPTY:
                boards[curr][i] = player
                if (this_evel := next_board(boards, i)) > best_eval:
                    best_eval = this_evel
                    n = i
                print("@87", i, this_evel)
                boards[curr][i] = EMPTY  # Roll back

    print("playing", n, "at", curr)
    place(curr, n, 1)
    return n


# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    boards[board][num] = player


# read what the server sent us and
# parse only the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    # init tells us that a new game is about to begin.
    # start(x) or start(o) tell us whether we will be playing first (x)
    # or second (o); we might be able to ignore start if we internally
    # use 'X' for *our* moves and 'O' for *opponent* moves.

    # second_move(K,L) means that the (randomly generated)
    # first move was into square L of sub-board K,
    # and we are expected to return the second move.
    if command == "second_move":
        # place the first move (randomly generated for opponent)
        place(int(args[0]), int(args[1]), 2)
        return play()  # choose and return the second move

    # third_move(K,L,M) means that the first and second move were
    # in square L of sub-board K, and square M of sub-board L,
    # and we are expected to return the third move.
    elif command == "third_move":
        # place the first move (randomly generated for us)
        place(int(args[0]), int(args[1]), 1)
        # place the second move (chosen by opponent)
        place(curr, int(args[2]), 2)
        return play()  # choose and return the third move

    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        # place the previous move (chosen by opponent)
        place(curr, int(args[0]), 2)
        return play()  # choose and return our next move

    elif command == "win":
        print("Yay!! We win!! :)")
        return -1

    elif command == "loss":
        print("We lost :(")
        return -1

    return 0


# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2])  # Usage: ./agent.py -p (port)

    s.connect(("localhost", port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())


if __name__ == "__main__":
    main()
