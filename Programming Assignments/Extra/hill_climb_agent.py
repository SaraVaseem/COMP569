import sys
import random

sys.path.append(r"C:\Users\tahse\Minesweeper\.spyproject\pysweeper")  # Adjust accordingly
import Pysweeper

# Game settings
setup_grid_x = 16
setup_grid_y = 16
setup_mine_count = 80

visuals_tile_hidden = "■"
visuals_tile_flagged = "⚑"
visuals_tile_mine = "☄"
visuals_tile_empty = "□"

def fitness_tile(index, minesweep):
    """Estimate how safe a tile is based on neighbors."""
    neighbors = minesweep.info_adjacent_tiles(index)
    known = [n for n in neighbors if minesweep.info_tile_is_revealed(n)]
    score = 0
    for n in known:
        adjacent_mines = minesweep.info_adjacent_mines(n)
        score += adjacent_mines
    return score  # Lower is better (fewer mines nearby)

def get_best_move(minesweep):
    """Return the index of the safest tile to reveal."""
    hidden_tiles = [
        i for i in range(setup_grid_x * setup_grid_y)
        if not minesweep.info_tile_is_revealed(i) and not minesweep.info_tile_is_flagged(i)
    ]

    if not hidden_tiles:
        return None

    # Score all hidden tiles based on heuristic
    scored_tiles = [(fitness_tile(i, minesweep), i) for i in hidden_tiles]
    scored_tiles.sort()  # Lower score = safer

    return scored_tiles[0][1]  # Return safest

def run_hill_climb_game():
    minesweep = Pysweeper.minesweeper()
    minesweep.setup_game(setup_grid_x, setup_grid_y, setup_mine_count, False, True)
    minesweep.set_visuals(visuals_tile_hidden, visuals_tile_flagged, visuals_tile_mine, visuals_tile_empty)

    state = Pysweeper.reveal_outcome.none

    while state != Pysweeper.reveal_outcome.won and state != Pysweeper.reveal_outcome.lost:
        move = get_best_move(minesweep)

        if move is None:
            print("No more moves.")
            break

        state = minesweep.try_reveal_tile(move)
        # print(minesweep.text_grid())

    if state == Pysweeper.reveal_outcome.won:
        print("AI won the game!")
    else:
        print("AI lost the game.")

def test_accuracy(num_games=100):
    wins = 0
    for _ in range(num_games):
        minesweep = Pysweeper.minesweeper()
        minesweep.setup_game(setup_grid_x, setup_grid_y, setup_mine_count, False, True)
        minesweep.set_visuals("■", "F", "*", ".")

        state = Pysweeper.reveal_outcome.none

        while state != Pysweeper.reveal_outcome.won and state != Pysweeper.reveal_outcome.lost:
            move = get_best_move(minesweep)
            if move is None:
                break
            state = minesweep.try_reveal_tile(move)

        if state == Pysweeper.reveal_outcome.won:
            wins += 1
        elif state == Pysweeper.reveal_outcome.lost:
            print("Game lost.")
        else:
            print("Game ended without a win or loss.")

        revealed_tiles = sum(
            1 for i in range(setup_grid_x * setup_grid_y)
            if minesweep.info_tile_is_revealed(i)
        )
        total_tiles = setup_grid_x * setup_grid_y
        non_mine_tiles = total_tiles - setup_mine_count

        print(f"Revealed: {revealed_tiles}/{non_mine_tiles}")


    print(f"AI won {wins} out of {num_games} games ({wins / num_games * 100:.2f}%)")

if __name__ == "__main__":
    run_hill_climb_game()
    test_accuracy(100)  # 100 runs 

