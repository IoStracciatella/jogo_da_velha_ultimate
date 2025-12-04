import random
from game import JogoDaVelha

class UltimateAI:
    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = 'X' if symbol == 'O' else 'O'

    # --- Verifica vitória no tabuleiro local ---
    def check_win(self, board, player):
        lines = [
            [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
            [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
            [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]
        ]
        for line in lines:
            if all(board[r][c] == player for r,c in line):
                return True
        return False

    # --- IA simples: vence > bloqueia > aleatório ---
    def get_best_move(self, game):
        valid_moves = game.obter_movimentos_validos()
        if not valid_moves:
            return None

        # 1. Tenta ganhar algum mini-tabuleiro
        for (b, r, c) in valid_moves:
            # copia do tabuleiro local
            temp = [row[:] for row in game.tabuleiros[b]]
            temp[r][c] = self.symbol
            if self.check_win(temp, self.symbol):
                return (b, r, c)

        # 2. Tenta bloquear vitória do adversário
        for (b, r, c) in valid_moves:
            temp = [row[:] for row in game.tabuleiros[b]]
            temp[r][c] = self.opponent_symbol
            if self.check_win(temp, self.opponent_symbol):
                return (b, r, c)

        # 3. Se nada urgente, escolhe aleatório
        return random.choice(valid_moves)
