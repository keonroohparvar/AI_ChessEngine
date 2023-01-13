"""
This script will be where we train the model off of Lichess positions so that it learns how to
approximate Stockfish's evaluation for a certain position. 

Incrementally, this script will save models to the saved_models/ directory, so that we will have 
model examples of how it looks through training.

Author: Keon Roohparvar
Date: 11/3/2022
"""

# Python Imports
import os
import argparse
import tensorflow as tf
import numpy as np
import pandas as pd


# Local Imports
from model_architecture import ChessAIModel

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
    return df[0], df[1]

def get_model(type_of_model, learning_rate):
    """
    This will interface with the model_architecture file to retrieve the proper model we want to 
    use for training.

    Argument:
        type_of_model (str): The type of model we want to retreive. Currently only 'simple' is supported.
    
    Output:
        keras model: A keras model instance
    """
    # Create model class
    model = ChessAIModel(learning_rate)
    return model.get_model(type_of_model)


def train_model(training_csv):
    """
    This is the big function that will train our neural network. 

    Argument:
        training_csv (filepath): The location of where our trainng fata is that we preprocessed
        in our data_handler.py file.
    """
    # HYPERPARAMETERS
    MODEL_TYPE = 'simple'
    NUM_EPOCHS = 100
    BATCH_SIZE = 16
    LEARNING_RATE = 0.01

    # Load in data
    X, Y = load_dataset(training_csv)

    print(X)
    return

    # Retrieve model
    model = get_model(MODEL_TYPE, LEARNING_RATE)

    # Train Model
    model.fit(
        x=X, 
        y=Y,
        epochs=NUM_EPOCHS,
        batch_size=BATCH_SIZE,
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_location', type=str)

    args = parser.parse_args()

    if not args.csv_location or (not os.path.isfile(args.csv_location)):
        print('ERROR - Did not provide a correct location to the training .csv file.')
        exit(-1)

    train_model(args.csv_location)