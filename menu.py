import pygame
import sys
import json
import os
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Principal")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fontes
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)

# Arquivo para salvar scores
SCORE_FILE = "high_scores.json"

# Estado do jogo
class GameState:
    MENU = 0
    JOGO = 1
    SCORES = 2

current_state = GameState.MENU

# Funções para gerenciar scores
def load_scores():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"player_wins": 0, "ai_wins": 0, "draws": 0}
    return {"player_wins": 0, "ai_wins": 0, "draws": 0}

def save_scores(scores):
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f)

def update_score(result):
    scores = load_scores()
    if result == "player":
        scores["player_wins"] += 1
    elif result == "ai":
        scores["ai_wins"] += 1
    elif result == "draw":
        scores["draws"] += 1
    save_scores(scores)

# Variáveis do jogo da velha
board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'X'  # Jogador sempre começa
game_over = False
winner = None
player_symbol = 'X'
ai_symbol = 'O'

# IA do jogo da velha
class TicTacToeAI:
    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = 'X' if symbol == 'O' else 'O'
    
    def get_empty_cells(self, board):
        return [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    
    def check_winner(self, board, player):
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
    
    def minimax(self, board, depth, is_maximizing):
        # Verificar se o jogo terminou
        if self.check_winner(board, self.symbol):
            return 10 - depth
        if self.check_winner(board, self.opponent_symbol):
            return depth - 10
        if not self.get_empty_cells(board):
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for i, j in self.get_empty_cells(board):
                board[i][j] = self.symbol
                score = self.minimax(board, depth + 1, False)
                board[i][j] = ''
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i, j in self.get_empty_cells(board):
                board[i][j] = self.opponent_symbol
                score = self.minimax(board, depth + 1, True)
                board[i][j] = ''
                best_score = min(score, best_score)
            return best_score
    
    def get_best_move(self, board):
        best_score = -float('inf')
        best_move = None
        
        # Se for o primeiro movimento, escolher aleatoriamente para variar
        if len(self.get_empty_cells(board)) == 9:
            return random.choice([(0,0), (0,2), (2,0), (2,2), (1,1)])
        
        for i, j in self.get_empty_cells(board):
            board[i][j] = self.symbol
            score = self.minimax(board, 0, False)
            board[i][j] = ''
            
            if score > best_score:
                best_score = score
                best_move = (i, j)
        
        return best_move

# Criar instância da IA
ai = TicTacToeAI(ai_symbol)

# Função para desenhar o menu
def draw_menu():
    screen.fill(WHITE)
    
    # Título
    title = font_large.render("MENU PRINCIPAL", True, BLACK)
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

# Função para desenhar o tabuleiro do jogo da velha
def draw_board():
    # Fundo
    screen.fill(WHITE)
    
    # Título
    title = font_large.render("JOGO DA VELHA", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
    
    # Desenhar grade
    cell_size = 100
    board_x = WIDTH//2 - 150
    board_y = HEIGHT//2 - 150
    
    # Linhas verticais
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, 
                        (board_x + i * cell_size, board_y),
                        (board_x + i * cell_size, board_y + 3 * cell_size), 3)
    
    # Linhas horizontais
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK,
                        (board_x, board_y + i * cell_size),
                        (board_x + 3 * cell_size, board_y + i * cell_size), 3)
    
    # Desenhar X e O
    for row in range(3):
        for col in range(3):
            x = board_x + col * cell_size + cell_size // 2
            y = board_y + row * cell_size + cell_size // 2
            
            if board[row][col] == 'X':
                # Desenhar X vermelho (Jogador)
                pygame.draw.line(screen, RED, (x-30, y-30), (x+30, y+30), 5)
                pygame.draw.line(screen, RED, (x+30, y-30), (x-30, y+30), 5)
            elif board[row][col] == 'O':
                # Desenhar O azul (IA)
                pygame.draw.circle(screen, BLUE, (x, y), 30, 5)
    
    # Botão Voltar
    pygame.draw.rect(screen, GRAY, (50, 50, 100, 40))
    voltar_text = font_small.render("Voltar", True, BLACK)
    screen.blit(voltar_text, (75, 55))
    
    # Botão Reiniciar
    pygame.draw.rect(screen, GRAY, (WIDTH - 150, 50, 100, 40))
    reiniciar_text = font_small.render("Reiniciar", True, BLACK)
    screen.blit(reiniciar_text, (WIDTH - 140, 55))
    
    # Mostrar jogador atual ou resultado
    if not game_over:
        if current_player == player_symbol:
            player_text = font_medium.render("Sua vez (X)", True, BLACK)
        else:
            player_text = font_medium.render("Vez da IA (O)", True, BLACK)
        screen.blit(player_text, (WIDTH//2 - player_text.get_width()//2, HEIGHT - 100))
    else:
        if winner == player_symbol:
            result_text = font_medium.render("Você venceu!", True, GREEN)
            pygame.display.flip()
            pygame.time.wait(1000)  # Pequena pausa antes de salvar
        elif winner == ai_symbol:
            result_text = font_medium.render("IA venceu!", True, RED)
            pygame.display.flip()
            pygame.time.wait(1000)
        else:
            result_text = font_medium.render("Empate!", True, YELLOW)
            pygame.display.flip()
            pygame.time.wait(1000)
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT - 100))

# Função para verificar vitória
def check_winner():
    global winner, game_over
    
    # Verificar linhas
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '':
            winner = board[row][0]
            game_over = True
            return
    
    # Verificar colunas
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            winner = board[0][col]
            game_over = True
            return
    
    # Verificar diagonais
    if board[0][0] == board[1][1] == board[2][2] != '':
        winner = board[0][0]
        game_over = True
        return
    if board[0][2] == board[1][1] == board[2][0] != '':
        winner = board[0][2]
        game_over = True
        return
    
    # Verificar empate
    if all(board[row][col] != '' for row in range(3) for col in range(3)):
        game_over = True
        winner = None

# Função para fazer uma jogada do jogador
def make_player_move(row, col):
    global current_player, game_over
    
    if board[row][col] == '' and not game_over and current_player == player_symbol:
        board[row][col] = player_symbol
        check_winner()
        
        if not game_over:
            current_player = ai_symbol
            # IA joga após um pequeno delay
            pygame.display.flip()
            pygame.time.wait(500)  # Delay para parecer mais natural
            make_ai_move()

# Função para a IA fazer uma jogada
def make_ai_move():
    global current_player, game_over
    
    if not game_over and current_player == ai_symbol:
        row, col = ai.get_best_move(board)
        board[row][col] = ai_symbol
        check_winner()
        
        if not game_over:
            current_player = player_symbol

# Função para reiniciar o jogo
def reset_game():
    global board, current_player, game_over, winner
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = player_symbol  # Jogador sempre começa
    game_over = False
    winner = None

# Função para desenhar a tela de scores
def draw_scores():
    screen.fill(WHITE)
    
    title = font_large.render("HIGH SCORES", True, BLACK)
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

# Loop principal do jogo
running = True
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
                    reset_game()
                
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
                
                # Botão Reiniciar
                elif WIDTH - 150 <= mouse_pos[0] <= WIDTH - 50 and 50 <= mouse_pos[1] <= 90:
                    reset_game()
                
                # Clicar no tabuleiro (só se for vez do jogador)
                elif not game_over and current_player == player_symbol:
                    board_x = WIDTH//2 - 150
                    board_y = HEIGHT//2 - 150
                    cell_size = 100
                    
                    # Verificar qual célula foi clicada
                    for row in range(3):
                        for col in range(3):
                            cell_rect = pygame.Rect(
                                board_x + col * cell_size,
                                board_y + row * cell_size,
                                cell_size, cell_size
                            )
                            if cell_rect.collidepoint(mouse_pos):
                                make_player_move(row, col)
            
            # Tela de Scores
            elif current_state == GameState.SCORES:
                if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 90:
                    current_state = GameState.MENU
    
    # Verificar se o jogo terminou e salvar o score
    if current_state == GameState.JOGO and game_over:
        if winner == player_symbol:
            update_score("player")
        elif winner == ai_symbol:
            update_score("ai")
        else:
            update_score("draw")
        # Resetar para evitar salvar múltiplas vezes
        game_over = False
    
    # Desenhar a tela baseada no estado atual
    if current_state == GameState.MENU:
        draw_menu()
    elif current_state == GameState.JOGO:
        draw_board()
    elif current_state == GameState.SCORES:
        draw_scores()
    
    pygame.display.flip()

pygame.quit()
sys.exit()