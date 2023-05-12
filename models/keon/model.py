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
import numpy
import tensorflow as tf
from keras.layers import Input, Dense, Conv2D, Flatten, Concatenate, Reshape
from keras.optimizers import Adam
import numpy as np


class ChessAIModel:
    def __init__(self, learning_rate=1e-3):
        self.learning_rate = learning_rate
    
    def get_model(self, model_type='complex'):
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
        
        if model_type == 'conv':
            return self.get_conv_model()
        
        if model_type == 'complex':
            return self.get_complex_model()
        
        if model_type == 'just_board':
            return self.get_just_board_model()

        else:
            raise NotImplementedError
    
    def get_simple_model(self):
        """
        This function will return a simple Tesnorflow Model() object with the architecture defined below.
        """
        # Create Model
        model = tf.keras.models.Sequential()

        # Add Layer

        INPUT_SIZE = (72,)
        input_layer = Input(INPUT_SIZE)
        print('getting simple model :)')

        layer1 = Dense(2000, activation='relu')
        layer2 = Dense(1000, activation='relu')
        layer3 = Dense(1000, activation='relu')
        layer4 = Dense(500, activation='relu')
        layer5 = Dense(500, activation='relu')
        layer6 = Dense(500, activation='relu')
        layer7 = Dense(500, activation='relu')
        output_layer = Dense(1, activation='linear')

        # Connect all layers into model
        model.add(input_layer)
        model.add(layer1)
        model.add(layer2)
        model.add(layer3)
        model.add(layer4)
        model.add(layer5)
        model.add(layer6)
        model.add(layer7)
        model.add(output_layer)

        # Create optimizer
        opt = Adam(learning_rate=self.learning_rate)

        # Compile model
        model.compile(
            optimizer = opt,
            loss='mse',
            )

        return model

    def get_conv_model(self):
        """
        This function will return a conv. model Tesnorflow Model() object with the architecture defined below.
        """
        # Split tensor into board and other information
        INPUT_SIZE = (72,)
        inputs = Input(shape=INPUT_SIZE)
        print(f'inp shape: {inputs.shape}')

        board_tensor, non_board_tensor = inputs[:, :64], inputs[:, 64:]
        board_tensor = Reshape(np.array([-1,8,8,1]))(board_tensor)

        print(f'Board tensor shaope: {board_tensor.shape}')

        # Convolude on board data
        x = Conv2D(128, 3, padding='same')(board_tensor)
        x = Conv2D(256, 3, padding='same')(x)
        x = Flatten()(x)

        # Concat board convolution data and non_board tensors
        # board_and_non_board = tf.concat([x, non_board_tensor])
        board_and_non_board = Concatenate()([x, non_board_tensor])
        x = Dense(2000, activation='relu')(board_and_non_board)
        x = Dense(1000, activation='relu')(x)
        x = Dense(500, activation='relu')(x)
        x = Dense(500, activation='relu')(x)
        x = Dense(500, activation='relu')(x)
        outputs = Dense(1, activation='linear')(x)

        # Create optimizer
        opt = Adam(learning_rate=self.learning_rate)

        model = tf.keras.Model(inputs=inputs, outputs=outputs, name='keons_conv_model')

        # Compile model
        model.compile(
            optimizer = opt,
            loss='mse',
            )

        return model

    def get_complex_model(self, batch_size=1):
        """
        This function will return a simple Tesnorflow Model() object with the architecture defined below.
        """
        # Create Model
        model = tf.keras.models.Sequential()

        INPUT_SIZE = (776,)
        inputs = Input(shape=INPUT_SIZE)
        BATCH_SIZE = inputs.shape[0] or batch_size

        num_items_in_board = 12 * 8 * 8
        board_tensor, non_board_tensor = inputs[:, :num_items_in_board], inputs[:, num_items_in_board:]

        board_tensor_2d = Reshape(np.array([8, 8, 12]))(board_tensor)

        # Convolude on board data
        x = Conv2D(32, 5, padding='same', activation='relu')(board_tensor_2d)
        x = Conv2D(64, 5, padding='same', activation='relu')(x)
        x = Conv2D(128, 5, padding='same', activation='relu')(x)
        x = Flatten()(x)

        print(x.shape)

        # Have some dense layers on the non-board data
        non_board_neurons = Dense(64, activation='relu')(non_board_tensor)
        non_board_neurons = Dense(128, activation='relu')(non_board_neurons)
        non_board_neurons = Dense(256, activation='relu')(non_board_neurons)

        # add the output of convolutions and our non_board_tensor information together
        board_and_non_board = Concatenate()([x, non_board_neurons])

        # Normal Deep Network onwards
        x = Dense(512, activation='relu')(board_and_non_board)
        x = Dense(256, activation='relu')(x)
        x = Dense(128, activation='relu')(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(32, activation='relu')(x)
        outputs = Dense(1, activation='tanh')(x)

        model = tf.keras.Model(inputs=inputs, outputs=outputs)

        # Create optimizer
        opt = Adam(learning_rate=self.learning_rate)

        # Compile model
        model.compile(
            optimizer = opt,
            loss='mse',
            )

        return model

    def get_just_board_model(self, batch_size=1):
        """
        This function will return a simple Tesnorflow Model() object with the architecture defined below.
        """
        # Create Model
        model = tf.keras.models.Sequential()

        LEARNING_RATE = 1e-4
        self.learning_rate = LEARNING_RATE

        INPUT_SIZE = (776,)
        inputs = Input(shape=INPUT_SIZE)
        BATCH_SIZE = inputs.shape[0] or batch_size

        num_items_in_board = 12 * 8 * 8
        board_tensor, non_board_tensor = inputs[:, :num_items_in_board], inputs[:, num_items_in_board:]

        board_tensor_2d = Reshape(np.array([8, 8, 12]))(board_tensor)

        # Convolude on board data
        x = Conv2D(32, 5, padding='same', activation='relu')(board_tensor_2d)
        x = Conv2D(64, 5, padding='same', activation='relu')(x)
        x = Conv2D(128, 5, padding='same', activation='relu')(x)
        x = Flatten()(x)

        # Normal Deep Network onwards
        x = Dense(512, activation='relu')(x)
        x = Dense(256, activation='relu')(x)
        x = Dense(128, activation='relu')(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(32, activation='relu')(x)
        outputs = Dense(1, activation='tanh')(x)

        model = tf.keras.Model(inputs=inputs, outputs=outputs)

        # Create optimizer
        opt = Adam(learning_rate=self.learning_rate)

        # Compile model
        model.compile(
            optimizer = opt,
            loss='mae',
            )

        return model



