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
from datetime import datetime

logging.basicConfig()
root = logging.getLogger(__name__)
root.setLevel(logging.INFO)
root.info('Importing packages...')

# Change env variable to surpress tf logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}
import tensorflow as tf
import keras

import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from data_handler import game_to_data

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

def load_dataset(filepath):
    """
    This will simply load in the data we have already processed in data_handler.py, but it will
    be used in this file

    Arguments:
        filepath (str): Location of our .txt file with our games
    
    Output:
        array: Array of data points we will use
    """
    df = pd.read_csv(filepath, header=None)

    # Bound values between [-15, 15]
    y = df.pop(df.columns[-1])
    y = y.clip(upper=15, lower=-15)
    print(y.head())

    # Split into training + testing
    train_x, test_x, train_y, test_y = train_test_split(df, y, test_size=0.2)

    return train_x, test_x, train_y, test_y

def import_model(name):
    """
    Dynamic function to import a custom class based off of the name of who implemented it.
    For example, passing in 'keon' will dynamically load Keon's model, while passing in 'corey'
    will dynamically load corey's instead. 

    Arguments: 
        name (str): The name of the person who implemented a model in the models/ dir
    """
    module = importlib.import_module(name, package='source')
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
    NUM_BATCHES_TO_TRAIN = 100
    NUM_GAMES_PER_BATCH = 10
    MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')
    
    # Create log dir and callback
    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', user, 'logs/') + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=LOG_DIR)
    

    with open(training_csv, 'r') as f:
        total_number_of_games = sum(1 for _ in f)

    # Retrieve model
    root.info('Retrieving model...')
    model = get_model(user)

    with tqdm(range(NUM_BATCHES_TO_TRAIN), unit='batch') as progress_bar:
        progress_bar.set_description('Training the Model')
        for game_ind in progress_bar:
            this_batch_x, this_batch_y = None, None

            for _ in range(NUM_GAMES_PER_BATCH):
                # Random select game index 
                chosen_game_index = np.random.randint(0, total_number_of_games)

                # Pull the game at the specified random index 
                chosen_game = linecache.getline(training_csv, chosen_game_index, module_globals=None)

                # Get all of the data from this game
                this_game_x, this_game_y = game_to_data(chosen_game)

                if this_batch_x is None or this_batch_y is None:
                    this_batch_x = this_game_x
                    this_batch_y = this_game_y

                # Append this game's information to our batches TODO
                this_batch_x = pd.concat([this_batch_x, this_game_x], ignore_index=True)
                this_batch_y = pd.concat([this_batch_y, this_game_y], ignore_index=True)

            if game_ind == 0:
                print(this_batch_x)
                print('----\n')
                print(this_batch_y)
                print(f'y min and max: {this_batch_y.min()} $ {this_batch_y.max()}')

            # Train Model
            try:
                if game_ind % 50 == 0:
                    hist = model.fit(
                        x=this_batch_x, 
                        y=this_batch_y,
                        epochs=100,
                        batch_size=64,
                        verbose=1,
                        callbacks=[tensorboard_callback]
                    )
                else:
                    hist = model.fit(
                        x=this_batch_x, 
                        y=this_batch_y,
                        epochs=5,
                        batch_size=64,
                        verbose=0
                    )


            except:
                root.error(f'Error with the following data')
                print(f'Game number: {chosen_game_index}')
                print(f'game line: {chosen_game}')
                print(this_game_x)
                print(this_game_y)
                exit()

            # Get loss and log it
            if game_ind == 0:
                print(hist.history['loss'])
            loss = hist.history['loss'][-1]
            progress_bar.set_postfix(loss=loss)

    SAVE_MODEL = True
    if SAVE_MODEL:
        save_model(model, MODEL_DIR, user)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_location', type=str)
    parser.add_argument('model_dir', type=str)

    args = parser.parse_args()

    if not args.csv_location or (not os.path.isfile(args.csv_location)):
        print('ERROR - Did not provide a correct location to the training .csv file.')
        exit(-1)

    if not args.model_dir or (args.model_dir not in os.listdir(MODEL_DIR)):
        print('ERROR - Did not provide a correct location to the model directory.')
        exit(-1)

    train_model(args.csv_location, args.model_dir)
