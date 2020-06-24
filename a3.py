# a3.py
from random import choice, randint
from copy import deepcopy

RANDOM_PLAYOUTS = 500

CHARACTERS = {
    0: " ",
    1: "x",
    2: "o"
}

class TicTacToe():

    def __init__(self, state=[0, 0, 0, 0, 0, 0, 0, 0, 0]):
        self.state = state
        self.possible_moves = self.get_moves()

    def get_moves(self):
        positions = []
        for i in range(9):
            if (self.state[i]) == 0:
                positions.append(i)
        
        return positions

    def print_tictactoe(self):
        def print_line(line):
            first  = line[0]
            second = line[1]
            third  = line[2]

            row = "| " + CHARACTERS[first] + " | " + CHARACTERS[second] + " | " + CHARACTERS[third] + " |"
            print (row)

        def print_separators():
            print (" ----------- ")

        print()
        print_separators()
        for i in [0, 3, 6]:
            print_line(self.state[i: i + 3])
            print_separators()
        print()

    def is_valid_move(self, position):
        return position in self.possible_moves

    def action(self, player, position):

        if (self.state[position] != 0):
            print ("\nERROR: Performed invalid action\n")
            self.print_tictactoe()
            print ("Move chosen: " + str(position))
            return 1

        self.state[position] = player
        self.possible_moves.remove(position)

        # self.print_tictactoe()
        return 0

    def check_victory(self):
        def triple_equality(positions):
            a = positions[0]
            b = positions[1]
            c = positions[2]
            if self.state[a] == self.state[b] == self.state[c]:
                return self.state[a]
            return 0

        to_check = [
            (0, 1, 2),
            (3, 4, 5), 
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7), 
            (2, 5, 8),
            (0, 4, 8), 
            (2, 4, 6)
        ]

        for tup in to_check:
            winner = triple_equality(tup)
            if winner != 0:
                return winner

        if 0 not in self.state:
            return 3
        return 0

    def rand_move(self):
        return choice(self.possible_moves)


def print_reference():
    def print_line(line):
        first  = str(line[0])
        second = str(line[1])
        third  = str(line[2])

        row = "| " + first + " | " + second + " | " + third + " |"
        print (row)

    def print_separators():
        print (" ----------- ")

    print("\nReference: ")
    print_separators()
    for i in [0, 3, 6]:
        print_line(list(range(i, i + 3)))
        print_separators()
    print()

def win_more_strategy(gamestate):
    if (gamestate == 2):
        return 2
    if (gamestate == 1):
        return -1
    return 0

def equal_weight_strategy(gamestate):
    if (gamestate == 2):
        return 1
    if (gamestate == 1):
        return -1
    return 0

def lose_less_strategy(gamestate):
    if (gamestate == 2):
        return 1
    if (gamestate == 1):
        return -2
    return 0

def random_playout(puzzle, starting_move, strategy):

    if starting_move not in puzzle.possible_moves:
        print ("ERROR: Playout starting move is invalid")
        return 1

    clone = deepcopy(puzzle)

    # print ("Starting move: " + str(starting_move))
    # Perform the starting move for the computer
    clone.action(2, starting_move)


    # Perform random moves for both playes until the game has ended
    gamestate = clone.check_victory()
    while (gamestate == 0):

        clone.action(1, clone.rand_move())

        gamestate = clone.check_victory()

        if (gamestate == 0):
            clone.action(2, clone.rand_move())
            gamestate = clone.check_victory()

    return strategy(gamestate)

def computer_turn(puzzle, strategy, playouts):
    results = {}

    moves = puzzle.possible_moves

    for move in moves:
        results[move] = 0

    print ("\nComputer is making its move...\n")

    for move in results:
        for i in range(playouts):
            results[move] += random_playout(puzzle, move, strategy)
        
    maximum = max(results.values())
    chosen_move = moves[0]
    for move in results:
        if results[move] == maximum:
            chosen_move = move
            break

    print ("Results after random playouts: "+ str(results))
    print ("The computer has chosen the move to space " + str(chosen_move))

    puzzle.action(2, chosen_move)

def introduction(starting_player):
    print ("\n\nWelcome to the game!\n")
    print ("You will be playing TicTacToe against an AI that I created. You will be the 'X' player.\n")
    print ("HOW TO PLAY:")
    print ("Each square has been assigned a number. When it is your turn, enter the number which you would like to place your X.")
    print ("There will be a reference square for you when it is your turn:")
    print_reference()

    if (starting_player == 1):
        print("You have randomly been chosen to play FIRST.\n") 
    else:
        print("You have randomly been chosen to play SECOND.\n") 
        
    input("Press 'Enter' when you are ready to begin\n")

def play_a_new_game():

    puzzle = TicTacToe()
    starting_player = randint(1, 2) # 1 = player, 2 = computer
    # starting_player = 2

    introduction(starting_player)

    # If the player goes first, choose the "lose less strategy"
    # If the computer goes first, choose the "win more strategy"
    strategy_dict = {
        1: lose_less_strategy,
        2: win_more_strategy,
        3: equal_weight_strategy
    }
    strategy = strategy_dict[starting_player]

    if (starting_player == 2):
        computer_turn(puzzle, strategy, RANDOM_PLAYOUTS)

    game_is_ended = 0
    while(game_is_ended == 0):

        print_reference()
        puzzle.print_tictactoe()
        print ("Possible moves: " + str(puzzle.possible_moves))
        move = int(input("Enter your move: "))

        while (puzzle.action(1, move) == 1):
            print ("Possible moves: " + str(puzzle.possible_moves))
            move = int(input("Enter your move: "))

        game_is_ended = puzzle.check_victory()
        if (game_is_ended == 0):
            computer_turn(puzzle, strategy, RANDOM_PLAYOUTS)
            game_is_ended = puzzle.check_victory()

    if (game_is_ended == 2):
        print ("\nThe Computer has won")
    elif (game_is_ended == 3):
        print ("\nThe game is tied")
    elif (game_is_ended == 1):
        print ("\nCongratulations, you won!")

    puzzle.print_tictactoe()

if __name__ == '__main__':
    play_a_new_game()