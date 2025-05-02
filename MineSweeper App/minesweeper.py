#!/usr/bin/env python3
import random
import sys

class Minesweeper:
    def __init__(self, rows=9, cols=9, bombs=10):
        self.rows = rows
        self.cols = cols
        self.bombs = bombs
        self._place_bombs()
        self._calc_adjacency()
        self.revealed = [[False]*cols for _ in range(rows)]
        self.flagged  = [[False]*cols for _ in range(rows)]
        self.remaining = rows*cols - bombs

    def _place_bombs(self):
        self.board = [[0]*self.cols for _ in range(self.rows)]
        # randomly choose bomb locations
        spots = list(range(self.rows * self.cols))
        random.shuffle(spots)
        for idx in spots[:self.bombs]:
            r, c = divmod(idx, self.cols)
            self.board[r][c] = 'B'

    def _calc_adjacency(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'B':
                    continue
                # count bombs in 8 neighbors
                count = 0
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.board[nr][nc] == 'B':
                                count += 1
                self.board[r][c] = count

    def display(self, show_all=False):
        # header
        print("\n   " + " ".join(f"{c:2}" for c in range(self.cols)))
        for r in range(self.rows):
            row_str = []
            for c in range(self.cols):
                if show_all:
                    cell = '💣' if self.board[r][c]=='B' else str(self.board[r][c])
                elif self.flagged[r][c]:
                    cell = '⚑'
                elif not self.revealed[r][c]:
                    cell = '■'
                else:
                    cell = str(self.board[r][c])
                row_str.append(f"{cell:2}")
            print(f"{r:2} " + " ".join(row_str))
        print()

    def flood_reveal(self, r, c):
        # reveal recursively on zeros
        stack = [(r,c)]
        while stack:
            x,y = stack.pop()
            if self.revealed[x][y]:
                continue
            self.revealed[x][y] = True
            self.remaining -= 1
            if self.board[x][y] == 0:
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        nx, ny = x+dr, y+dc
                        if (0 <= nx < self.rows and 0 <= ny < self.cols
                            and not self.revealed[nx][ny]
                            and not self.flagged[nx][ny]):
                            stack.append((nx,ny))

    def play(self):
        while True:
            self.display()
            # get user action
            try:
                action, r, c = input("Enter action (r to reveal, f to flag) and row col: ").split()
                r, c = int(r), int(c)
                if action not in ('r','f') or not (0<=r<self.rows and 0<=c<self.cols):
                    raise ValueError
            except ValueError:
                print("  Invalid input. Example:  r 3 4   or   f 2 1")
                continue

            if action == 'f':
                # toggle flag
                if not self.revealed[r][c]:
                    self.flagged[r][c] = not self.flagged[r][c]
                continue

            # reveal
            if self.flagged[r][c]:
                print("  Cell is flagged—unflag first.")
                continue

            if self.board[r][c] == 'B':
                # hit a bomb → game over
                print("\n💥 Boom! You hit a mine. Game over.")
                self.display(show_all=True)
                return

            # safe reveal
            self.flood_reveal(r, c)

            # win check
            if self.remaining == 0:
                print("\n🎉 Congratulations! You cleared all safe cells!")
                self.display(show_all=True)
                return

if __name__ == "__main__":
    # parse optional size arguments
    if len(sys.argv) == 4:
        try:
            r, c, b = map(int, sys.argv[1:])
            game = Minesweeper(r, c, b)
        except:
            print("Usage: python minesweeper.py [rows cols bombs]")
            sys.exit(1)
    else:
        game = Minesweeper()
    game.play()
