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
