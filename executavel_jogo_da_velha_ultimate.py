import pygame
import sys
import json
import os
import random
import math

# Código feito por Lucas, Uili e Welton
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Tic-Tac-Toe")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
HIGHLIGHT = (255, 255, 200)
DARK_HIGHLIGHT = (200, 255, 200)

# Fontes
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)
font_tiny = pygame.font.SysFont('Arial', 16)

# Arquivo para salvar scores
SCORE_FILE = "ultimate_scores.json"

# Estado do jogo
class GameState:
    MENU = 0
    JOGO = 1
    SCORES = 2

current_state = GameState.MENU

# Funções para gerenciar scores CORRIGIDAS
def load_scores():
    """Carrega os scores do arquivo JSON"""
    try:
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, 'r') as f:
                scores = json.load(f)
                # Garantir que todas as chaves existem
                if "player_wins" not in scores:
                    scores["player_wins"] = 0
                if "ai_wins" not in scores:
                    scores["ai_wins"] = 0
                if "draws" not in scores:
                    scores["draws"] = 0
                return scores
        else:
            # Criar arquivo com scores zerados se não existir
            default_scores = {"player_wins": 0, "ai_wins": 0, "draws": 0}
            save_scores(default_scores)
            return default_scores
    except Exception as e:
        print(f"Erro ao carregar scores: {e}")
        return {"player_wins": 0, "ai_wins": 0, "draws": 0}

def save_scores(scores):
    """Salva os scores no arquivo JSON"""
    try:
        with open(SCORE_FILE, 'w') as f:
            json.dump(scores, f, indent=4)
        print(f"Scores salvos: {scores}")  # Debug
    except Exception as e:
        print(f"Erro ao salvar scores: {e}")

def update_score(result):
    """Atualiza os scores baseado no resultado"""
    scores = load_scores()
    print(f"Score anterior: {scores}")  # Debug
    
    if result == "player":
        scores["player_wins"] += 1
    elif result == "ai":
        scores["ai_wins"] += 1
    elif result == "draw":
        scores["draws"] += 1
    
    print(f"Score atualizado: {scores}")  # Debug
    save_scores(scores)
    
    # Verificar se salvou corretamente
    verify_scores = load_scores()
    print(f"Score verificado: {verify_scores}")  # Debug

# Classe para o Ultimate Tic-Tac-Toe
class UltimateTicTacToe:
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
        self.score_saved = False  # Nova flag para evitar salvar múltiplas vezes
    
    def get_valid_moves(self):
        moves = []
        if self.next_board is None:
            # Pode jogar em qualquer tabuleiro que não está vencido
            for board_idx in range(9):
                if self.global_board[board_idx] == '':
                    for i in range(3):
                        for j in range(3):
                            if self.boards[board_idx][i][j] == '':
                                moves.append((board_idx, i, j))
        else:
            # Deve jogar no tabuleiro especificado
            if self.global_board[self.next_board] == '':
                for i in range(3):
                    for j in range(3):
                        if self.boards[self.next_board][i][j] == '':
                            moves.append((self.next_board, i, j))
            else:
                # Se o tabuleiro especificado já está vencido, pode jogar em qualquer um
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
        
        # Verificar se o movimento é válido
        valid_moves = self.get_valid_moves()
        if (board_idx, row, col) not in valid_moves:
            return False
        
        # Fazer o movimento
        self.boards[board_idx][row][col] = self.current_player
        
        # Verificar se ganhou o tabuleiro pequeno
        if self.check_small_board_winner(board_idx, self.current_player):
            self.global_board[board_idx] = self.current_player
        
        # Determinar próximo tabuleiro
        self.next_board = row * 3 + col
        
        # Se o próximo tabuleiro já estiver vencido, pode jogar em qualquer um
        if self.global_board[self.next_board] != '':
            self.next_board = None
        
        # Verificar se o jogo acabou
        self.check_global_winner()
        
        # Trocar jogador
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        return True
    
    def check_small_board_winner(self, board_idx, player):
        board = self.boards[board_idx]
        
        # Verificar linhas
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
        
        # Verificar colunas
        for j in range(3):
            if all(board[i][j] == player for i in range(3)):
                return True
        
        # Verificar diagonais
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2-i] == player for i in range(3)):
            return True
        
        return False
    
    def is_small_board_full(self, board_idx):
        board = self.boards[board_idx]
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    return False
        return True
    
    def check_global_winner(self):
        # Verificar linhas
        for i in range(3):
            if all(self.global_board[i*3 + j] == 'X' for j in range(3)):
                self.winner = 'X'
                self.game_over = True
                return
            if all(self.global_board[i*3 + j] == 'O' for j in range(3)):
                self.winner = 'O'
                self.game_over = True
                return
        
        # Verificar colunas
        for j in range(3):
            if all(self.global_board[i*3 + j] == 'X' for i in range(3)):
                self.winner = 'X'
                self.game_over = True
                return
            if all(self.global_board[i*3 + j] == 'O' for i in range(3)):
                self.winner = 'O'
                self.game_over = True
                return
        
        # Verificar diagonais
        if all(self.global_board[i*3 + i] == 'X' for i in range(3)):
            self.winner = 'X'
            self.game_over = True
            return
        if all(self.global_board[i*3 + (2-i)] == 'X' for i in range(3)):
            self.winner = 'X'
            self.game_over = True
            return
        if all(self.global_board[i*3 + i] == 'O' for i in range(3)):
            self.winner = 'O'
            self.game_over = True
            return
        if all(self.global_board[i*3 + (2-i)] == 'O' for i in range(3)):
            self.winner = 'O'
            self.game_over = True
            return
        
        # Verificar empate
        if all(self.global_board[i] != '' or self.is_small_board_full(i) for i in range(9)):
            self.game_over = True
            self.winner = None

# IA para Ultimate Tic-Tac-Toe (mantida igual pois está funcionando)
class UltimateAI:
    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = 'X' if symbol == 'O' else 'O'
    
    def evaluate_small_board(self, board, player):
        """Avalia um tabuleiro pequeno para um jogador específico"""
        score = 0
        opponent = 'X' if player == 'O' else 'O'
        
        # Verificar linhas, colunas e diagonais
        lines = [
            # Linhas
            [(0,0), (0,1), (0,2)],
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],
            # Colunas
            [(0,0), (1,0), (2,0)],
            [(0,1), (1,1), (2,1)],
            [(0,2), (1,2), (2,2)],
            # Diagonais
            [(0,0), (1,1), (2,2)],
            [(0,2), (1,1), (2,0)]
        ]
        
        for line in lines:
            values = [board[i][j] for i, j in line]
            player_count = values.count(player)
            opponent_count = values.count(opponent)
            empty_count = values.count('')
            
            if player_count == 3:
                score += 100
            elif player_count == 2 and empty_count == 1:
                score += 10
            elif player_count == 1 and empty_count == 2:
                score += 1
            elif opponent_count == 3:
                score -= 100
            elif opponent_count == 2 and empty_count == 1:
                score -= 10
            elif opponent_count == 1 and empty_count == 2:
                score -= 1
        
        return score
    
    def evaluate_global_board(self, game, player):
        """Avalia o tabuleiro global para um jogador específico"""
        score = 0
        opponent = 'X' if player == 'O' else 'O'
        global_board = game.global_board
        
        # Verificar linhas, colunas e diagonais do tabuleiro global
        lines = [
            # Linhas
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            # Colunas
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            # Diagonais
            [0, 4, 8],
            [2, 4, 6]
        ]
        
        for line in lines:
            values = [global_board[i] for i in line]
            player_count = values.count(player)
            opponent_count = values.count(opponent)
            empty_count = values.count('')
            
            if player_count == 3:
                score += 10000  # Vitória no jogo
            elif player_count == 2 and empty_count == 1:
                score += 1000
            elif player_count == 1 and empty_count == 2:
                score += 100
            elif opponent_count == 3:
                score -= 10000  # Derrota no jogo
            elif opponent_count == 2 and empty_count == 1:
                score -= 1000
            elif opponent_count == 1 and empty_count == 2:
                score -= 100
        
        return score
    
    def evaluate_position(self, game, player):
        """Avalia a posição atual do jogo para um jogador"""
        score = 0
        
        # Avaliar tabuleiro global
        score += self.evaluate_global_board(game, player)
        
        # Avaliar cada tabuleiro pequeno
        for board_idx in range(9):
            if game.global_board[board_idx] == '':
                board_score = self.evaluate_small_board(game.boards[board_idx], player)
                # Dar mais peso aos tabuleiros centrais e do canto
                if board_idx == 4:  # Centro
                    score += board_score * 2
                elif board_idx in [0, 2, 6, 8]:  # Cantos
                    score += board_score * 1.5
                else:  # Bordas
                    score += board_score
        
        # Estratégia especial: controlar o próximo movimento
        if game.next_board is not None and game.global_board[game.next_board] == '':
            # Se podemos enviar o oponente para um tabuleiro ruim
            next_board_score = self.evaluate_small_board(game.boards[game.next_board], player)
            if next_board_score < 0:  # Tabuleiro favorável ao oponente
                score -= 50
            else:  # Tabuleiro favorável a nós
                score += 50
        
        return score
    
    def minimax(self, game, depth, alpha, beta, maximizing_player):
        """Algoritmo Minimax com poda Alpha-Beta"""
        if depth == 0 or game.game_over:
            return self.evaluate_position(game, self.symbol)
        
        valid_moves = game.get_valid_moves()
        
        if maximizing_player:
            max_eval = -float('inf')
            for move in valid_moves:
                # Fazer cópia do jogo para simular
                game_copy = UltimateTicTacToe()
                game_copy.boards = [[row[:] for row in board] for board in game.boards]
                game_copy.global_board = game.global_board[:]
                game_copy.current_player = game.current_player
                game_copy.next_board = game.next_board
                game_copy.game_over = game.game_over
                game_copy.winner = game.winner
                
                game_copy.make_move(*move)
                eval = self.minimax(game_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                # Fazer cópia do jogo para simular
                game_copy = UltimateTicTacToe()
                game_copy.boards = [[row[:] for row in board] for board in game.boards]
                game_copy.global_board = game.global_board[:]
                game_copy.current_player = game.current_player
                game_copy.next_board = game.next_board
                game_copy.game_over = game.game_over
                game_copy.winner = game.winner
                
                game_copy.make_move(*move)
                eval = self.minimax(game_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def get_best_move(self, game):
        """Encontra o melhor movimento usando Minimax"""
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return None
        
        # Para os primeiros movimentos, escolher estrategicamente
        if len(valid_moves) > 20:
            # Priorizar centro e cantos no início
            good_moves = []
            for move in valid_moves:
                board_idx, row, col = move
                # Centro do tabuleiro global é o mais importante
                if board_idx == 4:
                    good_moves.append(move)
                # Cantos são bons também
                elif board_idx in [0, 2, 6, 8]:
                    good_moves.append(move)
            
            if good_moves:
                # Dentro dos bons tabuleiros, priorizar centro
                best_in_good = []
                for move in good_moves:
                    _, row, col = move
                    if row == 1 and col == 1:  # Centro do tabuleiro pequeno
                        best_in_good.append(move)
                
                if best_in_good:
                    return random.choice(best_in_good)
                return random.choice(good_moves)
        
        # Para jogadas mais avançadas, usar Minimax
        best_score = -float('inf')
        best_moves = []
        
        # Usar profundidade adaptativa baseada na complexidade
        depth = 2 if len(valid_moves) > 15 else 3
        
        for move in valid_moves:
            # Fazer cópia do jogo para simular
            game_copy = UltimateTicTacToe()
            game_copy.boards = [[row[:] for row in board] for board in game.boards]
            game_copy.global_board = game.global_board[:]
            game_copy.current_player = game.current_player
            game_copy.next_board = game.next_board
            game_copy.game_over = game.game_over
            game_copy.winner = game.winner
            
            game_copy.make_move(*move)
            score = self.minimax(game_copy, depth, -float('inf'), float('inf'), False)
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        
        return random.choice(best_moves) if best_moves else random.choice(valid_moves)

# Instâncias do jogo e IA
game = UltimateTicTacToe()
ai = UltimateAI('O')
player_symbol = 'X'
ai_symbol = 'O'

# Função para desenhar o menu
def draw_menu():
    screen.fill(WHITE)
    
    # Título
    title = font_large.render("ULTIMATE TIC-TAC-TOE", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    # Botão Jogar
    pygame.draw.rect(screen, GRAY, (WIDTH//2 - 100, 200, 200, 50))
    jogar_text = font_medium.render("Jogar", True, BLACK)
    screen.blit(jogar_text, (WIDTH//2 - jogar_text.get_width()//2, 210))
    
    # Botão Scores
    pygame.draw.rect(screen, GRAY, (WIDTH//2 - 100, 270, 200, 50))
    scores_text = font_medium.render("Scores", True, BLACK)
    screen.blit(scores_text, (WIDTH//2 - scores_text.get_width()//2, 280))
    
    # Botão Sair
    pygame.draw.rect(screen, GRAY, (WIDTH//2 - 100, 340, 200, 50))
    sair_text = font_medium.render("Sair", True, BLACK)
    screen.blit(sair_text, (WIDTH//2 - sair_text.get_width()//2, 350))

# Função para desenhar o jogo Ultimate
def draw_ultimate_board():
    screen.fill(WHITE)
    
    # Título
    title = font_large.render("ULTIMATE TIC-TAC-TOE", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Tamanhos e posições
    board_size = 600
    start_x = (WIDTH - board_size) // 2
    start_y = 80
    small_board_size = board_size // 3
    cell_size = small_board_size // 3
    
    # Desenhar grade global (linhas grossas)
    for i in range(1, 3):
        # Linhas horizontais
        pygame.draw.line(screen, BLACK, 
                        (start_x, start_y + i * small_board_size),
                        (start_x + board_size, start_y + i * small_board_size), 4)
        # Linhas verticais
        pygame.draw.line(screen, BLACK,
                        (start_x + i * small_board_size, start_y),
                        (start_x + i * small_board_size, start_y + board_size), 4)
    
    # Desenhar cada tabuleiro pequeno
    for big_row in range(3):
        for big_col in range(3):
            board_idx = big_row * 3 + big_col
            
            # Posição do tabuleiro pequeno
            board_x = start_x + big_col * small_board_size
            board_y = start_y + big_row * small_board_size
            
            # Destacar tabuleiro ativo
            if game.next_board == board_idx or (game.next_board is None and game.global_board[board_idx] == ''):
                pygame.draw.rect(screen, HIGHLIGHT, 
                               (board_x + 2, board_y + 2, small_board_size - 4, small_board_size - 4))
            
            # Desenhar grade do tabuleiro pequeno (linhas finas)
            for i in range(1, 3):
                # Linhas horizontais
                pygame.draw.line(screen, GRAY,
                                (board_x, board_y + i * cell_size),
                                (board_x + small_board_size, board_y + i * cell_size), 1)
                # Linhas verticais
                pygame.draw.line(screen, GRAY,
                                (board_x + i * cell_size, board_y),
                                (board_x + i * cell_size, board_y + small_board_size), 1)
            
            # Desenhar X e O nos tabuleiros pequenos
            for small_row in range(3):
                for small_col in range(3):
                    cell_x = board_x + small_col * cell_size + cell_size // 2
                    cell_y = board_y + small_row * cell_size + cell_size // 2
                    
                    symbol = game.boards[board_idx][small_row][small_col]
                    if symbol == 'X':
                        # X vermelho (Jogador)
                        size = cell_size // 3
                        pygame.draw.line(screen, RED, 
                                       (cell_x - size, cell_y - size),
                                       (cell_x + size, cell_y + size), 3)
                        pygame.draw.line(screen, RED,
                                       (cell_x + size, cell_y - size),
                                       (cell_x - size, cell_y + size), 3)
                    elif symbol == 'O':
                        # O azul (IA)
                        radius = cell_size // 3
                        pygame.draw.circle(screen, BLUE, (cell_x, cell_y), radius, 3)
            
            # Desenhar vencedor do tabuleiro pequeno
            if game.global_board[board_idx] != '':
                # Fundo semi-transparente
                s = pygame.Surface((small_board_size, small_board_size), pygame.SRCALPHA)
                if game.global_board[board_idx] == 'X':
                    s.fill((255, 0, 0, 100))  # Vermelho transparente
                else:
                    s.fill((0, 0, 255, 100))  # Azul transparente
                screen.blit(s, (board_x, board_y))
                
                # Símbolo grande
                winner_font = pygame.font.SysFont('Arial', 80)
                winner_text = winner_font.render(game.global_board[board_idx], True, WHITE)
                screen.blit(winner_text, 
                          (board_x + small_board_size//2 - winner_text.get_width()//2,
                           board_y + small_board_size//2 - winner_text.get_height()//2))
    
    # Botões
    pygame.draw.rect(screen, GRAY, (50, 50, 100, 40))
    voltar_text = font_small.render("Voltar", True, BLACK)
    screen.blit(voltar_text, (75, 55))
    
    pygame.draw.rect(screen, GRAY, (WIDTH - 150, 50, 100, 40))
    reiniciar_text = font_small.render("Reiniciar", True, BLACK)
    screen.blit(reiniciar_text, (WIDTH - 140, 55))
    
    # Informações do jogo
    info_y = start_y + board_size + 20
    
    if not game.game_over:
        if game.current_player == player_symbol:
            status_text = font_medium.render("Sua vez (X) - Clique em qualquer lugar verde", True, BLACK)
        else:
            status_text = font_medium.render("Vez da IA (O) - Pensando...", True, BLACK)
    else:
        if game.winner == player_symbol:
            status_text = font_medium.render("Você venceu!", True, GREEN)
        elif game.winner == ai_symbol:
            status_text = font_medium.render("IA venceu!", True, RED)
        else:
            status_text = font_medium.render("Empate!", True, YELLOW)
    
    screen.blit(status_text, (WIDTH//2 - status_text.get_width()//2, info_y))

# Função para desenhar a tela de scores
def draw_scores():
    screen.fill(WHITE)
    
    title = font_large.render("ULTIMATE SCORES", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    
    scores = load_scores()
    
    # Exibir estatísticas
    player_wins_text = font_medium.render(f"Vitórias do Jogador: {scores['player_wins']}", True, GREEN)
    ai_wins_text = font_medium.render(f"Vitórias da IA: {scores['ai_wins']}", True, RED)
    draws_text = font_medium.render(f"Empates: {scores['draws']}", True, YELLOW)
    
    screen.blit(player_wins_text, (WIDTH//2 - player_wins_text.get_width()//2, 180))
    screen.blit(ai_wins_text, (WIDTH//2 - ai_wins_text.get_width()//2, 230))
    screen.blit(draws_text, (WIDTH//2 - draws_text.get_width()//2, 280))
    
    # Calcular total de partidas
    total_games = scores['player_wins'] + scores['ai_wins'] + scores['draws']
    if total_games > 0:
        win_rate = (scores['player_wins'] / total_games) * 100
        win_rate_text = font_medium.render(f"Taxa de Vitória: {win_rate:.1f}%", True, BLUE)
        screen.blit(win_rate_text, (WIDTH//2 - win_rate_text.get_width()//2, 330))
    
    # Botão Voltar
    pygame.draw.rect(screen, GRAY, (50, 50, 100, 40))
    voltar_text = font_small.render("Voltar", True, BLACK)
    screen.blit(voltar_text, (75, 55))

# Função para fazer jogada da IA
def make_ai_move():
    if not game.game_over and game.current_player == ai_symbol:
        move = ai.get_best_move(game)
        if move:
            game.make_move(*move)

# Loop principal do jogo CORRIGIDO
running = True
ai_thinking = False
score_update_pending = False
score_result = None

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Menu Principal
            if current_state == GameState.MENU:
                # Botão Jogar
                if WIDTH//2 - 100 <= mouse_pos[0] <= WIDTH//2 + 100 and 200 <= mouse_pos[1] <= 250:
                    current_state = GameState.JOGO
                    game.reset_game()
                    ai_thinking = False
                    score_update_pending = False
                
                # Botão Scores
                elif WIDTH//2 - 100 <= mouse_pos[0] <= WIDTH//2 + 100 and 270 <= mouse_pos[1] <= 320:
                    current_state = GameState.SCORES
                
                # Botão Sair
                elif WIDTH//2 - 100 <= mouse_pos[0] <= WIDTH//2 + 100 and 340 <= mouse_pos[1] <= 390:
                    running = False
            
            # Tela do Jogo
            elif current_state == GameState.JOGO:
                # Botão Voltar
                if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 90:
                    current_state = GameState.MENU
                    score_update_pending = False
                
                # Botão Reiniciar
                elif WIDTH - 150 <= mouse_pos[0] <= WIDTH - 50 and 50 <= mouse_pos[1] <= 90:
                    game.reset_game()
                    ai_thinking = False
                    score_update_pending = False
                
                # Clicar no tabuleiro (só se for vez do jogador)
                elif not game.game_over and game.current_player == player_symbol:
                    board_size = 600
                    start_x = (WIDTH - board_size) // 2
                    start_y = 80
                    small_board_size = board_size // 3
                    cell_size = small_board_size // 3
                    
                    # Verificar clique em algum tabuleiro
                    for big_row in range(3):
                        for big_col in range(3):
                            board_idx = big_row * 3 + big_col
                            board_x = start_x + big_col * small_board_size
                            board_y = start_y + big_row * small_board_size
                            
                            # Verificar se o clique foi neste tabuleiro
                            if (board_x <= mouse_pos[0] <= board_x + small_board_size and
                                board_y <= mouse_pos[1] <= board_y + small_board_size):
                                
                                # Verificar se pode jogar neste tabuleiro
                                if game.next_board is None or game.next_board == board_idx:
                                    # Encontrar célula específica
                                    rel_x = mouse_pos[0] - board_x
                                    rel_y = mouse_pos[1] - board_y
                                    
                                    small_col = rel_x // cell_size
                                    small_row = rel_y // cell_size
                                    
                                    if 0 <= small_row < 3 and 0 <= small_col < 3:
                                        # Tentar fazer a jogada
                                        if game.make_move(board_idx, int(small_row), int(small_col)):
                                            ai_thinking = True
            
            # Tela de Scores
            elif current_state == GameState.SCORES:
                if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 90:
                    current_state = GameState.MENU
    
    # Lógica da IA
    if current_state == GameState.JOGO and not game.game_over and game.current_player == ai_symbol and ai_thinking:
        # Pequeno delay para parecer mais natural
        pygame.time.delay(500)
        make_ai_move()
        ai_thinking = False
    
    # Iniciar pensamento da IA
    if current_state == GameState.JOGO and not game.game_over and game.current_player == ai_symbol and not ai_thinking:
        ai_thinking = True
    
    # LÓGICA DE SCORE CORRIGIDA - Salvar score apenas uma vez quando o jogo terminar
    if current_state == GameState.JOGO and game.game_over and not game.score_saved:
        # Determinar resultado
        if game.winner == player_symbol:
            score_result = "player"
        elif game.winner == ai_symbol:
            score_result = "ai"
        else:
            score_result = "draw"
        
        # Marcar que vamos atualizar o score
        score_update_pending = True
        game.score_saved = True  # Importante: marcar que já salvamos para esta partida
    
    # Atualizar score com um pequeno delay para o jogador ver o resultado
    if score_update_pending:
        pygame.time.delay(1000)  # Esperar 1 segundo antes de salvar
        update_score(score_result)
        score_update_pending = False
    
    # Desenhar a tela baseada no estado atual
    if current_state == GameState.MENU:
        draw_menu()
    elif current_state == GameState.JOGO:
        draw_ultimate_board()
    elif current_state == GameState.SCORES:
        draw_scores()
    
    pygame.display.flip()

pygame.quit()
sys.exit()
