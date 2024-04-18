#!/usr/bin/python3
""" 
author: Jueying Huang   z5490742
author: Mingxin Li      z5433288

1. How the program works in general: #--------------------------------#
    This program use angent.py's program frame.  It mainly use
Alpha-Beta pruning to reduce search complexity and Heuristic to
evaluate the board.


2. Algorithms Analyse: #----------------------------------------------#
    2.1: Alpha-Beta pruning algorithm is a tree pruning algorithm
which applies on MiniMax good at analyse two-player combinatorial
games.  However, this nine boards tik-tac-toe will make the tree 
with a depth of 81!  So we use alpha-beta pruning algorithm to 
cut-off unnecessary branches to reduce the complexity.
    
    Our alpha-beta pruning algorithm will search a specific number
of depth, if find a player in a win state then stop searching in 
this branch and return evaluate to reduce search cost.  Or when it
reach the claimed depth without find a win state then use Heuristic
to evaluate the score. 

    2.2: Heuristic been used to calculate both players advantages and 
disadvantages.  It will evaluate every sub boards by considering the
distance near the goal (self triple) and distance near lose (i.e 
distance of opponent near his triple).  Then add them together as a
evaluate for overall boards. (For more details, please read 4.2)
   

3. Data Structures employed:#-----------------------------------------#
    Dictionary list and numpy array are most important data structures
been used in this program.  
    The dictionary for example table, it stores the heuristic evaluate
results we calculated for a board.  

    And boards (array) and best_move (list) are built on numpy arrays.
They stores the overall nine tic-tac-toe's board and decision of moves
been calculated by the program separately.

    Other than data structures mentioned above we also use a lot of
integers, bool, string type of values. 

4. Decisions we made: #----------------------------------------------#
    4.1: The alpha-beta pruning algorithm we refer it from ttt.py, we
change it not too much.  Since original version of alpha-beta pruning
algorithm must reach the bottom (i.e. final of the game) then will
find the evaluate.  This is not realizable at now (the worst search
depth is 81!)   

    We set serval stages to decide how depth the alpha-beta pruning
algorithm to search. For example, at the start we only allow the program
search 6 level of depth (other wise will timeout, and not too much improve
for the decision).  And after couple of moves then increase the search
depth to allow the algorithm reach a real win state (the evaluate will be
much more precise)

    4.2: Originally we want to count conditions of go in a line: 
1. (one) one go (only X or O) and two empty. 2. (two) two go (only X or O)
and one empty. 3. (three) triple go.  And use the count numbers to
implement our heuristic formula: h = one * 10 + two * 45 + three * MAX
    For example: suppose X(0) is playing:
                (1,1,0) --> 0
              ↗
    +-------+
    | X . X | --> (0,2,0) --> The player have two go and one empty --> 45
    | . O . | --> (2,1,2) --> The opponent have one go and two empty --> -10
    | O O X | --> (1,1,0) --> 0
    +-------+
             ↘
              (0,1,0) --> 0
     - column 1: (0,2,1) --> 0
     - column 2: (2,1,1) --> The opponent have two go and one empty --> -90
     - column 3: (0,2,0) --> The player have two go and one empty --> 45
 

    We find to count out all number is an extra action comparing calculate
out all cases evaluate and store in a diction. So we made the 'table' in the
program to reduce the process to calculate and search.
"""

import socket
import sys
import numpy as np

WE = 0;     OPP = 1;    EMPTY = 2;  MAX_MOVE = 9
MIN_EVAL = -1000000;    MAX_EVAL = 1000000
START_DEPTH = 6;        MAX_DEPTH = 18

# the boards are of size 10 because index 0 isn't used
boards = EMPTY * np.ones((10, 10), dtype="int8")
best_move = np.zeros(100, dtype="int8")

# curr represent the current subboard. m represent count of m-th moves.  
s = ["X", "O", "."];    curr = 0;   m = 0

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

# ----------------------------------------------------------------#
# -------------------Evaluating The board-------------------------#
# ----------------------------------------------------------------#
table = { 
    # line: [eval for X(0), eval for O(1)]
    # line is a product of all possible cases of X(0), O(1) and Empty
    (1, 1, 0): [0, 4],  (1, 0, 1): [0, 0],    (0, 1, 1): [0, 4],
    (1, 0, 0): [4, 0],  (0, 1, 0): [0, 0],    (0, 0, 1): [4, 0],
    (2, 1, 0): [0, 0],  (2, 0, 1): [0, 0],    (0, 2, 1): [0, 0],
    (1, 2, 0): [0, 0],  (1, 0, 2): [0, 0],    (0, 1, 2): [0, 0],
    (2, 2, 2): [0, 0],

    (2, 1, 1): [-90, 45],   (1, 2, 1): [-90, 45],  (1, 1, 2): [-90, 45],
    (0, 0, 2): [45, -90],   (0, 2, 0): [45, -90],  (2, 0, 0): [45, -90],
    (0, 2, 2): [10, -10],   (2, 0, 2): [10, -10],  (2, 2, 0): [10, -10],
    (1, 2, 2): [-10, 10],   (2, 1, 2): [-10, 10],  (2, 2, 1): [-10, 10],

    (1, 1, 1): [MIN_EVAL, MAX_EVAL],
    (0, 0, 0): [MAX_EVAL, MIN_EVAL],
}

def evaluate(player):  
    eval = 0
    for board in boards[1:]:
        for i, j, k in [
            (1, 2, 3),  (4, 5, 6),    (7, 8, 9),    #Horizontal
            (1, 4, 7),  (2, 5, 8),    (3, 6, 9),    #Vertical
            (1, 5, 9),  (3, 5, 7),                  #Diagonal
        ]:
            line = (board[i], board[j], board[k])
            eval += table[line][player]

    return eval

def win(role, board, one_step=False):
    for i, j, k in [
        (1, 2, 3),  (4, 5, 6),    (7, 8, 9),    #Horizontal
        (1, 4, 7),  (2, 5, 8),    (3, 6, 9),    #Vertical
        (1, 5, 9),  (3, 5, 7),                  #Diagonal
    ]:
        line = [board[i], board[j], board[k]];  line.sort()

        if one_step and line == [role, role, EMPTY]:
            return (i, j, k)
        
        if not one_step and line == [role, role, role]:
            return (i, j, k)
        
    return None

# ----------------------------------------------------------------#
# -------------------Alpha Beta Prunning--------------------------#
# ----------------------------------------------------------------#
def alphabeta(player, m, board, alpha, beta, best_move, depth=6):
    best_eval = MIN_EVAL - 10

    if win(player, board, True):    #Check is one step left to win
        return MAX_EVAL - (MAX_DEPTH - depth)
    if win(1 - player, board):      #Check is win (triple) now
        return MIN_EVAL + (MAX_DEPTH - depth)

    if depth == 0:  return evaluate(player)

    this_move = 0
    for r in [1, 3, 7, 9, 5, 2, 4, 6, 8]:
        if board[r] == EMPTY:  # move is legal
            this_move = r
            board[this_move] = player  # make move
            this_eval = -alphabeta( 1 - player, m + 1, boards[this_move], -beta, -alpha, best_move, depth - 1,)

            board[this_move] = EMPTY  # undo move
            if this_eval > best_eval:
                best_move[m] = this_move
                best_eval = this_eval  # evaluate

                if best_eval > alpha:
                    alpha = best_eval
                    if alpha >= beta:  # cutoff
                        return alpha
    if this_move == 0:  # no legal moves
        return 0  # DRAW
    else:   return alpha


# choose a move to play
def play():
    global m

    # print_board(boards)
    if pos := win(WE, boards[curr], True):
        for x in pos:
            if boards[curr][x] == EMPTY:
                n = x;  break
    else:
        if m <= 14:
            alphabeta( WE, m, boards[curr], MIN_EVAL, MAX_EVAL, best_move, depth=START_DEPTH)
        elif m <= 18:
            alphabeta( WE, m, boards[curr], MIN_EVAL, MAX_EVAL, best_move, depth=START_DEPTH + 1)
        elif m <= 20:
            alphabeta( WE, m, boards[curr], MIN_EVAL, MAX_EVAL, best_move, depth=START_DEPTH + 2)
        elif m <= 22:
            alphabeta( WE, m, boards[curr], MIN_EVAL, MAX_EVAL, best_move, depth=START_DEPTH + 3)
        elif m <= 24:
            alphabeta( WE, m, boards[curr], MIN_EVAL, MAX_EVAL, best_move, depth=START_DEPTH + 5)
        elif m <= 26:
            alphabeta( WE, m, boards[curr], MIN_EVAL, MAX_EVAL, best_move, depth=START_DEPTH + 7)
        elif m <= 28:
            alphabeta( WE, m, boards[curr], MIN_EVAL, MAX_EVAL, best_move, depth=START_DEPTH + 9)
        elif m <= 32:
            alphabeta( WE, m, boards[curr], MIN_EVAL, MAX_EVAL, best_move, depth=START_DEPTH + 11)
        else:
            alphabeta(WE, m, boards[curr], MIN_EVAL, MAX_EVAL, best_move, depth=MAX_DEPTH)

        n = best_move[m]

    print("playing", n, "at", curr)
    place(curr, n, WE)
    m += 1
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
        OPP = 0
        WE = 1  # means oppenent use X we use O
        # place the first move (randomly generated for opponent)
        place(int(args[0]), int(args[1]), OPP)
        m += 1
        return play()  # choose and return the second move

    # third_move(K,L,M) means that the first and second move were
    # in square L of sub-board K, and square M of sub-board L,
    # and we are expected to return the third move.
    elif command == "third_move":
        WE = 0
        OPP = 1
        # place the first move (randomly generated for us)
        place(int(args[0]), int(args[1]), WE)
        # place the second move (chosen by opponent)
        place(curr, int(args[2]), OPP)
        m += 2
        return play()  # choose and return the third move

    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        # place the previous move (chosen by opponent)
        place(curr, int(args[0]), OPP)
        m += 1
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
