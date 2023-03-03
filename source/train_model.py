"""
This script will be where we train the model off of Lichess positions so that it learns how to
approximate Stockfish's evaluation for a certain position. 

Incrementally, this script will save models to the saved_models/ directory, so that we will have 
model examples of how it looks through training.

Author: Keon Roohparvar
Date: 11/3/2022
"""

# Python Imports
import sys
import os
import importlib
import argparse

import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# # Checks to see if running on GPU
# tf.debugging.set_log_device_placement(True)


# Local Imports
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')
sys.path.append(MODEL_DIR)
print(sys.path)

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
    NUM_EPOCHS = 10
    BATCH_SIZE = 128
    MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')


    # Load in data
    train_x, test_x, train_y, test_y = load_dataset(training_csv)

    # Retrieve model
    model = get_model(user)



    # Train Model
    model.fit(
        x=train_x, 
        y=train_y,
        epochs=NUM_EPOCHS,
        batch_size=BATCH_SIZE,
    )

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
