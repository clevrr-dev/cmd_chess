# Chess Board class
import shelve
from pieces import * #Piece, King, Queen, Rook, Bishop, Knight, Pawn

class Board:
    '''Chess board grid'''
    GRID = [[('a',8),('b',8),('c',8),('d',8),('e',8),('f',8),('g',8),('h',8)],
            [('a',7),('b',7),('c',7),('d',7),('e',7),('f',7),('g',7),('h',7)],
            [('a',6),('b',6),('c',6),('d',6),('e',6),('f',6),('g',6),('h',6)],
            [('a',5),('b',5),('c',5),('d',5),('e',5),('f',5),('g',5),('h',5)],
            [('a',4),('b',4),('c',4),('d',4),('e',4),('f',4),('g',4),('h',4)],
            [('a',3),('b',3),('c',3),('d',3),('e',3),('f',3),('g',3),('h',3)],
            [('a',2),('b',2),('c',2),('d',2),('e',2),('f',2),('g',2),('h',2)],
            [('a',1),('b',1),('c',1),('d',1),('e',1),('f',1),('g',1),('h',1)]]

    FILE = ['a','b','c','d','e','f','g','h']
    RANK = [1, 2, 3, 4, 5, 6, 7, 8]

    def __init__(self):
        # Initialize variables
        self.GRID = Board.GRID
        self.FILE = Board.FILE
        self.RANK = Board.RANK
        self.db_file = 'chessdb_file'

        # Create database file
        mod = __import__("dbm")
        chessdb = shelve.Shelf(mod.open(self.db_file, 'c'), writeback=True)
        chessdb.sync()
        chessdb.close()

    def get_from_db(self, db_file, object_key):
        # get object from a given database file
        mod = __import__("dbm")
        db = shelve.Shelf(mod.open(db_file, 'w'), writeback=True)
        
        got_object = db[object_key]
        db.close()

        return(got_object)

    def save_to_db(self, db_file, object_key, object_value):
        # save object to db file
        mod = __import__("dbm")
        db = shelve.Shelf(mod.open(db_file, 'c'), writeback=True)
        # Save to chess database
        db[str(object_key)] = object_value
        db.sync()
        db.close()

    def get_position_on_grid(self, pos=(0,0)):
        # Get position from grid
        file_dict = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}

        if pos == (0,0):
            return []

        else:
            file = pos[0]
            rank = pos[1]
            # (8 - rank) to get index of rank on GRID
            return [8-rank,file_dict[file]]

    def initialize_board(self):
        # Setup chess board with all pieces
        # Initialize squares under attack db file
        self.init_squares_under_attack_db()     
        
        # Initial positions for pieces
        black_init_positions = [('a',8),('b',8),('c',8),('d',8),
                                ('e',8),('f',8),('g',8),('h',8),
                                ('a',7),('b',7),('c',7),('d',7),
                                ('e',7),('f',7),('g',7),('h',7)]

        white_init_positions = [('a',1),('b',1),('c',1),('d',1),
                                ('e',1),('f',1),('g',1),('h',1),
                                ('a',2),('b',2),('c',2),('d',2),
                                ('e',2),('f',2),('g',2),('h',2)]
        grid = self.GRID

        for row in grid:
            for square in row:
                # Setup Black pieces
                if square in black_init_positions:
                    if square == ('a',8): grid[0][0] = Rook(square, 'black')
                    if square == ('b',8): grid[0][1] = Knight(square, 'black')
                    if square == ('c',8): grid[0][2] = Bishop(square, 'black')
                    if square == ('d',8): grid[0][3] = Queen(square, 'black')
                    if square == ('e',8): grid[0][4] = King(square, 'black')
                    if square == ('f',8): grid[0][5] = Bishop(square, 'black')
                    if square == ('g',8): grid[0][6] = Knight(square, 'black')
                    if square == ('h',8): grid[0][7] = Rook(square, 'black')
                    if square == ('a',7): grid[1][0] = Pawn(square, 'black')
                    if square == ('b',7): grid[1][1] = Pawn(square, 'black')
                    if square == ('c',7): grid[1][2] = Pawn(square, 'black')
                    if square == ('d',7): grid[1][3] = Pawn(square, 'black')
                    if square == ('e',7): grid[1][4] = Pawn(square, 'black')
                    if square == ('f',7): grid[1][5] = Pawn(square, 'black')
                    if square == ('g',7): grid[1][6] = Pawn(square, 'black')
                    if square == ('h',7): grid[1][7] = Pawn(square, 'black')

                # Setup White pieces
                if square in white_init_positions:
                    if square == ('a',1): grid[7][0] = Rook(square, 'white')
                    if square == ('b',1): grid[7][1] = Knight(square, 'white')
                    if square == ('c',1): grid[7][2] = Bishop(square, 'white')
                    if square == ('d',1): grid[7][3] = Queen(square, 'white')
                    if square == ('e',1): grid[7][4] = King(square, 'white')
                    if square == ('f',1): grid[7][5] = Bishop(square, 'white')
                    if square == ('g',1): grid[7][6] = Knight(square, 'white')
                    if square == ('h',1): grid[7][7] = Rook(square, 'white')
                    if square == ('a',2): grid[6][0] = Pawn(square, 'white')
                    if square == ('b',2): grid[6][1] = Pawn(square, 'white')
                    if square == ('c',2): grid[6][2] = Pawn(square, 'white')
                    if square == ('d',2): grid[6][3] = Pawn(square, 'white')
                    if square == ('e',2): grid[6][4] = Pawn(square, 'white')
                    if square == ('f',2): grid[6][5] = Pawn(square, 'white')
                    if square == ('g',2): grid[6][6] = Pawn(square, 'white')
                    if square == ('h',2): grid[6][7] = Pawn(square, 'white')

        self.update_positions(grid)

    def check_king(self):
        # check if King is in CHECK
        grid = self.get_from_db('chessdb_file', 'chess_grid')

        for row in grid:
                for square in row:
                    if not isinstance(square, tuple) and type(square) == King:
                        if square.check():
                            #print(f"{square} is in check")
                            return(1)

    # FIX: Too slow
    # BUG: check_king not working properly
    def move_piece(self, current_position, final_position):
        # Move piece from current_position to final_position

        # check if king is in CHECK
        if self.check_king():
            print("King is in check")
            # undo move
            return(0)

        # Access db
        grid = self.get_from_db(self.db_file, 'chess_grid')

        current_file = self.get_position_on_grid(pos=current_position)[0]
        current_rank = self.get_position_on_grid(pos=current_position)[1]

        final_file = self.get_position_on_grid(pos=final_position)[0]
        final_rank = self.get_position_on_grid(pos=final_position)[1]
        
        moved = False

        for row in grid:
            for square in row:
                if not isinstance(square, tuple):
                    #print(f"piece {square.position()}")
                    if square.position() == current_position and \
                                final_position in square.valid_moves():
                        # update piece position
                        grid[final_file][final_rank] = square
                        grid[current_file][current_rank] = square.position()
                        moved = True
                        square.update_piece_position(final_position, 
                                                     piece=square)
                        print(f"Piece moved to {final_position}")


        if moved == False:
            print("Illegal move")
            return(0)
        else:
            self.update_positions(grid)
            return(1)

    def capture_piece(self, current_position, final_position):
        # capture piece in final_position from current_position

        # check if king is in CHECK
        if self.check_king():
            print("King is in check")
            # undo move
            return(0)

        # Access db
        grid = self.get_from_db(self.db_file, 'chess_grid')

        current_file = self.get_position_on_grid(pos=current_position)[0]
        current_rank = self.get_position_on_grid(pos=current_position)[1]

        final_file = self.get_position_on_grid(pos=final_position)[0]
        final_rank = self.get_position_on_grid(pos=final_position)[1]
        
        captured = False

        for row in grid:
            for square in row:
                if not isinstance(square, tuple):
                    #print(f"piece {square.position()}")
                    if square.position() == current_position and \
                                final_position in square.valid_captures():
                        # update piece position
                        grid[final_file][final_rank] = square
                        grid[current_file][current_rank] = square.position()
                        captured = True
                        square.update_piece_position(final_position, 
                                                     piece=square)
                        print(f"Piece {final_position} captured.")

        if captured == False:
            print(f"Illegal Move")
            return(0)
        else:
            self.update_positions(grid)
            return(1)
            
    def update_positions(self, grid):
        # Update positions of pieces after every move
        # Save to chess database
        self.save_to_db(self.db_file, 'chess_grid', grid)

    def init_squares_under_attack_db(self):
        # Add to pos_list to list of 
        # squares under attack
        
        mod = __import__("dbm")
        db = shelve.Shelf(mod.open('white_squares', 'n'), writeback=True)
        # list index corresponds to each chess piece
        db['squares_under_attack'] = [[],[],[],[],[],[]]
        db.close()

        db = shelve.Shelf(mod.open('black_squares', 'n'), writeback=True)
        db['squares_under_attack'] = [[],[],[],[],[],[]]
        db.close()

    def draw_board(self):
        # Draw chess grid
        board_string = ''

        # Access db
        grid = self.get_from_db(self.db_file, 'chess_grid')

        down_d = "." * 58 # Seperator

        i = 1
        r_side_num = 7
        l_side_num = 8
        for row in grid:
            for square in row:
                # create checkered pattern
                if isinstance(square, Piece):
                    board_string += str(square) + "\t"
                else:
                    if i % 2 == 0 and l_side_num % 2 == 0:
                            board_string += "-\t"
                    else:
                        board_string += "*\t"

                # Add numbers after the end of every line
                if i % 8 == 0 and i != 64:
                    board_string += f'{l_side_num}\n\t\t\b{down_d}\
\n\t{r_side_num}\t\b'

                i += 1
            r_side_num -= 1
            l_side_num -= 1


        print("\n")
        print("\t\t\ba\tb\tc\td\te\tf\tg\th")
        print(f"\t\t\b{down_d}")
        print(f"\t8\t\b{board_string}1")
        print(f"\t\t\b{down_d}")
        print("\t\t\ba\tb\tc\td\te\tf\tg\th")
        print("\n")



if __name__ == '__main__':
    #
    chess_board = Board()

    # chess_board.initialize_board()
    # chess_board.move_piece(('b',1),('c',3))
    # chess_board.move_piece(('g',8),('f',6))
    #chess_board.capture_piece(('f',6),('h',5))

    #chess_board.capture_piece(('a',6),('b',7))

    #print(chess_board.get_position_on_grid(pos=('f',6)))
    chess_board.draw_board()