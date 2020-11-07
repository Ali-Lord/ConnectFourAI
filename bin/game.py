# All the game states will be here.
class GameStates(Enum):
	REINITIALIZE = 1
	SPLASH = 2
	PAUSED = 3
	MENU = 4
	PLAYING = 5
	REPLAY = 6
	EXITING = 7

# A player class that will hold necessary variables.
class Player:
	def __init__(self, is_ai):
		self.is_ai = is_ai

# A class for the connect four board game.
class Game:
	def __init__(board, is_ai_first_player, is_ai_second_player):
		self.initialize_game(board, is_ai_first_player, is_ai_second_player)
	
	state = None # The current state of the game.
	board = None # The connect four board.
	
	# Players
	first_player = None
	second_player = None

	# Setters
	def set_state(state):
		self.state = state
	
	def set_board(board):
		self.board = board
	
	# This setter returns the object.
	def set_player(is_ai):
		return Player(is_ai)
	
	# Getters
	def get_state():
		return state
	
	# Displays
	def display_init():
		user_input = input("Is player 1 an AI?")
		
		# if the user input is not Y or N then we don't 
		if user_input != "Y" or user_input != "N":
			
	
	def display_splash():
		print("Connect Four")

	# When the game starts, we must assign something to the necessary variables.
	def initialize_game(board, is_ai_first_player, is_ai_second_player):
		# Setting up the board.
		self.set_board(board) 
		
		# Setting up players.
		self.first_player = self.set_player(is_ai_first_player)
		self.second_player = self.set_player(is_ai_second_player)

		# Changing the game state.
		self.set_state(GameStates.SPLASH)


## Debugging
game = Game(list[1:5], False, True)

while game.get_state() != GameStates.EXITING:
	if game.get_state() == GameStates.REINITIALIZE:
		game.display_splash()
		game.initialize_game(
