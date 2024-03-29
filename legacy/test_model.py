"""
This script will be where we train the model off of Lichess positions so that it learns how to
approximate Stockfish's evaluation for a certain position. 

Incrementally, this script will save models to the saved_models/ directory, so that we will have 
model examples of how it looks through training.

Author: Keon Roohparvar
Date: 11/3/2022
"""

# Python Imports
import logging
import sys
import os
import importlib
import argparse
import linecache
import time

logging.basicConfig()
root = logging.getLogger(__name__)
root.setLevel(logging.INFO)
root.info('Importing packages...')

# Change env variable to surpress tf logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}
import tensorflow as tf

import numpy as np
import pandas as pd


from data_handler import game_to_data
from board import ChessBoard

# # Checks to see if running on GPU
# tf.debugging.set_log_device_placement(True)

# Do this to suppress TF warnings
tf.autograph.set_verbosity(2)

# Local Imports
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')
sys.path.append(MODEL_DIR)

def strlist_to_list(l):
    """
    This function will take a string representation of a list and convert it into a python list.
    For example, it will take the string representation '[1, 2, 3]' -> List([1, 2, 3])

    Arguments: 
        l (String): the string representation of a list
    Output:
        List: the list object
    """
    l_split = l.strip('][').split(', ')
    l_ints = [int(i) for i in l_split]
    return l_ints


def import_model(path_to_model_file):
    module = importlib.import_module(path_to_model_file, package='source')
    model_class = getattr(module, 'ChessAIModel')
    return model_class

def get_model(model_folder_name, learning_rate=1e-3):
    """
    This will interface with the model_architecture file to retrieve the proper model we want to 
    use for training.
    Argument:
        path_to_model_file (str): The location to your specific model file that contains the ChessAIModel
            class. For keon, it looks like -> "models.keon.model"
    Output:
        keras model: A keras model instance
    """
    module_name = model_folder_name + '.model'
    model_class = import_model(module_name)
    # Create model class
    model = (model_class()).get_model()
    return model

def save_model(model, model_dir, user):
    """
    This saves models in the saved model .h5 keras format. 

    Arguments:
        model (Keras Model): The model you want to save
        model_dir (str): Path to the models/ folder
        user (str): Your name (make sure you have a fodler in the models/ folder)
    """
    user_dir = os.path.join(model_dir, user)
    path_to_save = os.path.join(user_dir, 'saved_models')
    dirs_in_path = os.listdir(user_dir)
    if 'saved_models' not in dirs_in_path:
        os.makedirs(path_to_save)

    name_of_model = 'model' + str(len(os.listdir(path_to_save))) + '.h5'

    model.save(os.path.join(path_to_save, name_of_model))

def train_model(training_csv, user):
    """
    This is the big function that will train our neural network. 

    Argument:
        training_csv (filepath): The location of where our trainng fata is that we preprocessed
            in our data_handler.py file.
        user (str): your name - make sure a folder with your name exists in the models/ directory. For example, if
            you pass in 'keon' as the user parameter, then make sure a keon/ folder exists in models/.
    """
    # HYPERPARAMETERS
    NUM_GAMES = 1000
    MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')

    with open(training_csv, 'r') as f:
        total_number_of_games = sum(1 for _ in f)


    # # Load in data
    # train_x, test_x, train_y, test_y = load_dataset(training_csv)

    # Retrieve model
    root.info('Retrieving model...')
    model = get_model(user)

    for game_ind in range(1):
        # Random select game index 
        chosen_game_index = np.random.randint(0, total_number_of_games)

        # # Pull the game at the specified random index 
        # chosen_game = linecache.getline(training_csv, chosen_game_index, module_globals=None)

        # Get all of the data from this game
        basic_game_obj = ChessBoard()
        basic_game = basic_game_obj.positional_encode()
        basic_game_fen = basic_game_obj.get_fen()
        # print(f'fen: {basic_game_fen}')
        # print(len(basic_game))
        # print(basic_game[:12])
        # print(f'the rook piece is : {ChessBoard().piece_dict["r"]}')
        # print(basic_game[12:24])
        # print(f'the horsey: {basic_game_obj.piece_dict["n"]}')
        # print(f'basic game len: {len(basic_game)}')

        print('\n\n-----\n\n')
        print('Running on model!')

        from keras.layers import Input, Dense, Conv2D, Flatten, Concatenate, Reshape

        INPUT_SIZE = (776,)
        inputs = np.array([basic_game])
        BATCH_SIZE = inputs.shape[0]
        print(f'batch size; {BATCH_SIZE}')

        num_items_in_board = 12 * 8 * 8
        board_tensor, non_board_tensor = inputs[:, :num_items_in_board], inputs[:, num_items_in_board:]

        print(f'board tensor shape; {board_tensor.shape}')

        board_tensor_2d = Reshape(np.array([8, 8, 12]))(board_tensor)
        
        # for i in range(12):
        #     print(f'\n----\ni is {i}')
        #     print('this slice of board: ')
        #     print(board_tensor_2d[0, :, :, i])
     
        # # Train Model
        hist = model.fit(
            x=np.array([basic_game]), 
            y=np.array([0.]),
            epochs=10,
            batch_size=1,
            verbose=0
        )

        pred = model.predict(np.array([basic_game]))
        print(f'pred is: {pred}')

        move = str(list(basic_game_obj.get_legal_moves())[0])
        basic_game_obj.make_move(move)
        basic_game_obj.print_board()
        new_PE = basic_game_obj.positional_encode()
        new_pred = model.predict(np.array([new_PE]))
        print(f'new pred: {new_pred}')

        exit()

        # Get loss and log it
        loss = hist.history['loss'][-1]

    SAVE_MODEL = True
    if SAVE_MODEL:
        save_model(model, MODEL_DIR, user)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('csv_location', type=str)
    # parser.add_argument('model_dir', type=str)

    # args = parser.parse_args()

    # if not args.csv_location or (not os.path.isfile(args.csv_location)):
    #     print('ERROR - Did not provide a correct location to the training .csv file.')
    #     exit(-1)

    # if not args.model_dir or (args.model_dir not in os.listdir(MODEL_DIR)):
    #     print('ERROR - Did not provide a correct location to the model directory.')
    #     exit(-1)

    # train_model(args.csv_location, args.model_dir)

    train_model('/Users/keonroohparvar/Dev/SPD_Chessbot/data/games.csv', 'keon')

    # piece_dict = {
    #     'x': [1, 0, 0, 0],
    #     'y': [0, 1, 0, 0],
    #     'z': [0, 0, 1, 0],
    #     'a': [0, 0, 0, 1],
    #     '.': [0, 0, 0, 0]
    # }
    # s = 'xxxyyyz.z'
    # out_arr = []
    # for c in s:
    #     out_arr = out_arr + piece_dict[c]

    # out_arr = np.array(out_arr)
    # out_arr_reshaped = out_arr.reshape([3,3,4])
    # print(out_arr_reshaped)
    # print(out_arr_reshaped.shape)
    # print('----')
    # print(out_arr_reshaped[:, :, 2])
