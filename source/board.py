"""
Our custom class that implements a board while building off of Python's Chess library.
"""

import chess
import chess.svg
import time
import os

class ChessBoard:
    def __init__(self):
        self.board = chess.Board()
        self.piece_dict = {
            'p': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'b': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'n': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'r': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            'q': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            'k': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            'P': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            'B': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            'N': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            'R': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            'Q': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            'K': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            '.': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        }
        self.img_location = ''

    def get_legal_moves(self):
        return self.board.legal_moves
    
    def print_board(self):
        pieces_from_fen = self.get_fen().split(' ')[0]
        board_strs = []
        for row in pieces_from_fen.split('/'):
            this_arr = []
            for c in row:
                if c.isnumeric():
                    this_arr = this_arr + ['-' for _ in range(int(c))]
                else:
                    this_arr.append(c)
            board_strs.append(" ".join(this_arr))
        
        print("\n".join(board_strs))

    def get_turn(self):
        if self.board.turn:
            return 'W'
        else:
            return 'B'

    
    def make_move(self, move):
        # if move_obj not in self.board.legal_moves:
        #     print('ERROR - Illegal Move.')
        #     return -1
        
        self.board.push_san(move)
        return 0
    
    def get_fen(self):
        return self.board.fen()
    
    def set_fen(self, fen):
        self.board.set_fen(fen)
    
    def is_in_checkmate(self):
        return self.board.is_checkmate()
    
    def game_is_done(self):
        if self.is_in_checkmate():
            return True, 'checkmate'
        if self.board.can_claim_draw():
            return True, 'draw'
        if self.board.is_fifty_moves():
            return True, 'fifty'
        if not any(self.get_legal_moves()):
            return True, 'stalemate'
        return False, None

    def get_validity(self):
        valid = self.board.is_valid()
        if not valid:
            print(f'ERROR - Board is not valid: {self.board.status()}')
            return False

        return valid

    
    def positional_encode(self):
        # print('Board position is: ' + self.board.fen())
        
        # Parse the fen notation 
        fen = self.get_fen()

        pieces, move, castles, en_passant, halfmove_clock, fullmove_num = fen.split(' ')

        # Parse pieces
        pieces_arr = []        
        rows = pieces.split('/')
        for row in rows:
            for spot in row:
                if spot.isdigit():
                    for _ in range(int(spot)):
                        pieces_arr.extend(self.piece_dict['.'])
                else:
                    pieces_arr.extend(self.piece_dict[spot])
        
        assert len(pieces_arr) == 12 * 8 * 8 # This is making sure our pieces array has a 12-length vector for every single spot
        
        # Parse Move
        move_arr = [1] if move == 'w' else [0]

        # Parse castles
        castles_arr = ['K' in castles, 'Q' in castles, 'k' in castles, 'q' in castles]
        for idx, bool in enumerate(castles_arr):
            if bool:
                castles_arr[idx] = 1
            else:
                castles_arr[idx] = 0
        
        # Parse en passant
        en_passant_arr = [0] if en_passant == '-' else [chess.parse_square(en_passant)]
    
        return pieces_arr + move_arr + castles_arr + en_passant_arr + [int(halfmove_clock)] + [int(fullmove_num)]




if __name__ == '__main__':
    board = ChessBoard()
    board.print_board()