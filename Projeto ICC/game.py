# Se você quiser seguir estritamente a imagem, coloque isso em board.py
# Se preferir lógica de jogo, pode ser game.py, mas board.py faz sentido aqui.

class JogoDaVelha:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        # 9 tabuleiros pequenos (3x3 cada)
        self.boards = [[['' for _ in range(3)] for _ in range(3)] for _ in range(9)]
        # Tabuleiro global (vencedores de cada tabuleiro pequeno)
        self.global_board = ['' for _ in range(9)]
        self.current_player = 'X'  # Jogador começa
        self.next_board = None  # None significa que pode jogar em qualquer tabuleiro
        self.game_over = False
        self.winner = None
        self.score_saved = False 
    
    def get_valid_moves(self):
        moves = []
        if self.next_board is None:
            for board_idx in range(9):
                if self.global_board[board_idx] == '':
                    for i in range(3):
                        for j in range(3):
                            if self.boards[board_idx][i][j] == '':
                                moves.append((board_idx, i, j))
        else:
            if self.global_board[self.next_board] == '':
                for i in range(3):
                    for j in range(3):
                        if self.boards[self.next_board][i][j] == '':
                            moves.append((self.next_board, i, j))
            else:
                for board_idx in range(9):
                    if self.global_board[board_idx] == '':
                        for i in range(3):
                            for j in range(3):
                                if self.boards[board_idx][i][j] == '':
                                    moves.append((board_idx, i, j))
        return moves
    
    def make_move(self, board_idx, row, col):
        if self.game_over:
            return False
        
        valid_moves = self.get_valid_moves()
        if (board_idx, row, col) not in valid_moves:
            return False
        
        self.boards[board_idx][row][col] = self.current_player
        
        if self.check_small_board_winner(board_idx, self.current_player):
            self.global_board[board_idx] = self.current_player
        
        self.next_board = row * 3 + col
        
        if self.global_board[self.next_board] != '':
            self.next_board = None
        
        self.check_global_winner()
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True
    
    def check_small_board_winner(self, board_idx, player):
        board = self.boards[board_idx]
        for i in range(3):
            if all(board[i][j] == player for j in range(3)): return True
        for j in range(3):
            if all(board[i][j] == player for i in range(3)): return True
        if all(board[i][i] == player for i in range(3)): return True
        if all(board[i][2-i] == player for i in range(3)): return True
        return False
    
    def is_small_board_full(self, board_idx):
        board = self.boards[board_idx]
        for i in range(3):
            for j in range(3):
                if board[i][j] == '': return False
        return True
    
    def check_global_winner(self):
        lines = [
            [0,1,2], [3,4,5], [6,7,8], # Linhas
            [0,3,6], [1,4,7], [2,5,8], # Colunas
            [0,4,8], [2,4,6]           # Diagonais
        ]
        
        for line in lines:
            if all(self.global_board[i] == 'X' for i in line):
                self.winner = 'X'; self.game_over = True; return
            if all(self.global_board[i] == 'O' for i in line):
                self.winner = 'O'; self.game_over = True; return

        if all(self.global_board[i] != '' or self.is_small_board_full(i) for i in range(9)):
            self.game_over = True
            self.winner = None