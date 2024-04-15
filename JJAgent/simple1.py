EMPTY = 0
WEPLAY = 1
OPPONENT = 2

MIN_EVAL = -1000000
MAX_EVAL = 1000000


def move_at(boards, curr):
    for i in range(1, 10):
        if boards[curr][i] != EMPTY:
            pass


def next_board(boards, curr, my_turn=0, deepth=3):
    score = 0
    board = boards[curr]
    for i in range(1, 10):
        if board[i] != EMPTY:
            if not my_turn:
                if board[i] == OPPONENT:
                    score -= 20 * (2**deepth)
                elif board[i] == WEPLAY:
                    score -= 10 * (2**deepth)
                if one_step_win(OPPONENT, board):
                    # print("@28 X is one step to win at", one_step_win(OPPONENT, board))
                    score -= MAX_EVAL
            else:
                if board[i] == WEPLAY:
                    score += 20 * (2**deepth)
                elif board[i] == OPPONENT:
                    score += 10 * (2**deepth)
                if one_step_win(WEPLAY, board):
                    # print("@28 O is one step to win at", one_step_win(WEPLAY, board))
                    score += MAX_EVAL
        if deepth > 0 and board[i] == EMPTY:
            board[i] = WEPLAY if my_turn else OPPONENT
            score += next_board(boards, i, 1 - my_turn, deepth - 1)
            board[i] = EMPTY
    return score / 10


def one_step_win(role, board):
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
        if sorted(line) == [EMPTY, role, role]:
            return (i, j, k)
    return None
