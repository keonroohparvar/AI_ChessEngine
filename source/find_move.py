"""
This is the script that the mechatronics team will interface with when finding moves.

There is one function named find_best_move() that will take in a Board's FEN notation 
string (this is found online) and it will return the string representation of a move.
For example, if the find_best_move() function determines that the pawn on c2 going to c4
is the best move in this position, it will return the string "c2c4" which is chess' 
notation for that pawn move.

Just make sure your python environment has the appropriate packages installed (should be 
found in requirements.txt and can be insalled wiht the command `pip install -r requirements.txt`).

IMPORTANT: CALL THIS FILE BY DOING THE FOLLOWING:

`
python find_move.py "INSERT YOUR FEN STRING HERE IN QUOTES"
`
"""

# Python Imports
import os
import sys
import time
import tensorflow as tf

# Local imports
from board import ChessBoard
from eval.eval_board import evaluate_board

# Set tf logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

# Dynamically get path to our trained neural network
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            'models', 
                            'keon', 
                            'saved_models', 
                            'model_example.h5')

def main():
    # Make sure the user passed in a fen string and nothing else
    if len(sys.argv) == 1:
        exit(f'Error - User passed in {len(sys.argv)} argument when only 2 were required.')
    if len(sys.argv) > 2:
        exit(f'Error - User passed in {len(sys.argv)} arguments when only 2 were required.')
    
    # Get fen string and make sure it's valid
    fen = sys.argv[1]
    board = ChessBoard()
    board.set_fen(fen)
    validity = board.get_validity()

    if not validity:
        exit()

    # Load in model
    model = tf.keras.models.load_model(MODEL_PATH)

    # Get best move
    start_time = time.time()
    best_move, _ = evaluate_board(board, model, board.get_turn())
    end_time = time.time()

    print(f'Best move: {best_move}')
    print(f'Time to make move: {end_time - start_time}')

    return best_move






if __name__ == '__main__':
    main()

