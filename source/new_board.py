"""
This is NOT our implementation of a chess board, but rather using the Python API 'Chess'.
"""

import chess

class ChessBoard:
    def __init__(self):
        self.board = chess.Board()
        self.piece_dict = {
            'r': 1,
            'n': 2,
            'b': 3,
            'q': 4,
            'k': 5,
            'p': 6,
            'R': 7,
            'N': 8,
            'B': 9,
            'Q': 10,
            'K': 11,
            'P': 12
        }
    
    def make_move(self, move):
        # if move_obj not in self.board.legal_moves:
        #     print('ERROR - Illegal Move.')
        #     return -1
        
        self.board.push_san(move)
        return 0
    
    def positional_encode(self):
        # print('Board position is: ' + self.board.fen())
        
        # Parse the fen notation 
        fen = self.board.fen()

        pieces, move, castles, en_passant, halfmove_clock, fullmove_num = fen.split(' ')

        # Parse pieces
        pieces_arr = []        
        rows = pieces.split('/')
        for row in rows:
            for spot in row:
                if spot.isdigit():
                    pieces_arr.extend([0 for _ in range(int(spot))])
                else:
                    pieces_arr.append(self.piece_dict[spot])
        
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

        return pieces_arr + move_arr + castles_arr + move_arr + en_passant_arr + [int(halfmove_clock)] + [int(fullmove_num)]


    

if __name__ == '__main__':
    board = ChessBoard()
    print(board.positional_encode())
    print(len(board.positional_encode()))