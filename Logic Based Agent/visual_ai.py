import tkinter as tk
from tkinter import messagebox
from minesweeper import Minesweeper
from ai_agent import MinesweeperAI

TILE_SIZE = 40
DELAY_MS = 500  

class MinesweeperGUI:
    def __init__(self, root, rows=6, cols=6, bombs=6):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.bombs = bombs

        # Frame for game grid and buttons
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=5)

        self.restart_button = tk.Button(self.control_frame, text="Restart", command=self.restart_game)
        self.restart_button.pack()

        self.setup_game()

    def setup_game(self):
        self.game = Minesweeper(self.rows, self.cols, self.bombs)
        self.ai = MinesweeperAI(self.game)

        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        for widget in self.top_frame.winfo_children():
            widget.destroy()

        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.top_frame, width=3, height=1, font=('Arial', 14), relief='raised')
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

        self.root.after(1000, self.ai_step)

    def update_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = self.buttons[r][c]
                if self.game.flagged[r][c]:
                    btn.config(text='⚑', bg='orange')
                elif self.game.revealed[r][c]:
                    val = self.game.board[r][c]
                    btn.config(text='' if val == 0 else str(val), relief='sunken', bg='lightgrey')
                else:
                    btn.config(text='', bg='SystemButtonFace', relief='raised')

    def ai_step(self):
        self.update_board()

        if self.game.remaining == 0:
            messagebox.showinfo("Victory", "🎉 AI cleared the board!")
            self.update_board()
            return

        move = self.ai.make_informed_move()
        if not move:
            move = self.ai.make_random_move()
        if not move:
            messagebox.showinfo("Done", "No moves left.")
            return

        action, (r, c) = move

        if action == 'flag':
            if not self.game.revealed[r][c]:
                self.game.flagged[r][c] = True
        elif action == 'reveal':
            if self.game.board[r][c] == 'B':
                self.game.revealed[r][c] = True
                self.update_board()
                messagebox.showerror("Game Over", "💥 AI hit a mine!")
                return
            self.game.flood_reveal(r, c)

        self.root.after(DELAY_MS, self.ai_step)

    def restart_game(self):
        self.setup_game()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper AI - Visual Mode")
    app = MinesweeperGUI(root, rows=6, cols=6, bombs=6)
    root.mainloop()
