# COMP 569 - Artificial Intelligence
# Spring 2025
# Group Programming Assignment 3 - Tic Tac Toe
# Group 4: Nicholas Rodriguez Weda, Sarah Vaseem, Tanner Good, Moeeza Nazir, Tamim Sweedan, Luis Olmos


# GLOBAL VARS
# Can change the shape which player has
HUMAN = 'X'
AI    = 'O'
EMPTY = ' '

############################################################
# -----Helper Functions-----
############################################################

# Print the tic-tac-toe board, with the board key
def print_board(cells, with_key=False):

    n = int(len(cells) ** 0.5)
    if n * n != len(cells):
        raise ValueError("cells length must be a perfect square")
    
    # Add proper spacing to cells
    cell_width = 3
    sep = ('-' * cell_width + '+') * (n - 1) + '-' * cell_width

    # Create the board Key
    if with_key:
        layout = [str(i + 1) for i in range(n * n)]

    # Print the board(s)
    for r in range(n): # each row
        # Build the main board
        board_row = '|'.join(f"{cells[r*n + c]:^{cell_width}}" for c in range(n))

        # Build the board Key
        if with_key:
            key_row = '|'.join(f"{layout[r*n + c]:^{cell_width}}" for c in range(n))
            print(f"{board_row}         {key_row}") # 9 spaces       
        else:
            print(board_row) # Only print the board

        # Seperator for the board and the board key
        if r < n - 1:
            if with_key:
                print(f"{sep}         {sep}") # 9 spaces
            else:
                print(sep)
    print()

# Return the board positions that are empty
def available_moves(cells):
    return [i for i, v in enumerate(cells) if v == EMPTY]

# Check if there is a winning line from a player
def check_win(cells, player):
    lines = [
        (0,1,2), (3,4,5), (6,7,8),  # horizontal wins
        (0,3,6), (1,4,7), (2,5,8),  # vertical wins
        (0,4,8), (2,4,6)            # diagonal wins
    ]
    return any(all(cells[i] == player for i in line) for line in lines)


############################################################
# -----Algorithm-----
############################################################

# Mini Max Search Algorithm
def minimax(cells, maximizing):

    # Base Cases - already won or draw
    if check_win(cells, AI):
        return 1
    if check_win(cells, HUMAN):
        return -1
    if not available_moves(cells):
        return 0

    if maximizing:
        best = -float('inf')

        # Try all moves
        for index in available_moves(cells):
            cells[index] = AI # make the move
            score = minimax(cells, False) # recursive call
            cells[index] = EMPTY # undo the move
            best = max(best, score) # take the highest score
        return best
    else: # minimizing
        best = float('inf')
        for index in available_moves(cells):
            cells[index] = HUMAN
            score = minimax(cells, True) # recursive call
            cells[index] = EMPTY
            best = min(best, score) # take the lowest score
        return best

# AI's Turn (Agent) - Call MiniMax
def choose_move(cells):
    best_score = -float('inf')
    choice = None

    for index in available_moves(cells):
        # Try the Move
        cells[index] = AI
        score = minimax(cells, False)

        # Undo the Move
        cells[index] = EMPTY

        # If the move is better
        if score > best_score:
            best_score = score
            choice = index

    return choice # The best move

# Huma's Turn (Adversary) - Collect input from the user and add to game board
def human_turn(cells):
    while True:
        try:
            sel = int(input('Your move (1–9): ')) - 1
            if sel in available_moves(cells):
                cells[sel] = HUMAN
                return
            print('That spot is taken or out of range.')
        except ValueError:
            print('Enter a number from 1 to 9.')

############################################################
# -----Tests-----
############################################################

def run_tests():
    
    # (board_state, expected_move, description)
    test_boards = [   
        
        ([EMPTY,EMPTY,EMPTY,
          EMPTY,HUMAN,EMPTY,
          EMPTY,EMPTY,EMPTY],            0, "Human at 5                 : Should take corner at 1  "),
        
        ([HUMAN,HUMAN,EMPTY,
          EMPTY,EMPTY,EMPTY,
          EMPTY,EMPTY,EMPTY],            2, "Human at 1 & 2             : Should block at 3        "),
        
        ([AI   , AI   , EMPTY,
          EMPTY, HUMAN, EMPTY,
          EMPTY, HUMAN, EMPTY],          2, "AI at 1 & 2                : Should complete win at 3 "),
        
        ([HUMAN, EMPTY, EMPTY,
          EMPTY, AI   , EMPTY,
          EMPTY, EMPTY, HUMAN],          1, "Human Fork threat at 1 & 9 : Should block on side at 2"),
        
        ([HUMAN,AI   ,HUMAN,
          HUMAN,AI   ,HUMAN,
          AI   ,HUMAN,EMPTY],               8, "One empty spot             : Should take it to draw   ")
    ]

    print("\nRunning tests:")
    for i, (board, expected, desc) in enumerate(test_boards, start=1):
        test_board = board.copy() # fresh board

        # AI makes the move
        move = choose_move(test_board)
        # Result
        status = "PASS" if move == expected else "FAIL"
        print(f" {i}. {desc:40s} ----------------------------- Result - [{status}]")
    print()

############################################################
# -----Main-----
############################################################

def main():

    # Tests
    run_tests()

    while True: # Game Loop
        # Define an empty board
        board = [EMPTY]*9

        # Print the board key to guide user input
        print('\n-Board Key-')
        print_board([str(i+1) for i in range(9)])

        # Who starts first
        current = HUMAN

        while True:
            # Playing the Game

            # Human's Turn
            if current == HUMAN:
                human_turn(board)
            else: # AI's Turn
                move = choose_move(board)
                board[move] = AI # Place the symbol on the board
                print(f'Computer moves to {move+1}')

            # Print the board
            print_board(board, with_key=True)

            # Determine if the game was won
            if check_win(board, current):
                print(f'{current} wins')
                break
            # Check if the game is a draw
            if not available_moves(board):
                print('Game ends in a draw')
                break
            # Swap Player
            current = AI if current == HUMAN else HUMAN
        
        # Play again?
        while True:
            response = input("Play again? (Y/n): ")

            # Handle Yes
            if response in ('', 'y', 'Y', ' '): # including enter key
                break      # restart outer loop (new game)
            # Handle No
            if response in ('n', 'N'):
                print("Good Game!")
                return     # exit the program
            # Wrong Character
            print("Please enter 'Y' or 'n'.")

if __name__ == '__main__':
    main()