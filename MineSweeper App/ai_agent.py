import random
from minesweeper import Minesweeper

class MinesweeperAI:
    def __init__(self, game):
        self.game = game

    def get_neighbors(self, r, c):
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if (0 <= nr < self.game.rows and 0 <= nc < self.game.cols) and (dr != 0 or dc != 0):
                    neighbors.append((nr, nc))
        return neighbors

    def make_informed_move(self):
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                if not self.game.revealed[r][c]:
                    continue
                val = self.game.board[r][c]
                if val == 0 or val == 'B':
                    continue

                neighbors = self.get_neighbors(r, c)
                unrevealed = [(nr, nc) for (nr, nc) in neighbors if not self.game.revealed[nr][nc] and not self.game.flagged[nr][nc]]
                flagged = [(nr, nc) for (nr, nc) in neighbors if self.game.flagged[nr][nc]]

                if len(unrevealed) > 0 and len(unrevealed) + len(flagged) == val:
                    return 'flag', unrevealed[0]

                if len(flagged) == val and len(unrevealed) > 0:
                    return 'reveal', unrevealed[0]

        return None

    def make_random_move(self):
        options = []
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                if not self.game.revealed[r][c] and not self.game.flagged[r][c]:
                    options.append((r, c))
        if options:
            return 'reveal', random.choice(options)
        return None

def run_ai_game(rows=4, cols=4, bombs=4):
    game = Minesweeper(rows, cols, bombs)
    ai = MinesweeperAI(game)

    while True:
        game.display()
        move = ai.make_informed_move()
        if not move:
            move = ai.make_random_move()
            if not move:
                break  

        action, (r, c) = move
        print(f"AI {action}s: ({r}, {c})")

        if action == 'flag':
            if not game.revealed[r][c]:
                game.flagged[r][c] = True
            continue

        if game.flagged[r][c]:
            continue  

        if game.board[r][c] == 'B':
            print("\n💥 AI hit a mine! Game over.")
            game.revealed[r][c] = True
            game.display(show_all=True)
            return

        game.flood_reveal(r, c)

        if game.remaining == 0:
            print("\n🎉 AI cleared all safe cells! You win.")
            game.display(show_all=True)
            return

if __name__ == "__main__":
    run_ai_game()
