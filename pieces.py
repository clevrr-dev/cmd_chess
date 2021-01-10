# A chess cli program
# Objects
import shelve

# BUG: QUEEN, ROOK, and BISHOP valid_captures
#       not working well.
class Piece:
    '''Chess Piece'''
    def __init__(self, piece_position, piece_color):
        self.piece_position = piece_position
        self.piece_color = piece_color

        # name of piece position database file
        self.pos_db_file = f"{piece_color + str(self.__class__)}"
        # Create db file for piece position
        self.save_to_db(self.pos_db_file, self.piece_position, piece_position)

        self.FILE = ['a','b','c','d','e','f','g','h']
        self.RANK = [1, 2, 3, 4, 5, 6, 7, 8]

    def get_from_db(self, dbfile, object_key):
        # get object from a given database file
        mod = __import__("dbm")
        db = shelve.Shelf(mod.open(dbfile, 'w'), writeback=True)
        
        got_object = db[object_key]
        db.close()

        return(got_object)

    def save_to_db(self, dbfile, object_key, object_value):
        # save object to db file
        mod = __import__("dbm")
        db = shelve.Shelf(mod.open(dbfile, 'c'), writeback=True)
        # Save to chess database
        db[str(object_key)] = object_value
        db.sync()
        db.close()

    def position(self):
        # Position of piece
        position = self.get_from_db(self.pos_db_file, str(self.piece_position))
        return(position)

    def update_piece_position(self, final_position, piece=0):
        # update position of piece in db
        grid = self.get_from_db('chessdb_file', 'chess_grid')

        for row in grid:
            for square in row:
                if not isinstance(square, tuple):
                    if square.position() == self.position():
                        self.piece_position = square.position()
                        self.save_to_db(self.pos_db_file, 
                                        self.piece_position, final_position)

        # add piece valid moves to squares_under_attack
        if piece:
            self.squares_under_attack(piece)

    def get_num_limit(self):
        # get the num_limit for diagonal_movement()
        position = self.position()
        current_file = position[0]
        current_rank = position[1]

        file_dict = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        files = ['a','b','c','d','e','f','g','h']
        ranks = [1, 2, 3, 4, 5, 6, 7, 8]

        # Get the number of ranks and files to either sides
        # by slicing before and after the given rank and file
        ranks_above = ranks[(current_rank):]
        ranks_below = ranks[:(current_rank-1)][::-1] # reverse
        files_right = files[(file_dict[current_file]+1):]
        files_left  = files[:(file_dict[current_file])][::-1] # reverse

        # Use the direction with the least amount of squares 
        # as the limit for looping
        # diagonal movements
        if len(ranks_above) < len(files_right): 
            num_limit1 = len(ranks_above)
        else:
            num_limit1 = len(files_right)

        if len(ranks_above) < len(files_left):
            num_limit2 = len(ranks_above)
        else:
            num_limit2 = len(files_left)

        if len(ranks_below) < len(files_right):
            num_limit3 = len(ranks_below)
        else:
            num_limit3 = len(files_right)

        if len(ranks_below) < len(files_left):
            num_limit4 = len(ranks_below)
        else:
            num_limit4 = len(files_left)

        return([num_limit1, num_limit2, num_limit3, num_limit4])

    # TODO: don't add squares in occupied squares list
    def vertical_movement(self, limit=0):
        # vertical movements
        #grid = self.get_from_db('chessdb_file', 'chess_grid')
        #file_dict = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        files = ['a','b','c','d','e','f','g','h']
        ranks = [1, 2, 3, 4, 5, 6, 7, 8]

        position = self.position()
        current_file = position[0]
        current_rank = position[1]
        
        # Get the number of ranks and files to either sides
        # by slicing before and after the given rank and file
        ranks_above = ranks[(current_rank):]
        ranks_below = ranks[:(current_rank-1)][::-1] # reverse

        if limit:
            # up moves
            up_moves = [(current_file, ranks_above[i])
                            for i in range(len(ranks_above)) if i < limit]
            # down moves
            down_moves = [(current_file, ranks_below[i])
                            for i in range(len(ranks_below)) if i < limit]
        else:
            # up moves
            up_moves = [(current_file, ranks_above[i])
                            for i in range(len(ranks_above))]
            # down moves
            down_moves = [(current_file, ranks_below[i])
                            for i in range(len(ranks_below))]

        return([up_moves,down_moves])
    
    def horizontal_movement(self, limit=0):
        # horizontal movements
        file_dict = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        files = ['a','b','c','d','e','f','g','h']
        ranks = [1, 2, 3, 4, 5, 6, 7, 8]

        position = self.position()
        current_file = position[0]
        current_rank = position[1]
        
        # Get the number of files to either sides
        # by slicing before and after the given file
        files_right = files[(file_dict[current_file]+1):]
        files_left  = files[:(file_dict[current_file])][::-1] # reverse

        if limit:
            # right moves
            right_moves = [(files_right[i], current_rank)
                            for i in range(len(files_right)) if i < limit]
            # left moves
            left_moves = [(files_left[i], current_rank)
                            for i in range(len(files_left)) if i < limit]
        else: # if no limit
            # right moves
            right_moves = [(files_right[i], current_rank)
                            for i in range(len(files_right))]
            # down moves
            left_moves = [(files_left[i], current_rank)
                            for i in range(len(files_left))]

        return([right_moves,left_moves])

    # TODO: fix this mess!
    def diagonal_movement(self, limit=0):
        # diagonal movements of piece
        file_dict = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        files = ['a','b','c','d','e','f','g','h']
        ranks = [1, 2, 3, 4, 5, 6, 7, 8]

        position = self.position()
        current_file = position[0]
        current_rank = position[1]

        move_list = []

        # Get the number of ranks and files to either sides
        # by slicing before and after the given rank and file
        ranks_above = ranks[(current_rank):]
        ranks_below = ranks[:(current_rank-1)][::-1] # reverse
        files_right = files[(file_dict[current_file]+1):]
        files_left  = files[:(file_dict[current_file])][::-1] # reverse

        num_limit = self.get_num_limit()

        if limit:
            # top right squares
            top_right = [(files_right[i], ranks_above[i])
                            for i in range(num_limit[0]) if i < limit]
                            #if not (files_right[i], ranks_above[i]) in 
                            #    occupied_squares]
            # top left squares
            top_left = [(files_left[i], ranks_above[i])
                            for i in range(num_limit[1]) if i < limit]
                            #if not (files_left[i], ranks_above[i]) in 
                            #    occupied_squares]
            # bottom right squares
            bottom_right = [(files_right[i], ranks_below[i])
                                for i in range(num_limit[2]) if i < limit]
                            #    if not (files_right[i], ranks_below[i]) in 
                            #        occupied_squares]
            # bottom left squares
            bottom_left = [(files_left[i], ranks_below[i])
                                for i in range(num_limit[3]) if i < limit]
                            #    if not (files_right[i], ranks_below[i]) in 
                            #        occupied_squares]
        else:
            # top right squares
            top_right = [(files_right[i], ranks_above[i])
                            for i in range(num_limit[0])]
                            #if not (files_right[i], ranks_above[i]) in 
                            #    occupied_squares]
            # top left squares
            top_left = [(files_left[i], ranks_above[i])
                            for i in range(num_limit[1])]
                            #if not (files_left[i], ranks_above[i]) in 
                            #    occupied_squares]
            # bottom right squares
            bottom_right = [(files_right[i], ranks_below[i])
                                for i in range(num_limit[2])]
                            #    if not (files_right[i], ranks_below[i]) in 
                            #        occupied_squares]
            # bottom left squares
            bottom_left = [(files_left[i], ranks_below[i])
                                for i in range(num_limit[3])]
                                #if not (files_right[i], ranks_below[i]) in 
                                #    occupied_squares]

        #move_list = top_left + top_right + bottom_right + bottom_left
        return([top_left, top_right, bottom_right, bottom_left])

    def valid_moves(self):
        # valid piece movements
        grid = self.get_from_db('chessdb_file', 'chess_grid')
        # check if square is not occupied
        occupied_squares = [square.position() for row in grid for square in row
                            if not isinstance(square, tuple)]

        moves = self.available_moves()

        valid_moves_list = [pos for pos in moves if pos not in occupied_squares]
        
        # add to squares under attack
        #self.squares_under_attack(valid_moves_list)

        return(valid_moves_list)

    def valid_captures(self):
        # valid piece captures
        grid = self.get_from_db('chessdb_file', 'chess_grid')

        occupied_squares = [square.position() for row in grid for square in row
                            if not isinstance(square, tuple) 
                            if square.piece_color != self.piece_color]

        moves = self.available_moves()

        valid_captures_list = [pos for pos in moves if pos in occupied_squares]
        
        # add to squares under attack
        #self.squares_under_attack(valid_captures_list)

        return(valid_captures_list)

    def squares_under_attack(self, piece):
        # Add to pos_list to list of 
        # squares under attack
    
        if piece.piece_color == 'white':
            db_file = 'white_squares'    
        if piece.piece_color == 'black':
            db_file = 'black_squares'
        
        mod = __import__("dbm")
        db = shelve.Shelf(mod.open(db_file, 'w'), writeback=True)
        
        if type(piece) == Pawn:
            pos_list = piece.valid_captures()
        else:
            pos_list = piece.valid_moves() + piece.valid_captures()

        for pos in pos_list:
            if type(piece) == King: 
                db['squares_under_attack'][0] = pos_list
            if type(piece) == Queen:
                db['squares_under_attack'][1] = pos_list
            if type(piece) == Rook:
                db['squares_under_attack'][2] = pos_list
            if type(piece) == Bishop:
                db['squares_under_attack'][3] = pos_list
            if type(piece) == Knight:
                db['squares_under_attack'][4] = pos_list
            if type(piece) == Pawn:
                db['squares_under_attack'][5] = pos_list

        db.sync()
        db.close()


class King(Piece):
    '''King piece'''

    def __repr__(self):
        # Display piece
        if self.piece_color.upper() == 'WHITE':
            return '\033[33mK\033[0m'
        if self.piece_color.upper() == 'BLACK':
            return '\033[34mK\033[0m'

    # FIX: Takes too much time to run, look for a better way
    def get_squares_under_attack(self):
        # Get squares under attack by other pieces
        if self.piece_color == 'white':
            db_file = 'black_squares'

        if self.piece_color == 'black':
            db_file = 'white_squares'

        positions = self.get_from_db(db_file, 'squares_under_attack')

        squares_under_attack = [pos for row in positions for pos in row]

        return(squares_under_attack)

    def available_moves(self):
        # available piece movements

        # remove duplicate positions
        squares_under_attack = list(set(self.get_squares_under_attack()))

        vertical_moves = self.vertical_movement(limit=1)
        horizontal_moves = self.horizontal_movement(limit=1)
        diagonal_moves = self.diagonal_movement(limit=1)

        moves_list = vertical_moves + horizontal_moves + diagonal_moves

        moves = [pos for row in moves_list for pos in row
                        if pos not in squares_under_attack]

        return(moves)

    def check(self):
        # check if King is in CHECK
        grid = self.get_from_db('chessdb_file', 'chess_grid')
        # refresh squares_under_attack list
        # if piece has not been moved
        # for row in grid:
        #     for square in row:
        #         if not isinstance(square, tuple):
        #             if square.piece_color != self.piece_color and \
        #                     square.position() != square.piece_position:
        #                 self.update_piece_position(square.position(),
        #                                            piece=square)

        squares_under_attack = self.get_squares_under_attack()

        if self.position() in squares_under_attack:
            return(1)


class Queen(Piece):
    '''Queen Piece'''
    def __repr__(self):
        # Display piece
        if self.piece_color.upper() == 'WHITE':
            return '\033[33mQ\033[0m'
        if self.piece_color.upper() == 'BLACK':
            return '\033[34mQ\033[0m'

    def available_moves(self):
        # available piece movements
        grid = self.get_from_db('chessdb_file', 'chess_grid')
        # check if square is not occupied
        occupied_squares = [square.position() for row in grid for square in row
                            if isinstance(square, Piece)]

        vertical_moves = self.vertical_movement(limit=0)
        horizontal_moves = self.horizontal_movement(limit=0)
        diagonal_moves = self.diagonal_movement(limit=0)

        moves_list = [vertical_moves, horizontal_moves, diagonal_moves]
        #moves = [pos for row in moves_list for pos in row]

        return(moves_list)

    def valid_moves(self):
        # valid piece movements
        grid = self.get_from_db('chessdb_file', 'chess_grid')
        # check if square is not occupied
        occupied_squares = [square.position() for row in grid for square in row
                            if not isinstance(square, tuple)]

        moves = self.available_moves()

        valid_moves_list = []

        # break loop if square is occupied
        for move in moves[0]:
            for pos in move:
                if pos in occupied_squares:
                    break
                valid_moves_list.append(pos)

        for move in moves[1]:
            for pos in move:
                if pos in occupied_squares:
                    break
                valid_moves_list.append(pos)

        for move in moves[2]:
            for pos in move:
                if pos in occupied_squares:
                    break
                valid_moves_list.append(pos)

        # add to squares under attack
        #self.squares_under_attack(valid_moves_list)

        return(valid_moves_list)

    def valid_captures(self):
        # valid piece captures
        grid = self.get_from_db('chessdb_file', 'chess_grid')

        occupied_squares = [square.position() for row in grid for square in row
                            if not isinstance(square, tuple) 
                            if square.piece_color != self.piece_color]

        moves = self.available_moves()

        valid_capture_list = []

        # break loop if square is occupied
        for move in moves[0]:
            for pos in move:
                if pos in occupied_squares:
                    valid_capture_list.append(pos)
                    break

        for move in moves[1]:
            for pos in move:
                if pos in occupied_squares:
                    valid_capture_list.append(pos)
                    break

        for move in moves[2]:
            for pos in move:
                if pos in occupied_squares:
                    valid_capture_list.append(pos)
                    break

        # add to squares under attack
        #self.squares_under_attack(valid_capture_list)

        return(valid_capture_list)


class Rook(Piece):
    '''Rook Piece'''
    def __repr__(self):
        # Display piece
        if self.piece_color.upper() == 'WHITE':
            return '\033[33mR\033[0m'
        if self.piece_color.upper() == 'BLACK':
            return '\033[34mR\033[0m'

    def available_moves(self):
        # available piece movements
        grid = self.get_from_db('chessdb_file', 'chess_grid')
        # check if square is not occupied
        occupied_squares = [square.position() for row in grid for square in row
                            if isinstance(square, Piece)]

        vertical_moves = self.vertical_movement(limit=0)
        horizontal_moves = self.horizontal_movement(limit=0)

        moves_list = [vertical_moves, horizontal_moves]
        #moves = [pos for row in moves_list for pos in row]

        return(moves_list)

    def valid_moves(self):
        # valid piece movements
        grid = self.get_from_db('chessdb_file', 'chess_grid')
        # check if square is not occupied
        occupied_squares = [square.position() for row in grid for square in row
                            if not isinstance(square, tuple)]

        moves = self.available_moves()

        # valid_moves_list = [pos for pos in moves if pos not in occupied_squares]

        valid_moves_list = []

        # break loop if square is occupied
        for move in moves[0]:
            for pos in move:
                if pos in occupied_squares:
                    break
                valid_moves_list.append(pos)

        for move in moves[1]:
            for pos in move:
                if pos in occupied_squares:
                    break
                valid_moves_list.append(pos)

        # add to squares under attack
        #self.squares_under_attack(valid_moves_list)

        return(valid_moves_list)

    def valid_captures(self):
        # valid piece captures
        grid = self.get_from_db('chessdb_file', 'chess_grid')

        occupied_squares = [square.position() for row in grid for square in row
                            if not isinstance(square, tuple) 
                            if square.piece_color != self.piece_color]

        moves = self.available_moves()

        valid_capture_list = []

        # break loop if square is occupied
        for move in moves[0]:
            for pos in move:
                if pos in occupied_squares:
                    valid_capture_list.append(pos)
                    break

        for move in moves[1]:
            for pos in move:
                if pos in occupied_squares:
                    valid_capture_list.append(pos)
                    break

        # add to squares under attack
        #self.squares_under_attack(valid_capture_list)

        return(valid_capture_list)


class Bishop(Piece):
    '''Bishop Piece'''
    def __repr__(self):
        # Display piece
        if self.piece_color.upper() == 'WHITE':
            return '\033[33mB\033[0m'
        if self.piece_color.upper() == 'BLACK':
            return '\033[34mB\033[0m'

    def available_moves(self):
        # available piece movements
        grid = self.get_from_db('chessdb_file', 'chess_grid')
        # check if square is not occupied
        occupied_squares = [square.position() for row in grid for square in row
                            if isinstance(square, Piece)]

        diagonal_moves = self.diagonal_movement(limit=0)

        moves_list = [diagonal_moves]
        #moves = [pos for row in moves_list for pos in row]

        return(moves_list)

    def valid_moves(self):
        # valid piece movements
        grid = self.get_from_db('chessdb_file', 'chess_grid')
        # check if square is not occupied
        occupied_squares = [square.position() for row in grid for square in row
                            if not isinstance(square, tuple)]

        moves = self.available_moves()

        valid_moves_list = []

        # break loop if square is occupied
        for move in moves[0]:
            for pos in move:
                if pos in occupied_squares:
                    break
                valid_moves_list.append(pos)

        # add to squares under attack
        #self.squares_under_attack(valid_moves_list)

        return(valid_moves_list)

    def valid_captures(self):
        # valid piece captures
        grid = self.get_from_db('chessdb_file', 'chess_grid')

        occupied_squares = [square.position() for row in grid for square in row
                            if not isinstance(square, tuple) 
                            if square.piece_color != self.piece_color]

        moves = self.available_moves()

        valid_capture_list = []

        # break loop if square is occupied
        for move in moves[0]:
            for pos in move:
                if pos in occupied_squares:
                    valid_capture_list.append(pos)
                    break

        # add to squares under attack
        #self.squares_under_attack(valid_capture_list)

        return(valid_capture_list)


class Knight(Piece):
    '''Knight Piece'''
    def __repr__(self):
        # Display piece
        if self.piece_color.upper() == 'WHITE':
            return '\033[33mN\033[0m'
        if self.piece_color.upper() == 'BLACK':
            return '\033[34mN\033[0m'

    # TODO: clean up this mess
    def get_side_positions(self, position, sides):
        # use given position to get positions to either sides
        # of it
        file_dict = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        files = ['a','b','c','d','e','f','g','h']
        ranks = [1, 2, 3, 4, 5, 6, 7, 8]

        current_file = position[0]
        current_rank = position[1]

        if sides == 'l-r':
            # get the next files by slicing before and after it
            # and pick the first position
            if not file_dict[current_file] == 7:
                next_file_right = files[file_dict[current_file]+1:][0]
            else:
                next_file_right = 0
            
            if not file_dict[current_file] == 0:
                next_file_left  = files[:file_dict[current_file]][::-1][0]
            else:
                next_file_left = 0

            return ((next_file_right,current_rank),
                    (next_file_left,current_rank))

        if sides == 'u-d':
            # get the next ranks by slicing before and after it
            # and pick the first position
            if not current_rank == 8:
                next_rank_up = ranks[(current_rank-1)+1:][0]
            else:
                next_rank_up = 0

            if not current_rank == 1:
                next_rank_down = ranks[:(current_rank-1)][::-1][0]
            else:
                next_rank_down = 0

            return((current_file, next_rank_up),
                   (current_file, next_rank_down))

    def available_moves(self):
        # available knight piece moves
        
        up      = self.vertical_movement(limit=2)[0]
        down    = self.vertical_movement(limit=2)[1]
        right   = self.horizontal_movement(limit=2)[0]
        left    = self.horizontal_movement(limit=2)[1]

        moves_list = []

        # Use the last position (if it exists) to get the side positions
        # (l-r): left and right sides; (u-d): up and down sides
        if up:
            top_right, top_left = self.get_side_positions(up[::-1][0], 'l-r')
            moves_list.append(top_right)
            moves_list.append(top_left)
        #else:
        #    top_right, top_left = ((),())

        if down:
            bottom_right, bottom_left = self.get_side_positions(down[::-1][0], 'l-r')
            moves_list.append(bottom_right)
            moves_list.append(bottom_left)
        #else:
        #    bottom_right, bottom_left = ((),())

        if right:
            right_up, right_down = self.get_side_positions(right[::-1][0], 'u-d')
            moves_list.append(right_up)
            moves_list.append(right_down)
        # else:
        #     right_up, right_down = ((),())

        if left:
            left_up, left_down = self.get_side_positions(left[::-1][0], 'u-d')
            moves_list.append(left_up)
            moves_list.append(left_down)
        # else:
        #     left_up, left_down = ((),())

        # return([top_right, top_left, bottom_right, bottom_left,
        #         right_up, right_down, left_up, left_down])
        moves_list = [pos for pos in moves_list if 0 not in pos]

        return(moves_list)


class Pawn(Piece):
    '''Pawn Piece'''
    def __repr__(self):
        # Display piece
        if self.piece_color.upper() == 'WHITE':
            return '\033[33mP\033[0m'
        if self.piece_color.upper() == 'BLACK':
            return '\033[34mP\033[0m'

    # TODO: don't add move if square is occupied
    def available_moves(self):
        # valid moves of the pawn piece
        position = self.position()
        rank = position[1]

        if self.piece_color == 'white':
            # if first move
            if rank == 2:
                move = self.vertical_movement(limit=2)[0]
            else:
                move = self.vertical_movement(limit=1)[0]

        if self.piece_color == 'black':
            # if black piece
            # if first move
            if rank == 7:
                move = self.vertical_movement(limit=2)[1]
            else:
                move = self.vertical_movement(limit=1)[1]

        return(move)

    def valid_captures(self):
        # valid captures of the pawn piece
        grid = self.get_from_db('chessdb_file', 'chess_grid')

        occupied_squares = [square.position() for row in grid for square in row
                            if not isinstance(square, tuple) 
                            if square.piece_color != self.piece_color]

        # get diagonal captures
        captures = self.diagonal_movement(limit=1)

        top_left = captures[0]
        top_right = captures[1]
        bottom_left = captures[3]
        bottom_right = captures[2]

        if self.piece_color == 'white':
            top_left  = [pos for pos in top_left if pos in occupied_squares]
            top_right = [pos for pos in top_right if pos in occupied_squares]

            captures = [top_left, top_right]

            # add to squares under attack
            #self.squares_under_attack([pos for move in captures for pos in move])

            return([pos for move in captures for pos in move])
            
        if self.piece_color == 'black':
            bottom_right = [pos for pos in bottom_right if pos in occupied_squares]
            bottom_left  = [pos for pos in bottom_left if pos in occupied_squares]

            captures = [bottom_right, bottom_left]
            
            # add to squares under attack
            #self.squares_under_attack([pos for move in captures for pos in move])

            return([pos for move in captures for pos in move])

    def promote(self, new_piece):
        # promote pawn piece
        pass


if __name__ == '__main__':
    #
    joe = King(('e',8), 'black')
    print(f'vertical: {joe.vertical_movement(limit=0)}')
    print(f'horizontal: {joe.horizontal_movement(limit=0)}')
    print(f'diagonal: {joe.diagonal_movement(limit=0)}')
    #joe.horizontal_movement(limit=0)
    #print(joe.get_squares_under_attack())