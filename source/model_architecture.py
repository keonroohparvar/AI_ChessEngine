"""
This is the file that contains the model implementation for the chess estimator agent. 
LINK: https://colab.research.google.com/drive/1smI2B7kiwzkr43TqnCYOpxocZlI0kPUh?usp=sharing
LINK2: https://towardsdatascience.com/train-your-own-chess-ai-66b9ca8d71e4

Author: Keon Roohparvar
Date: 10/30/22
"""

# Python Imports
import sys
import os
import tensorflow as tf
import numpy

class ChessAIModel:
    def __init__(self, num_epochs, batch_size, learning_rate):
        self.num_epochs = num_epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
    
    def get_model(self, model_type):
        """
        This will return a Tensorflow Neural Network Object that can be used to train, and its
        architecture will be defined by the model_type parameter.

        Input:
            model_type (string): The type of model we want from a list of defined options. Current
            supported options are:
                -> simple - This creates a simple model
        
        Output:
            model: A tensorflow neural network Model instance that is ready to be trained.
        """
        if model_type == 'simple':
            return self.get_simple_model()
        
        else:
            raise NotImplementedError
    
    def get_simple_model(self):
        """
        This function will return a simple Tesnorflow Model() object with the architecture defined below.
        """
        pass

