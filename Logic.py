import random
from typing import Tuple

class TicTacToeLogic:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player1 = None
        self.player2 = None
        self.current_player = None
    
    def make_move(self, row, col):
        if self.board[row][col] == ' ' and not self.check_winner():
            self.board[row][col] = self.current_player.symbol
            
            if not self.check_winner():
                self.update_current_player()
    
    def update_current_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
    
    def check_winner(self,) -> str:
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]

        # Check columns
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != ' ':
                return self.board[0][j]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        return None
    
    def get_board(self):
        return self.board
    
    def get_legal_moves(self) -> list[Tuple[int, int]]:
        legal_moves = []
        for i in range(3):
            for j in range(3):
                if self.get_board()[i][j] == ' ':
                    legal_moves.append((i,j))
        return legal_moves
    
    def deepcopy(self) -> 'TicTacToeLogic':
        copy = TicTacToeLogic()
        copy.current_player = self.current_player
        copy.player1 = self.player1
        copy.player2 = self.player2

        for row in range(3):
            for col in range(3):
                copy.board[row][col] = self.board[row][col]
        return copy
    
    def gameover(self):
        if self.check_winner() or len(self.get_legal_moves()) == 0:
            return True
        return False
    
    def evaluate(self):
        winner = self.check_winner()
        if winner:
            if winner == 'X':  # AI is 'X'
                return 1
            else:  # AI is 'O'
                return -1
        if len(self.get_legal_moves()) == 0:
            return 0  # Draw
        return False
    
    def print_board(self):
        for row in self.board:
            print('| ' + ' | '.join(col for col in row) + ' |')
        
    def play_game(self, player1 :'Player', player2: 'Player'):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1 if player1.symbol == 'X' else player2
        
        while not self.gameover():
            self.current_player.make_move(self)
            self.print_board()
        print('Game over!')


class Player:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        pass
    
    def make_move(self, game: 'TicTacToeLogic') -> None:
        raise NotImplementedError

    
class HumanPlayer(Player):
    def __init__(self, symbol) -> None:
        super().__init__(symbol)
    
    def make_move(self, game: 'TicTacToeLogic') -> None:
        coords = input('Enter coordinates: ').split(',')
        game.make_move(int(coords[0]), int(coords[1]))


class RandomPlayer(Player):
    def __init__(self, symbol,) -> None:
        super().__init__(symbol)
        
    def make_move(self, game: 'TicTacToeLogic') -> None:
        legal_moves = self.logic.get_legal_moves()
        if len(legal_moves) > 0:
            move = random.choice(legal_moves)
            game.make_move(move[0], move[1])

        
class AIPlayer(Player):
    def __init__(self, symbol) -> None:
        super().__init__(symbol)
        
    def make_move(self, game: 'TicTacToeLogic') -> None:
        bestmove = self.get_best_move(game)
        game.make_move(bestmove[1][0], bestmove[1][1])
    
    def get_best_move(self, game) -> Tuple[int, int]:
        maximizing = True if self.symbol == 'X' else False
        alpha = float('-inf')
        beta = float('inf')
        if maximizing:
            bestmove = self.maximize(game, alpha, beta)
        else:
            bestmove = self.minimize(game, alpha, beta)
        return bestmove
    
    def maximize(self, game: 'TicTacToeLogic', alpha, beta) -> Tuple[int, Tuple[int, int]]:
        if game.gameover():
            return (game.evaluate(), None)
        bestscore = float('-inf')
        bestmove = None
        for possible_move in game.get_legal_moves():
            copy = game.deepcopy()
            copy.make_move(possible_move[0], possible_move[1])
            score, move = self.minimize(copy, alpha, beta)
            if score > bestscore:
                bestscore = score
                bestmove = possible_move
                alpha = max(alpha, score)
            if bestscore >= beta:
                return (bestscore, bestmove)
        return (bestscore, bestmove)
        
    def minimize(self, game: 'TicTacToeLogic', alpha, beta) -> Tuple[int, Tuple[int, int]]:
        if game.gameover():
            return (game.evaluate(), None) 
        bestscore = float('inf')
        bestmove = None
        for possible_move in game.get_legal_moves():
            copy = game.deepcopy()
            copy.make_move(possible_move[0], possible_move[1])
            score, move = self.maximize(copy, alpha, beta)
            if score < bestscore:
                bestscore = score
                bestmove = possible_move
                beta = min(beta, bestscore)
            if bestscore <= alpha:
                return (bestscore, bestmove)
        return (bestscore, bestmove)
    