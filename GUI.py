import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, master, logic ):
        self.master = master
        self.master.title("Tic-Tac-Toe")
        self.logic = logic

        self.buttons = [[None, None, None] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(master, text='', font=('Helvetica', 24), width=5, height=2,
                                               command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def make_move(self, row, col):
        if self.logic.board[row][col] == '':
            self.logic.make_move(row, col)
            self.update_board()
            if self.logic.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.logic.get_current_player()} wins!")
            elif all(self.logic.get_board()[i][j] != '' for i in range(3) for j in range(3)):
                messagebox.showinfo("Game Over", "It's a tie!")
            
            if not self.logic.check_winner():
                ai_row, ai_col = self.logic.best_move()
                if ai_row is not None and ai_col is not None:
                    self.logic.make_move(ai_row, ai_col)
                    self.update_board()
                    
                    if self.logic.check_winner():
                        messagebox.showinfo("Game Over", f"Player {self.logic.get_current_player()} wins!")
                    elif all(self.logic.get_board()[i][j] != '' for i in range(3) for j in range(3)):
                        messagebox.showinfo("Game Over", "It's a tie!")
        else:
            print('invalid move')
    
    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = self.logic.get_board()[i][j]
                
