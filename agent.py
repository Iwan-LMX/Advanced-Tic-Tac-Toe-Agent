#!/usr/bin/python3
#  agent.py
#  Nine-Board Tic-Tac-Toe Agent starter code
#  COMP3411/9814 Artificial Intelligence
#  CSE, UNSW

import socket
import sys
import numpy as np

# a board cell can hold:
#   0 - Empty -> 2 - Empty
#   1 - We played here -> WE 0
#   2 - Opponent played here -> OPP 1
WE = 0;     OPP = 1;    EMPTY = 2
MIN_EVAL = -1000000
MAX_EVAL =  1000000
# the boards are of size 10 because index 0 isn't used
boards = EMPTY * np.ones((10, 10), dtype="int8")
s = ["X", "O", "."]
curr = 0 # this is the current board to play in

# print a row
def print_board_row(bd, a, b, c, i, j, k):
    print(" "+s[bd[a][i]]+" "+s[bd[a][j]]+" "+s[bd[a][k]]+" | " \
             +s[bd[b][i]]+" "+s[bd[b][j]]+" "+s[bd[b][k]]+" | " \
             +s[bd[c][i]]+" "+s[bd[c][j]]+" "+s[bd[c][k]])

# Print the entire board
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()

def evaluate(board_num, player, weight: int = 1, depth: int = 1):
    global boards
    board = tuple(boards[board_num])
    evalu = 0

    if depth == 0:
        return evalu

    # 递归评估未来局
    if board in evaluates:
        try:
            evalu, move = evaluates[board][player]
            evalu -= evaluate(move, 1-player, weight-0.2, depth-1)
        except:
            evalu = 0

    return evalu
    
    
    
    
    return evaluate * weight #0.8 表示未来局的权重

def win(board, player):
    return(  ( board[1] == player and board[2] == player and board[3] == player )
           or( board[4] == player and board[5] == player and board[6] == player )
           or( board[7] == player and board[8] == player and board[9] == player )
           or( board[1] == player and board[4] == player and board[7] == player )
           or( board[2] == player and board[5] == player and board[8] == player )
           or( board[3] == player and board[6] == player and board[9] == player )
           or( board[1] == player and board[5] == player and board[9] == player )
           or( board[3] == player and board[5] == player and board[7] == player ))

# choose a move to play
def play():
    global WE, OPP, EMPTY

    best_eval = MIN_EVAL;   future_eval = MIN_EVAL

    #假设没有优选位置 (这是因为当前的map数据量太小, 有可能没有覆盖到)
    move = np.random.randint(1,9)
    while boards[curr][move] != EMPTY:
        move = np.random.randint(1,9)
    

    for i in range(1, 10):
        #因为未来局是对手先下, 要让他的eva最低
        if boards[curr][i] == EMPTY:
            future_eval = -evaluate(i, OPP, 0.8, 2)
        else:
            continue

        #测试当前局, 这里要让我们的eva最高
        boards[curr][i] = WE #测试该位置落子
        if win(boards[curr], WE):
            boards[curr][i] = EMPTY;    move = i
            break
        else:
            cur_eval = future_eval + evaluate(curr, WE)
        
        if best_eval < cur_eval:
            best_eval = cur_eval;   move = i

        boards[curr][i] = EMPTY #restore

    # print("playing", n)
    place(curr, move, WE)
    return move

# place a move in the global boards
def place( board, num, player ):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# parse only the strings that are necessary
def parse(string):
    global WE, OPP
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
        return play() # choose and return the third move

    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        # place the previous move (chosen by opponent)
        place(curr, int(args[0]), OPP)
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
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
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

# class Log:
#     board = 

if __name__ == "__main__": 

    evaluates = {}
    evaluates = np.load('evaluate.npy', allow_pickle=True).item()
    main()
