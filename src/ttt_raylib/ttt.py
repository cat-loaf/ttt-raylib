#!/usr/bin/env python3

from ttt_raylib.consts import GameState

class TicTacToe:
    """State representation of tic-tac-toe game"""
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = GameState.TURN_A

    def makeMove(self, row, col) -> GameState | bool:
        """Attempts to make a move on the board. 
            True on success, 
            False on invalid move. 
            GameState on win/tie
        """
        if self.board[row][col] == ' ':
            self.board[row][col] = 'X' if self.current_player == GameState.TURN_A else 'O'
            self.current_player = GameState.TURN_B if self.current_player == GameState.TURN_A \
                                    else GameState.TURN_A
            
            winner: GameState | None = self.checkWinner()
            return winner if winner else True
        return False
    
    def checkWinner(self) -> GameState | None:
        # rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return GameState.WIN_A if self.board[i][0] == 'X' else GameState.WIN_B
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return GameState.WIN_A if self.board[0][i] == 'X' else GameState.WIN_B
        
        # diags
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return GameState.WIN_A if self.board[0][0] == 'X' else GameState.WIN_B
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return GameState.WIN_A if self.board[0][2] == 'X' else GameState.WIN_B
        
        # tie or ongoing game
        if all(cell != ' ' for row in self.board for cell in row):
            return GameState.TIE
        
        return None  # Game ongoing
    
    def get(self, x, y) -> str:
        return self.board[y][x]