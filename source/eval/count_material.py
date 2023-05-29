"""
This script is a basic one that simply has a functon that returns the difference of material.

"""

# Imports
import os
import sys
import time

import tensorflow as tf
import numpy as np

def eval_material(board):
    fen = board.get_fen()

    # Handles end game boards
    game_is_done, reason = board.game_is_done()
    if game_is_done:
        if reason == 'checkmate':
            # If it's checkmate and white's turn, then Black won -> -infinity
            if board.get_turn():
                return -1 * np.inf
            # If it's checkmate and black's turn, then White won -> +infinity
            else:
                return +1 * np.inf
        # Draw
        else: 
            return 0


    piece_dict = {
        'p':-1,
        'n':-3,
        'b':-3,
        'r':-5,
        'q':-10,
        'k':0, # Black King does not change val
        'P':1,
        'N':3,
        'B':3,
        'R':5,
        'Q':10,
        'K': 0 # White King does not change val
    }

    this_sum = 0
    for c in fen.split(' ')[0]:
        if c in piece_dict.keys():
            this_sum += piece_dict[c]

    return this_sum
