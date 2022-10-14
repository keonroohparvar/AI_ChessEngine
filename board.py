# this is the base code for the board and pieces


class King(): # add a paramter for color
    def __init__(self, name, value, moves_list, position, color):
        self.name = name
        self.value = value
        self.moves = moves_list
        self.position = position
        self.color = color

    def __repr__(self):
        return (self.name)

    def move(self, location):
        print("move the piece")


class Queen():
    def __init__(self, name, value, moves_list,  position, color):
        self.name = name
        self.value = value
        self.moves = moves_list
        self.position = position
        self.color = color

    def __repr__(self):
        return (self.name)

    def move(self, location):
        print("move the piece")
    def take(self, location):
        print("take a piece")


class Bishop():
    def __init__(self, name, value, moves_list,  position, color):
        self.name = name
        self.value = value
        self.moves = moves_list
        self.position = position
        self.color = color

    def __repr__(self):
        return (self.name)

    def move(self, location):
        print("move the piece")
    def take(self, location):
        print("take a piece")


class Knight():
    def __init__(self, name, value, moves_list,  position, color):
        self.name = name
        self.value = value
        self.moves = moves_list
        self.position = position
        self.color = color

    def __repr__(self):
        return (self.name)

    def move(self, location):
        print("move the piece")
    def take(self, location):
        print("take a piece")


class Rook():
    def __init__(self, name, value, moves_list,  position, color):
        self.name = name
        self.value = value
        self.moves = moves_list
        self.position = position
        self.color = color

    def __repr__(self):
        return (self.name)

    def move(self, location):
        print("move the piece")
    def take(self, location):
        print("take a piece")


class Pawn():
    def __init__(self, name, value, moves_list,  position, color):
        self.name = name
        self.value = value
        self.moves = moves_list
        self.position = position
        self.color = color

    def __repr__(self):
        return (self.name)

    def find_moves(self, board):
        moves_list = [] # output with list of all possible moves
        position = self.position # where the piece is will be places in position
        if (self.color == 1): # if the piece is white
            # check forward
            if (position[0] > 0 or position[1] <= 7):  # see if piece is on border
                if(board[position[0]+1][position[1]] == 0):  # check one space in front and see if empty
                    move = [position[0]+1, position[1]]
                    moves_list.append(move)



    def move(self, location):
        print("move the piece")
    def take(self, location):
        print("take a piece")


ChessBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]


def create_all_pieces():  # this function will create all the pieces in the game, and
    all_pieces = []
    # all minor and major black pieces
    BR1 = Rook("BlackRook1", 5, ["up", "down", "left", "right"], [0, 0], 2)
    BR2 = Rook("BlackRook2", 5, ["up", "down", "left", "right"], [0, 7], 2)
    BN1 = Knight("BlackKnight1", 3, ["makes an L"], [0, 1], 2)
    BN2 = Knight("BlackKnight2", 3, ["makes an L"], [0, 6], 2)
    BB1 = Bishop("BlackBishop1", 3, ["digaonals"], [0, 2], 2)
    BB2 = Bishop("BlackBishop2", 3, ["digaonals"], [0, 5], 2)
    BQ = Queen("BlackQueen", 9, ["up", "down", "left", "right", "diagonals"], [0, 3], 2)
    BK = King("BlackKing", 100, ["up", "down", "left", "right", "diagonals"], [0, 4], 2)

    # all black pawns
    BP1 = Pawn("BlackPawn1", 1, ["up", "diagonal"], [1, 0], 2)
    BP2 = Pawn("BlackPawn2", 1, ["up", "diagonal"], [1, 1], 2)
    BP3 = Pawn("BlackPawn3", 1, ["up", "diagonal"], [1, 2], 2)
    BP4 = Pawn("BlackPawn4", 1, ["up", "diagonal"], [1, 3], 2)
    BP5 = Pawn("BlackPawn5", 1, ["up", "diagonal"], [1, 4], 2)
    BP6 = Pawn("BlackPawn6", 1, ["up", "diagonal"], [1, 5], 2)
    BP7 = Pawn("BlackPawn7", 1, ["up", "diagonal"], [1, 6], 2)
    BP8 = Pawn("BlackPawn8", 1, ["up", "diagonal"], [1, 7], 2)

    black_pieces = [BR1, BR2, BN1, BN2, BB1, BB2, BQ, BK, BP1, BP2, BP3, BP4, BP5, BP6, BP7, BP8]
    all_pieces.extend(black_pieces)

    # all minor and major white pieces
    WR1 = Rook("WhiteRook1", 5, ["up", "down", "left", "right"], [7, 0], 1)
    WR2 = Rook("WhiteRook2", 5, ["up", "down", "left", "right"], [7, 7], 1)
    WN1 = Knight("WhiteKnight1", 3, ["makes an L"], [7, 1], 1)
    WN2 = Knight("WhiteKnight2", 3, ["makes an L"], [7, 6], 1)
    WB1 = Bishop("WhiteBishop1", 3, ["digaonals"], [7, 2], 1)
    WB2 = Bishop("WhiteBishop2", 3, ["digaonals"], [7, 5], 1)
    WQ = Queen("WhiteQueen", 9, ["up", "down", "left", "right", "diagonals"], [7, 3], 1)
    WK = King("WhiteKing", 100, ["up", "down", "left", "right", "diagonals"], [7, 4], 1)

    # all white pawns
    WP1 = Pawn("WhitePawn1", 1, ["up", "diagonal"], [6, 0], 1)
    WP2 = Pawn("WhitePawn2", 1, ["up", "diagonal"], [6, 1], 1)
    WP3 = Pawn("WhitePawn3", 1, ["up", "diagonal"], [6, 2], 1)
    WP4 = Pawn("WhitePawn4", 1, ["up", "diagonal"], [6, 3], 1)
    WP5 = Pawn("WhitePawn5", 1, ["up", "diagonal"], [6, 4], 1)
    WP6 = Pawn("WhitePawn6", 1, ["up", "diagonal"], [6, 5], 1)
    WP7 = Pawn("WhitePawn7", 1, ["up", "diagonal"], [6, 6], 1)
    WP8 = Pawn("WhitePawn8", 1, ["up", "diagonal"], [6, 7], 1)

    white_pieces = [WR1, WR2, WN1, WN2, WB1, WB2, WQ, WK, WP1, WP2, WP3, WP4, WP5, WP6, WP7, WP8]
    all_pieces.extend(white_pieces)
    return all_pieces


def populate_board(all_pieces, board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            for itr in range(len(all_pieces)):
                if all_pieces[itr].position == [i, j]:
                    board[i][j] = all_pieces[itr]

    for i in range(len(board)):
        print(board[i])


all_pieces = create_all_pieces()
populate_board(all_pieces, ChessBoard)

print(type(ChessBoard[6][0]))
print(ChessBoard[6][0].color)
print(ChessBoard[6][0].name)
print()

ChessBoard[6][0].find_moves
# WP1.find_moves()
