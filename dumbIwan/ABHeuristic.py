#!/usr/bin/python3
#  SmartAgent.py
#  Nine-Board Tic-Tac-Toe Agent starter code
#  COMP3411/9814 Artificial Intelligence
#  CSE, UNSW

import socket
import sys
import numpy as np

EMPTY = 2
MAX_MOVE = 9

# a board cell can hold:
#   0 - Empty -> 2 - Empty
#   1 - We played here -> WE 0
#   2 - Opponent played here -> OPP 1
WE = 0;     OPP = 1;    EMPTY = 2
MIN_EVAL = -1000000
MAX_EVAL = 1000000


# the boards are of size 10 because index 0 isn't used
boards = EMPTY * np.ones((10, 10), dtype="int8")
s = ["X", "O", "."]
curr = 0  # this is the current board to play in
best_move = np.zeros(100, dtype="int8")
m = 0

# print a row
def print_board_row(bd, a, b, c, i, j, k):
    print(" "+s[bd[a][i]]+" "+s[bd[a][j]]+" "+s[bd[a][k]]+" | " \
             +s[bd[b][i]]+" "+s[bd[b][j]]+" "+s[bd[b][k]]+" | " \
             +s[bd[c][i]]+" "+s[bd[c][j]]+" "+s[bd[c][k]])


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

#----------------------------------------------------------------#
#-------------------Alpha Beta Prunning--------------------------#
#----------------------------------------------------------------#
def evaluate(player): #以player为考虑标准. 如果是优势局返回值应该是负的, 否则是正的. 

    (player,	player,	    1-player)
    (player,	player,	    EMPTY)
    (player,	1-player,	player)
    (player,	1-player,	1-player)
    (player,	1-player,	EMPTY)
    (player,	EMPTY,	    player)
    (player,	EMPTY,	    1-player)
    (player,	EMPTY,	    EMPTY)
    (1-player,	player,	    player)
    (1-player,	player,	    1-player)
    (1-player,	player,	    EMPTY)
    (1-player,	1-player,	player)
    (1-player,	1-player,	EMPTY)
    (1-player,	EMPTY,	    player)
    (1-player,	EMPTY,	    1-player)
    (1-player,	EMPTY,	    EMPTY)
    (EMPTY,	    player,	    player)
    (EMPTY,	    player,	    1-player)
    (EMPTY,	    player,	    EMPTY)
    (EMPTY,	    1-player,	player)
    (EMPTY,	    1-player,	1-player)
    (EMPTY,	    1-player,	EMPTY)
    (EMPTY,	    EMPTY,	    player)
    (EMPTY,	    EMPTY,	    1-player)
    (EMPTY,	    EMPTY,	    EMPTY)

    return  0

def win(role, board):
    for i, j, k in [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 9),
        (1, 5, 9),
        (3, 5, 7),
    ]:
        line = [board[i], board[j], board[k]]
        if sorted(line) == [role, role, role]:
            return (i, j, k)
    return None

def alphabeta( player, m, board, alpha, beta, best_move, depth=10 ):

    best_eval = MIN_EVAL

    if win( 1-player, board ):   
        return -1000 + m  # better to win faster (or lose slower)

    if depth == 0:
        return evaluate(1-player)

    this_move = 0
    for r in range( 1, 10):
        if board[r] == EMPTY:         # move is legal
            this_move = r
            board[this_move] = player # make move
            this_eval = -alphabeta(1-player, m+1, boards[this_move], -beta, -alpha, best_move, depth-1)
            board[this_move] = EMPTY  # undo move
            if this_eval > best_eval:
                best_move[m] = this_move
                best_eval = this_eval #evaluate 评估
                if best_eval > alpha:
                    alpha = best_eval
                    if alpha >= beta: # cutoff
                        return( alpha )

    if this_move == 0:  # no legal moves
        return( 0 )     # DRAW
    else:
        return( alpha )

# choose a move to play
def play():
    global m
    
    alphabeta( WE, m, boards[curr], MIN_EVAL, MAX_EVAL, best_move )
    n = best_move[m]


    
    print("playing", n, "at", curr)
    place(curr, n, WE)
    m+=1
    return n



# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    boards[board][num] = player


# read what the server sent us and
# parse only the strings that are necessary
def parse(string):
    global WE, OPP, m
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
        OPP = 0; WE = 1 #means oppenent use X we use O
        # place the first move (randomly generated for opponent)
        place(int(args[0]), int(args[1]), OPP)
        m+=1
        return play()  # choose and return the second move

    # third_move(K,L,M) means that the first and second move were
    # in square L of sub-board K, and square M of sub-board L,
    # and we are expected to return the third move.
    elif command == "third_move":
        WE = 0; OPP = 1
        # place the first move (randomly generated for us)
        place(int(args[0]), int(args[1]), WE)
        # place the second move (chosen by opponent)
        place(curr, int(args[2]), OPP)
        m+=2
        return play() # choose and return the third move

    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        # place the previous move (chosen by opponent)
        place(curr, int(args[0]), OPP)
        m+=1
        return play() # choose and return our next move

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
