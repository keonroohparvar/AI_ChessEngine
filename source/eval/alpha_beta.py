"""
This script will be the Monte Carlo implementation that will be the way our Chess Engine is able
to go down potential moves and choose the best one.

Author: Keon Roohparvar
Date: 11/3/2022
"""

# Imports
import os
import sys
import time

import tensorflow as tf
import numpy as np

# Local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from board import ChessBoard
from eval.count_material import eval_material


def alphaBetaMax(board, alpha, beta, depth, max_depth):
    # BELOW IS PRINTS FOR DEBBUGING
    # print(f'in max, depth is {depth} and board is ->')
    # board.print_board()
    # print(f'fen is {board.get_fen()}')
    # print(f'ev is : {eval_material(board)}')

    # Handles game-ending situations
    game_is_done, reason = board.game_is_done()
    if game_is_done:
        if reason == 'checkmate':
            # If it's checkmate and white's turn, then Black won -> -infinity
            if board.get_turn():
                return -1 * np.inf, depth
            # If it's checkmate and black's turn, then White won -> +infinity
            else:
                return +1 * np.inf, depth
        # Draw
        else: 
            return 0, depth

    # If Depth is max depth, we are at the end and we'll return the evaluation of this board
    if depth == max_depth:
        # this_evaluation = model.predict(np.array([board.positional_encode()]), verbose=0)[0][0]
        this_evaluation = eval_material(board)
        return this_evaluation, depth

    # Get Possible moves
    starter_board_fen = board.get_fen()
    legal_moves = list(board.get_legal_moves())
    possible_boards = []
    for legal_move in legal_moves:
        new_board = ChessBoard()
        new_board.set_fen(starter_board_fen)
        new_board.make_move(str(legal_move))
        possible_boards.append(new_board)
    
    # Iterate over moves while updating alpha; also, we watch for a beta break
    depth_reached = depth
    for board in possible_boards:
        this_board_score, this_depth_reached = alphaBetaMin(board, alpha, beta, depth+1, max_depth)
        if this_board_score >= beta:
            return beta, this_depth_reached
        if this_board_score > alpha:
            alpha = this_board_score
            depth_reached = this_depth_reached

    return alpha, depth_reached


def alphaBetaMin(board, alpha, beta, depth, max_depth):
    # BELOW IS PRINTS FOR DEBUGGING
    # print(f'in min, depth is {depth} and board is ->')
    # board.print_board()
    # print(f'fen is {board.get_fen()}')
    # print(f'ev is : {eval_material(board)}')

    # Handles game-ending situations
    game_is_done, reason = board.game_is_done()
    if game_is_done:
        if reason == 'checkmate':
            # If it's checkmate and white's turn, then Black won -> -infinity
            if board.get_turn():
                return -1 * np.inf, depth
            # If it's checkmate and black's turn, then White won -> +infinity
            else:
                return +1 * np.inf, depth
        # Draw
        else: 
            return 0, depth

    # If Depth is max depth, we are at the end and we'll return the evaluation of this board
    if depth == max_depth:
        this_evaluation = eval_material(board)
        return this_evaluation, depth


    # Get Possible moves
    starter_board_fen = board.get_fen()
    legal_moves = list(board.get_legal_moves())
    possible_boards = []
    for legal_move in legal_moves:
        new_board = ChessBoard()
        new_board.set_fen(starter_board_fen)
        new_board.make_move(str(legal_move))
        possible_boards.append(new_board)
    
    # Iterate over moves while updating beta; also, we watch for an alpha break
    depth_reached = depth
    for board in possible_boards:
        this_board_score, this_depth_reached = alphaBetaMax(board, alpha, beta, depth+1, max_depth)
        if this_board_score <= alpha:
            return alpha, this_depth_reached
        if this_board_score < beta:
            beta = this_board_score
            depth_reached = this_depth_reached
    
    # print(f'returning from min with beta of {beta}')
    return beta, depth_reached

def ab_pruning(turn, board, max_depth):
    # BELOW IS PRINTS FOR DEBUGGING
    # print(f'\n----ROOT-----\nTurn is {turn}, board is ->')
    # board.print_board()
    # print(f'fen is {board.get_fen()}')
    # ev = eval_material(board)
    # print(f'ev is : {ev}')
    # print('\n--\n')

    # Handles Draws/Stalemates
    game_is_done, reason = board.game_is_done()
    if game_is_done:
        if reason == 'checkmate':
            # If it's checkmate and white's turn, then Black won -> -infinity
            if board.get_turn():
                return None, -1 * np.inf, 1
            # If it's checkmate and black's turn, then White won -> +infinity
            else:
                return None, +1 * np.inf, 1
        # Draw
        else: 
            return None, 0, 1

    # Get all possible boards from this point
    original_fen = board.get_fen()
    legal_moves = list(board.get_legal_moves())
    possible_boards = []
    for legal_move in legal_moves:
        new_board = ChessBoard()
        new_board.set_fen(original_fen)
        new_board.make_move(str(legal_move))
        possible_boards.append(new_board)

    # Go through possibilities and do alpha beta pruning
    values = []
    times = []
    depths_reached = []
    for board in possible_boards:
        starttime = time.time()
        if turn == 'W':
            this_value, this_depth_reached = alphaBetaMin(board, alpha=-1*np.inf, beta=np.inf, depth=1, max_depth=max_depth)
        elif turn == 'B':
            this_value, this_depth_reached = alphaBetaMax(board, alpha=-1*np.inf, beta=np.inf, depth=1, max_depth=max_depth)

        endtime = time.time()
        times.append(endtime - starttime)

        # print(f'this val: {this_value}')
        values.append(this_value)
        depths_reached.append(this_depth_reached)
    
    # Choose the board that yields the highest value
    if turn == 'W':
        best_move = legal_moves[np.argmax(values)]
        # print(f'Best move: {best_move}\n----\n')
        return best_move, np.max(values), depths_reached[np.argmax(values)]
    else:
        best_move = legal_moves[np.argmin(values)]
        # print(f'Best move: {best_move}\n----\n')
        return best_move, np.min(values), depths_reached[np.argmin(values)]
        