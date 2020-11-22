import math
import random

# Minimax Alpha Beta Pruning algorithm
def check_valid_index(board, column, row_len):
	return board[row_len-1][column] == 0 # Check if the index is 0.

def get_possible_indexes(board, col_len, row_len):
	possible_indexes = []
	for i in range(col_len):
		if check_valid_index(board, i, row_len):
			possible_indexes.append(i)
	return possible_indexes

def get_open_row(board, col, row_len):
	for i in range(row_len):
		if board[i][col] == 0:
			return i

def win_action(board, piece, col_len, row_len):
	# Row
	for col in range(col_len-3):
		for row in range(row_len):
			if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
				return True
	# Column
	for col in range(col_len):
		for row in range(row_len-3):
			if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
				return True
	# Diagonal positive
	for col in range(col_len-3):
		for row in range(row_len-3):
			if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
				return True
	# Diagonal negative
	for col in range(col_len-3):
		for row in range(3, row_len):
			if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
				return True


def minimax(b, depth, alpha, beta, is_maximizing_player, minimax_piece, col_len, row_len):
	board = b[:]
	player_piece = 1
	if minimax_piece == 1:
		player_piece = 2

	possible_indexes = get_possible_indexes(board, col_len, row_len)
	# is it the leaf node?
	is_leaf = win_action(board, player_piece, col_len, row_len) or win_action(board, minimax_piece, col_len, row_len) or len(get_possible_indexes(board, col_len, row_len)) == 0
	if depth == 0 or is_leaf:
		if is_leaf:
			if win_action(board, minimax_piece, col_len, row_len):
				return (None, 1000000000)
			elif win_action(board, player_piece, col_len, row_len):
				return (None, -1000000000)
			else:
				return (None, 0) # Game's over.
		else: 
			return (None, score_index(board, minimax_piece)) # there's no depth

	if is_maximizing_player:
		val = -math.inf
		col_choice = random.choice(possible_indexes)
		
		for col in possible_indexes:
			row = get_open_row(board, col, row_len)
			duplicated_board = board.copy()
			
			duplicated_board[row][col] = player_piece
			new_score = minimax(duplicated_board, depth-1, alpha, beta, False, minimax_piece, col_len, row_len)[1]
			if new_score > val:
				val = new_score
				col_choice = col
			alpha = max(alpha, val)
			if alpha >= beta:
				break
		return col_choice, val
	else:
		# minimazing. (obviously)
		val = math.inf
		col_choice = random.choice(possible_indexes)
		
		for col in possible_indexes:
			row = get_open_row(board, col, row_len)
			duplicated_board = board.copy()
			
			duplicated_board[row][col] = player_piece
			new_score = minimax(duplicated_board, depth-1, alpha, beta, True, minimax_piece, col_len, row_len)[1]
			if new_score < val:
				val = new_score
				col_choice = col
			alpha = min(beta, val)
			if alpha >= beta:
				break
		return col_choice, val

