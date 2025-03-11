import sys
 sys.path.append(r"C:\Users\tahse\Minesweeper\.spyproject\pysweeper")  # Adjust accordingly
 
 import Pysweeper
 
 
 # Settings
 setup_grid_x = 4
 setup_grid_y = 4
 setup_mine_count = 4
 setup_reveal_all = False
 setup_flag_all = True
 
 visuals_tile_hidden = "■"
 visuals_tile_flagged = "⚑"
 visuals_tile_mine = "☄"
 visuals_tile_empty = "□"
 
 # Global variables.
 tiles_revealed = 0
 game_state = Pysweeper.reveal_outcome.none
 
 
 def reveal_tile(index):
     # Hook the global variables.
     global minesweep
 
     # Reveal the tile.
     state = minesweep.try_reveal_tile(index)
 
     # If the tile was revealed.
     if (state == Pysweeper.reveal_outcome.reveal):
         
         # Check if the tile has any adjacent mines.
         if minesweep.info_adjacent_mines(index) == 0:
             
             # Get the adjacent tiles.
             adjacent_tiles = minesweep.info_adjacent_tiles(index)
 
             # Reveal all adjacent tiles.
             for tile in adjacent_tiles:
                 if not minesweep.info_tile_is_revealed(tile):
                     reveal_tile(tile)
     
     return state
 
 def setup_game():
     # Hook the global variables.
     global minesweep
     global tiles_revealed
     global game_state
     global visuals_tile_hidden
     global visuals_tile_flagged
     global visuals_tile_mine
     global visuals_tile_empty
 
     # Setup the game.
     tiles_revealed = 0
     game_state = Pysweeper.reveal_outcome.none
     minesweep.setup_game(setup_grid_x, setup_grid_y, setup_mine_count, setup_reveal_all, setup_flag_all)
     minesweep.set_visuals(visuals_tile_hidden, visuals_tile_flagged, visuals_tile_mine, visuals_tile_empty)
 
 def play_round():
     # Hook the global variables.
     global minesweep
     global tiles_revealed
     global game_state
     global setup_grid_x
     global setup_grid_y
     global setup_mine_count
 
     # Setup the game.
     setup_game()
 
     # Start the game loop.
     while game_state != Pysweeper.reveal_outcome.won and game_state != Pysweeper.reveal_outcome.lost:
         # Loop until the user enters a valid input
         while True:
             # Print the grid with X and Y coordinates.
             print(minesweep.text_grid())
 
             try:
                 # Take the user action.
                 action = input("Enter action [r: reveal, f: flag]: ")
                 if action != "r" and action != "f":
                     print("Invalid input.")
                     continue
 
                 # Take X input.
                 x = int(input("Enter x [1, {}]: ".format(setup_grid_x))) - 1
                 if x < 0 or x > setup_grid_x:
                     print("Invalid input.")
                     continue
 
                 # Take Y input.
                 y = int(input("Enter y [1, {}]: ".format(setup_grid_y))) - 1
                 if y < 0 or y > setup_grid_y:
                     print("Invalid input.")
                     continue
 
                 coordinate = x + y * setup_grid_x
 
                 # Perform the action.
 
                 # Reveal.
                 if (action == "r"):
                     # Reveal the tile and track the outcome.
                     game_state = reveal_tile(coordinate)
                     if (game_state == Pysweeper.reveal_outcome.reveal):
                         tiles_revealed += 1
 
                     # Check if the player would've lost immediately, and reset the game if so.
                     while (tiles_revealed == 0 and game_state == Pysweeper.reveal_outcome.lost):
                         setup_game()
                         game_state = reveal_tile(coordinate)
 
                 # Flag.
                 if (action == "f"):
                     # Check if the tile is revealed.
                     if (minesweep.info_tile_is_revealed(coordinate)):
                         print("You can't flag a revealed tile.")
                         continue
 
                     # Flag/unflag the tile.
                     if (minesweep.info_tile_is_flagged(coordinate)):
                         minesweep.unflag_tile(coordinate)
                     else:
                         minesweep.flag_tile(coordinate)
                 break
             except:
                 continue
 
     # Check the win/loss state.
     if game_state == Pysweeper.reveal_outcome.won:
         print("You won!")
     else:
         print("You lost!")
 
 # Game Setup.
 minesweep = Pysweeper.minesweeper()
 
 while True:
     play_round()
     if input("Play again? (y/n): ") != "y":
         break
     # Clear the console.
     print("\n" * 100)
