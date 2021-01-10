# Chess cli
# Gameplay
import sys
from board import Board
from pieces import *

# TODO: USE PRINT STATEMENTS TO DEBUG THIS...
# BUG: check_position not dynamic...

# Initialize Board class
board = Board()

def get_from_db(dbfile, object_key):
    # get object from a given database file
	mod = __import__("dbm")
	db = shelve.Shelf(mod.open(dbfile, 'w'), writeback=True)
        
	got_object = db[object_key]
	db.close()

	return(got_object)

def draw():
	# draw board
	board.draw_board()

def check_position(piece_color):
	# Access db
	grid = get_from_db('chessdb_file', 'chess_grid')

	# prevent moving of other player's piece
	if piece_color == 'white':
		white_piece = [piece.position() for row in grid for piece in row
									if not isinstance(piece, tuple)
									if piece.piece_color == 'white']
		return(white_piece)

	if piece_color == 'black':
		black_piece = [piece.position() for row in grid for piece in row
									if not isinstance(piece, tuple)
									if piece.piece_color == 'black']
		return(black_piece)

def move_piece(current_position, final_position):
	# move a given piece
	try:
		return(board.move_piece(current_position, final_position))
	except:
		return(0)

def capture_piece(current_position, final_position):
	# capture a given piece
	try:
		return(board.capture_piece(current_position, final_position))
	except:
		return(0)

def get_positions(move):
	# get positions from user input
	if "-" in move:
		# move piece
		split_move = move.split("-")
		action = 0 # direct to move method

	if "x" in move:
		# capture piece
		split_move = move.split("x")
		action = 1 # direct to capture method

	current = split_move[0]
	final 	= split_move[1]

	current_file = current[0]
	current_rank = int(current[1])
	current_position = (current_file, current_rank)

	final_file = final[0]
	final_rank = int(final[1])
	final_position = (final_file, final_rank)

	return [current_position, final_position, action]

def take_action(move, player):
	# Take action; move or capture piece

	# If invalid move format is entered don't process
	try:
		current_position = get_positions(move)[0]
		final_position	 = get_positions(move)[1]
		action = get_positions(move)[2]
	except:
		return(0)

	# check if position is valid

	# Prevent movement of other player's pieces
	if player == 'white':
		valid_positions = check_position('white') 
		if current_position not in valid_positions:
			return(0)
	if player == 'black':
		valid_positions = check_position('black')
		if current_position not in valid_positions:
			return(0)


	if action == 0:
		result = move_piece(current_position, final_position)

	if action == 1:
		result = capture_piece(current_position, final_position)

	return(result)

def main():
	# Start Here!
	print("Pieces are moved using Algebraic Notation.")
	print("e.g. to move whites pawn, use '(a2-a3)'.")
	print("to capture a piece, use '(a2xb3)'.")
	print("""
	Notes: don't use spaces in between;
	only white player can `exit` game... ENJOY!""")
	
	# continue from last game or not
	print("\nContinue from last game?")
	cont = input("[Y|N]: ")

	if cont.upper() == "Y":
		print("Previous game loaded...")
	else:
		print("Starting new game...")
		board.initialize_board()

	draw() # draw board

	player_turn = 'white' # for switching turns

	while True:
		# Start gameloop

		if player_turn == 'white':
			#print("white's turn")
			move = input("w: ")

			if move == "exit" and player_turn == 'white':
				print("Game saved")
				sys.exit(0) # Exit game

			move_result = take_action(move, player_turn)

			if move_result == True:
				player_turn = 'black' # change turn
				draw()
			else:
				print("Please enter a valid move.\n")
			
		if player_turn == 'black':
			#print("black's turn")
			move = input("b: ")

			if move == "exit" and player_turn == 'white':
				print("Game saved")
				sys.exit(0) # Exit game

			move_result = take_action(move, player_turn)

			if move_result == True:
				player_turn = 'white' # change turn
				draw()
			else:
				print("Please enter a valid move.\n")


if __name__ == '__main__':
	#
	main()