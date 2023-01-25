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


# Local Imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
print(sys.path)
# from models.model_architecture import ChessAIModel

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
        filepath (str): Location of our .csv file
    
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

def get_model(path_to_model_file, learning_rate=1e-3):
    """
    This will interface with the model_architecture file to retrieve the proper model we want to 
    use for training.
    Argument:
        path_to_model_file (str): The location to your specific model file that contains the ChessAIModel
            class. For keon, it looks like -> "models.keon.model"
    Output:
        keras model: A keras model instance
    """
    module_name = path_to_model_file.replace('/', '.') + '.model'
    model_class = import_model(module_name)
    # Create model class
    model = (model_class()).get_model()
    return model

def save_model(model, path):
    """
    This saves models in the saved model .h5 keras format. 

    Arguments:
        model (Keras Model): The model you want to save
        path (str): Your specific folder (should be your name folder)
    """
    path_to_save = os.path.join(path, 'saved_models')
    dirs_in_path = os.listdir(path)
    if 'saved_models' not in dirs_in_path:
        os.makedirs(path_to_save)

    name_of_model = 'model' + str(len(os.listdir(path_to_save))) + '.h5'

    model.save(os.path.join(path_to_save, name_of_model))

def train_model(training_csv, model_dir):
    """
    This is the big function that will train our neural network. 

    Argument:
        training_csv (filepath): The location of where our trainng fata is that we preprocessed
            in our data_handler.py file.
        model_dir (filepath): Location of the directory that contains your model.py file and where
            you want to save your models.
    """
    # HYPERPARAMETERS
    NUM_EPOCHS = 10
    BATCH_SIZE = 128

    # Load in data
    train_x, test_x, train_y, test_y = load_dataset(training_csv)

    # Retrieve model
    model = get_model(model_dir)

    # Train Model
    model.fit(
        x=train_x, 
        y=train_y,
        epochs=NUM_EPOCHS,
        batch_size=BATCH_SIZE,
    )

    SAVE_MODEL = True
    if SAVE_MODEL:
        save_model(model, model_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_location', type=str)
    parser.add_argument('model_dir', type=str)

    args = parser.parse_args()

    if not args.csv_location or (not os.path.isfile(args.csv_location)):
        print('ERROR - Did not provide a correct location to the training .csv file.')
        exit(-1)

    if not args.model_dir or (not os.path.isdir(args.model_dir)):
        print('ERROR - Did not provide a correct location to the model directory.')
        exit(-1)

    train_model(args.csv_location, args.model_dir)
