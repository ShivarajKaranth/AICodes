"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    init_val=0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j]==EMPTY:
               init_val +=1
    
    if init_val%2!=0:
        return "X"
    else:
        return "O"    
 


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    allowed_mov=set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j]==EMPTY:
                allowed_mov.add((i,j))
    return allowed_mov



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j=action
    if i<3 and j<3 and board[i][j] is EMPTY:
        current_gamer=player(board)
        game_reset=copy.deepcopy(board)
        game_reset[i][j]=current_gamer
        return game_reset
    else:
        raise Exception("Invalid Move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[0][i]=="X" and board[1][i]=="X" and board[2][i]=="X":
            return X
        elif board[0][i]=="O" and board[1][i]=="O" and board[2][i]=="O":
            return O
    for i in range(3):
        if board[i][0]=="X" and board[i][1]=="X" and board[i][2]=="X":
            return X
        elif board[i][0]=="O" and board[i][1]=="O" and board[i][2]=="O":
            return O
    if board[0][0]=="X" and board[1][1]=="X" and board[2][2]=="X":
        return X
    elif board[0][0]=="O" and board[1][1]=="O" and board[2][2]=="O":
        return O
    if board[0][2]=="X" and board[1][1]=="X" and board[2][0]=="X": 
        return X
    elif board[0][2]=="O" and board[1][1]=="O" and board[2][0]=="O":
        return O
    return None

        


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board)!=None:
        return True
    if any(None in cell for cell in board):
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
        return 1
    elif winner(board)==O:
        return -1
    else:
        return 0

def MIN_VAL(board):
    if terminal(board):
        return utility(board)
    value=1
    for action in actions(board):
        value=min(value,MAX_VAL(result(board,action)))
        if value==-1:
            break
    return value

def MAX_VAL(board):
    if terminal(board):
        return utility(board)
    value=-1
    for action in actions(board):
        value=max(value,MIN_VAL(result(board,action)))
        if value==1:
            break
    return value



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board)=="X":
        good_val=-1
        good_move=(-1,-1)
        blank_cell=sum(cell.count(EMPTY) for cell in board)
        if blank_cell==9:
            return good_move
        for action in actions(board):
            act_val=MIN_VAL(result(board,action))
            if act_val==1:
                good_move=action
                break
            if act_val>good_val:
                good_move=action
        return good_move
    
    if player(board)=="O":
        good_val=1
        good_move=(-1,-1)
        
        for action in actions(board):
            act_val=MAX_VAL(result(board,action))
            if act_val==-1:
                good_move=action
                break
            if act_val<good_val:
                good_move=action
        return good_move

