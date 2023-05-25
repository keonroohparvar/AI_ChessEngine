# importing required librarys
import pygame
import chess
import math


#initialise display
X = 800
Y = 800
scrn = pygame.display.set_mode((X, Y))
pygame.init()

#basic colours
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

#initialise chess board
b = chess.Board()

#load piece images
pieces = {'p': pygame.image.load('b_pawn.png').convert(),
          'n': pygame.image.load('b_knight.png').convert(),
          'b': pygame.image.load('b_bishop.png').convert(),
          'r': pygame.image.load('b_rook.png').convert(),
          'q': pygame.image.load('b_queen.png').convert(),
          'k': pygame.image.load('b_king.png').convert(),
          'P': pygame.image.load('w_pawn.png').convert(),
          'N': pygame.image.load('w_knight.png').convert(),
          'B': pygame.image.load('w_bishop.png').convert(),
          'R': pygame.image.load('w_rook.png').convert(),
          'Q': pygame.image.load('w_queen.png').convert(),
          'K': pygame.image.load('w_king.png').convert(),
          
          }