import tkinter as tk
from Logic import TicTacToeLogic
from GUI import TicTacToeGUI
from Logic import HumanPlayer, RandomPlayer, AIPlayer


if __name__ == "__main__":
    x_player = HumanPlayer('X')
    y_player = AIPlayer('O')
    logic = TicTacToeLogic()
    logic.play_game(x_player, y_player)
    