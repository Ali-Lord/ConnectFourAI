from enum import Enum
import math
from algorithms.minimax_alphabetapruning import minimax
import copy

# All the game states will be here.
class GameStates(Enum):
	REINITIALIZE = 1
	PLAYING = 2
	DISPLAY = 3
	EXITING = 7

# A player class that will hold necessary variables.
class Player:
	def __init__(self, is_ai):
		self.is_ai = is_ai

	def get_is_ai(self):
		return self.is_ai

# A class for the connect four board game.
class Game:
	def __init__(self, board, is_ai_first_player, is_ai_second_player):
		self.initialize_game(board, is_ai_first_player, is_ai_second_player)
	
	state = None # The current state of the game.
	board = None # The connect four board.
	
	# Players
	first_player = None
	second_player = None 

	# Setters
	def set_state(self, state):
		self.state = state
	
	def set_board(self, board):
		col_size = int(board[0])
		row_size = int(board[1])
		self.board = [[0]*col_size for i in range(row_size)]	

	# This setter returns the object.
	def set_player(self, is_ai):
		return Player(is_ai)
	
	# Getters
	def get_state(self):
		return self.state

	def get_board(self):
		return self.board

	def get_copy_board(self):
		return copy.deepcopy(self.board)

	def get_board_column_len(self):
		return len(self.board[0])

	def get_board_row_len(self):
		return len(self.board)

	def is_ai_first_player(self):
		return self.first_player.get_is_ai()
	
	def is_ai_second_player(self):
		return self.second_player.get_is_ai()

	# Updaters
	def update_board(self, board):
		self.board = board
	
	# Displays - Note: Temporary not used.
	def display_init(self):
		user_input = input("Is player 1 an AI?")
		
		# if the user input is not Y or N then we don't 
		while True:
			try:
				if user_input != "Y" or user_input != "N":
					raise Exception("Sorry, please input capital Y or N.")
				break
			except:
				print("Sorry, please input capital Y or N.")
	
	def display_splash(self):
		print("Connect Four")

	# When the game starts, we must assign something to the necessary variables.
	def initialize_game(self, board, is_ai_first_player, is_ai_second_player):		
		# Setting up the board.
		self.set_board(board) 
		
		# Setting up players.
		self.first_player = self.set_player(is_ai_first_player)
		self.second_player = self.set_player(is_ai_second_player)
		
		# Changing the game state.
		self.set_state(GameStates.PLAYING)


## Debugging
import tkinter as tk
from tkinter import messagebox, LEFT, RIGHT, simpledialog
from functools import partial
import PIL.Image
import PIL.ImageTk

import time # Temp
import random

def is_ai_prompt(is_player_one):
	player = 1

	if is_player_one != True:
		player = 2	
	
	# "Is player 'n' an AI?" prompt
	if messagebox.askyesno("Selections Screen", "Is player " + str(player) + " an AI?"):
		return True
	else:
		return False

def get_entry(hold, col, row):
	col = col.get()
	row = row.get()

	if col.isnumeric() and row.isnumeric():
		hold.append(col)
		hold.append(row)
		
		for widget in window.winfo_children():
			widget.destroy()
		
		window.quit()
	else:
		messagebox.showwarning("Warning!", "Please input integer only!")
	
def board_size_prompt(hold_col_row, input_box):
	input_box.geometry('280x100')	
	
	column_size = tk.StringVar()
	row_size = tk.StringVar()

	lbl_column = tk.Label(input_box, text="Number of columns: ", justify=tk.LEFT).grid(row=1, column=0)
	entry_column = tk.Entry(input_box, bd=5, textvariable=column_size).grid(row=1, column=2)
		
	lbl_row = tk.Label(input_box, text="Number of rows: ", justify=tk.LEFT).grid(row=2, column=0)
	entry_row = tk.Entry(input_box, bd=5, textvariable=row_size).grid(row=2, column=2)
	
	entry_partial = partial(get_entry, hold_col_row, column_size, row_size)
	enter_btn = tk.Button(input_box, text="Enter", command=entry_partial).grid(row=3, column=0)	

	input_box.mainloop()

def display_graphics(win, board):
	# Clearing widgets
	for widget in win.winfo_children():
		widget.destroy()
		
	# Black piece
	img = PIL.Image.open("assets/black_piece.png")
	black_photo = PIL.ImageTk.PhotoImage(img)
		
	# Green piece
	img = PIL.Image.open("assets/green_piece.png")
	green_photo = PIL.ImageTk.PhotoImage(img)

	# Red piece
	img = PIL.Image.open("assets/red_piece.png")
	red_photo = PIL.ImageTk.PhotoImage(img)

	'''
	lbl_piece = tk.Label(win, image=photo)
	lbl_piece.image = photo
	
	lbl_piece.place(x=50, y=50)
	'''
	current_position_left = 0
	current_position_top = 50
	skip_position = 50

	for row in board:
		for i in row:
			lbl_piece = None
			if i == 0:
				lbl_piece = tk.Label(win, image=black_photo)
				lbl_piece.image = black_photo
			elif i == 1:
				lbl_piece = tk.Label(win, image=green_photo)
				lbl_piece.image = green_photo
			elif i == 2:
				lbl_piece = tk.Label(win, image=red_photo)
				lbl_piece.image = red_photo

			current_position_left += skip_position
			lbl_piece.place(x=current_position_left, y=current_position_top)
		current_position_top += skip_position
		current_position_left = 0
	
	win.update_idletasks()
	win.update()

def request_column(is_player_one, col_len):
	# Which player?
	player_n = 2
	if is_player_one:
		player_n = 1
	
	column_n = simpledialog.askinteger("Player " + str(player_n) + "'s Column Selection", 'Which column do you want to pick? (1-' + str(game.get_board_column_len()) +')')
	
	while column_n > col_len or column_n < 0:
		messagebox.showinfo("Incorrect input", "Please input correct value.")
		column_n = simpledialog.askinteger("Player " + str(player_n) + "'s Column Selection", 'Which column do you want to pick? (1-' + str(game.get_board_column_len()) +')')

	return column_n

def set_column(board, is_first_player, column, row_len):
	player_n = 2	
	if is_first_player:
		player_n = 1
	
	new_board = []
	has_changed = False
	row_c = 0
	for row in reversed(board):
		row_c += 1
		new_row = row
		print(column)
		if has_changed == False and new_row[column] == 0:
			new_row[column] = player_n
			has_changed = True
		elif has_changed == False and new_row[column] != 0 and row_c == row_len:
			messagebox.showinfo("Sorry", "Please pick another column.")
			return -1
		
		new_board.append(new_row)
	new_board = new_board[::-1]
	return new_board

def check_win(board, row_len, col_len):
	last_piece = 0	
	# Row
	for row in board:
		row_c = 0
		for i in row:
			if last_piece != i:
				row_c = 0 # reset counter
			
			last_piece = i
			if i != 0:
				row_c += 1
			
			if row_c == 4:
				messagebox.showinfo("Winning Screen", "Player " + str(last_piece) + " won!")
				exit()
	
	# Column
	last_piece = 0
	transposed_board = [list(i) for i in zip(*board)]
	for col in transposed_board:
		col_c = 0
		for i in col:
			if last_piece != i:
				col_c = 0 # reset counter
			
			last_piece = i
			if i != 0:
				col_c += 1
			if col_c == 4:
				messagebox.showinfo("Winning Screen", "Player " + str(last_piece) + " won!")
				exit()

	# Diagonal
	last_piece = 0
	row_len -= 1
	col_len -= 1
	j = 0
	diagonal_c = 0
	for k in range(col_len+1):
		j = k
		for row in range(row_len, -1, -1):
			for i in range(row, -1, -1):
				if j > col_len:
					break
				if last_piece != board[i][j]:
					diagonal_c = 0
				last_piece = board[i][j]
				if board[i][j] != 0:
					diagonal_c += 1

				if diagonal_c == 4:
					messagebox.showinfo("Winning Screen", "Player " + str(last_piece) + " won!")
					exit()
			
				# End
				j += 1

			if j == col_len:
				break	
def on_closing(win):
	win.destroy()
	exit()
		
# Game start
window = tk.Tk(className=" Connect Four - AI Project") # When the game starts

# Values of the window height and width.
window_width = window.winfo_reqwidth()
window_height = window.winfo_reqheight()

# Half screen values (to center the window)
position_right = int(window.winfo_screenwidth()/2 - window_width/2)
position_down = int(window.winfo_screenheight()/2 - window_height/2)

# Position the window
window.attributes("-zoomed", True)
window.geometry("+{}+{}".format(position_right, position_down))

# Update instead of event loop.
on_closing = partial(on_closing, window)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.update_idletasks()
window.update()

# Asking whether or not the game is to be played.
if not messagebox.askyesno("Main Menu", "Do you want to play the game?"):
	exit()

# Splash screen
messagebox.showinfo("Welcome", "Welcome to the Connect Four board game!")

is_ai_first_player = is_ai_prompt(True)
is_ai_second_player = is_ai_prompt(False)
board_size = []
board_size_prompt(board_size, window)
game = Game(board_size, is_ai_first_player, is_ai_second_player)

while game.get_state() != GameStates.EXITING:
	if game.get_state() == GameStates.REINITIALIZE:
		messagebox.askquestion(title="Main Menu", message="Do you want to play the game?")
		
		# Splash screen
		messagebox.Message("Welcome", "Welcome to the Connect Four board game!")
		
		board_size = []
		board_size_prompt(board_size, window)
		is_ai_first_player = is_ai_prompt(True)
		is_ai_second_player = is_ai_prompt(False)
		
		game.initialize_game(board, is_ai_first_player, is_ai_second_player)

	if game.get_state() == GameStates.PLAYING:
		# For debugging purposes
		#game.update_board([[0,0,0,0,0,0,0,0],[0,0,0,0,0,1,1,0],[0,0,0,0,1,1,0,0],[0,0,0,1,1,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0]])
		# Player 1 turn
		print("Player 1")
		if game.is_ai_first_player():
			messagebox.showinfo("AI Turn", "Player 1 AI Turn (Minimax Alpha Beta Pruning Algorithm).")
			b = game.get_copy_board()
			column_n, minimax_score = minimax(b, 5, -math.inf, math.inf, True, 1, game.get_board_column_len(), game.get_board_row_len())
			#messagebox.showinfo("Debug", str(column_n) + str(type(column_n)))
			if column_n == None:
				column_n = random.randint(0, game.get_board_column_len() - 1)
			game.update_board(set_column(game.get_board(), True, column_n, game.get_board_row_len()))


		else:
			brd = -1
			while brd == -1:
				column_n = request_column(True, game.get_board_column_len())
				brd = set_column(game.get_board(), True, column_n - 1,  game.get_board_row_len())
			game.update_board(brd)
		
		display_graphics(window, game.get_board())		
		check_win(game.get_board(), game.get_board_row_len(), game.get_board_column_len())		
		# Player 2 turn
		print("Player 2")
		if game.is_ai_second_player():
			messagebox.showinfo("AI Turn", "Player 2 AI Turn (Minimax Alpha Beta Pruning Algorithm).")
			b = game.get_copy_board()
			column_n, minimax_score = minimax(b, 5, -math.inf, math.inf, True, 2, game.get_board_column_len(), game.get_board_row_len())
			#messagebox.showinfo("Debug", str(column_n) + str(type(column_n)))
			if column_n == None:
				column_n = random.randint(0, game.get_board_column_len() - 1)
			game.update_board(set_column(game.get_board(), False, column_n, game.get_board_row_len()))
		else:
			brd = -1
			while brd == -1:
				column_n = request_column(False, game.get_board_column_len())
				brd = set_column(game.get_board(), False, column_n - 1, game.get_board_row_len())
			game.update_board(brd)
		
		display_graphics(window, game.get_board())
		check_win(game.get_board(), game.get_board_row_len(), game.get_board_column_len())	
		# For debugging purpose
		#time.sleep(5)
		#exit() #temp
	#break # temp
