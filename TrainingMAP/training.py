#!/usr/bin/python3
import itertools
# 创建一个长度为 9 的列表，全由 2 组成
original_list = [2] * 10

# 获取 1 的个数（n）
n = 5  # 你可以根据需要修改 n 的值

# 在列表中插入 n 个 1 或 0，并获取所有可能的组合
boards = []
for i in range(n):
    for indices in itertools.combinations(range(1, 10), i + 1):
        new_list_X = original_list.copy()
        new_list_O = original_list.copy()
        for idx in indices:
            new_list_X[idx] = 0
            new_list_O[idx] = 1
        boards.append(new_list_X)
        boards.append(new_list_O)



import pickle
import random
import numpy as np
EMPTY = 2

ILLEGAL_MOVE  = 0
STILL_PLAYING = 1
WIN           = 2
LOSS          = 3
DRAW          = 4

MAX_MOVE      = 4

MIN_EVAL = -1000000
MAX_EVAL =  1000000




def main(board):
    # global board
    # board = EMPTY*np.ones(10,dtype=np.int32)
    move = np.zeros(10,dtype=np.int32)
    best_move1 = np.zeros(10,dtype=np.int32)
    best_move2 = np.zeros(10,dtype=np.int32)
    is_human = (True,False)
    game_status = STILL_PLAYING
    player = 1
    m = 0

    while m < MAX_MOVE and game_status == STILL_PLAYING:
        m += 1 #m可以表示第多少move, 也可以表示当前落子总量
        player = 1-player

        if is_human[player]: # humann 时 player = 0
            move[m] = randmove ( board )
            alphabeta( player,m,board,MIN_EVAL,MAX_EVAL,best_move1 )
            alphabeta( 1-player,m,board,MIN_EVAL,MAX_EVAL,best_move2 )
            # move[m] = best_move1[m]

        else:
            move[m] = randmove ( board )
            alphabeta( 1-player,m,board,MIN_EVAL,MAX_EVAL,best_move1 )
            alphabeta( player,m,board,MIN_EVAL,MAX_EVAL,best_move2 )
            # move[m] = best_move2[m]

        game_status = make_move( player, m, move, board )

        # print_board( board )
        # print()


def recEvaluate(board, player, move, evaluate):
    if board not in evaluates:
        evaluates[board] = [[], []]
    if not evaluates[board][player]: #never stored
        evaluates[board][player] = [evaluate, move]
    elif evaluates[board][player][0] < evaluate:
        evaluates[board][player] = [evaluate, move]

#**********************************************************
#   Print the board
#
def print_board( bd ):
    sb = 'XO.'
    print('|',sb[bd[1]],sb[bd[2]],sb[bd[3]],'|')
    print('|',sb[bd[4]],sb[bd[5]],sb[bd[6]],'|')
    print('|',sb[bd[7]],sb[bd[8]],sb[bd[9]],'|')

#**********************************************************
#   Print the board
#
def randmove(board):
    move = random.randint(1, 9)
    while board[move] != EMPTY:
        move = random.randint(1, 9)
    
    return move

#**********************************************************
#   Negamax formulation of alpha-beta search
#
def alphabeta( player, m, board, alpha, beta, best_move2 ):

    best_eval = MIN_EVAL

    if game_won( 1-player, board ):   # LOSS 判断是否胜利
        return -500 + m  # better to win faster (or lose slower)

    this_move = 0
    for r in range( 1, 10):
        if board[r] == EMPTY:         # move is legal
            this_move = r
            board[this_move] = player # make move
            this_eval = -alphabeta(1-player,m+1,board,-beta,-alpha,best_move2)
            board[this_move] = EMPTY  # undo move
            if this_eval > best_eval:
                best_move2[m] = this_move
                best_eval = this_eval #evaluate 评估
                recEvaluate( tuple(board), player, this_move, this_eval)
                if best_eval > alpha:
                    alpha = best_eval
                    if alpha >= beta: # cutoff
                        return( alpha )

    if this_move == 0:  # no legal moves
        return( 0 )     # DRAW
    else:
        return( alpha )

#**********************************************************
#   Make specified move on the board and return game status
#
def make_move( player, m, move, board ):
    if board[move[m]] != EMPTY:
        print('Illegal Move')
        return ILLEGAL_MOVE
    else:
        board[move[m]] = player
        if game_won( player, board ):
            return WIN
        elif full_board( board ):
            return DRAW
        else:
            return STILL_PLAYING

#**********************************************************
#   Return True if the board is full
#
def full_board( board ):
    b = 1
    while b <= 9 and board[b] != EMPTY:
        b += 1
    return( b == 10 )

#**********************************************************
#   Return True if game won by player p on board bd[]
#
def game_won( p, bd ): # 8种胜利条件, 3横3纵2斜
    return(  ( bd[1] == p and bd[2] == p and bd[3] == p )
           or( bd[4] == p and bd[5] == p and bd[6] == p )
           or( bd[7] == p and bd[8] == p and bd[9] == p )
           or( bd[1] == p and bd[4] == p and bd[7] == p )
           or( bd[2] == p and bd[5] == p and bd[8] == p )
           or( bd[3] == p and bd[6] == p and bd[9] == p )
           or( bd[1] == p and bd[5] == p and bd[9] == p )
           or( bd[3] == p and bd[5] == p and bd[7] == p ))

if __name__ == '__main__':
    evaluates = {}
    evaluates = np.load('evaluate.npy', allow_pickle=True).item()

    random.seed()

    for board in boards:
        if game_won(0, board) or game_won(1, board):
            continue
    # for board play epoch turns:
        for epoch in range(500):
            main(np.array(board))

    np.save('evaluate.npy', evaluates)