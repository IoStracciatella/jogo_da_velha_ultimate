import pygame

# Inicializa fontes
pygame.font.init()

# Configurações da tela
WIDTH, HEIGHT = 900, 700
CAPTION = "JOGO DA VELHA"

# --- PALETA DE CORES (DARK NEON) ---
# Fundo e Elementos Base
BACKGROUND_COLOR = (20, 23, 30)      # Azul muito escuro (quase preto)
GRID_COLOR_GLOBAL = (255, 255, 255)  # Branco para as linhas grossas principais
GRID_COLOR_SMALL = (60, 70, 85)      # Cinza azulado para as linhas finas
ACTIVE_BOARD_BG = (40, 45, 60)       # Fundo levemente mais claro para o tabuleiro ativo

# Botões e Interface
BUTTON_COLOR = (50, 168, 82)         # Verde suave
BUTTON_HOVER_COLOR = (60, 188, 92)
TEXT_COLOR = (235, 235, 235)         # Branco gelo (menos agressivo que branco puro)

# Jogadores (Cores Neon)
PLAYER_X_COLOR = (255, 80, 80)       # Vermelho Neon
PLAYER_O_COLOR = (0, 200, 255)       # Ciano Neon
WINNER_X_BG = (255, 80, 80, 80)      # Vermelho transparente (para vitória local)
WINNER_O_BG = (0, 200, 255, 80)      # Azul transparente (para vitória local)

# Fontes Modernas (Tenta pegar Arial Rounded ou Verdana, senão usa padrão)
# Usaremos 'bold' para deixar os símbolos mais "gordinhos"
font_large = pygame.font.SysFont('Verdana', 48, bold=True)
font_medium = pygame.font.SysFont('Verdana', 30)
font_small = pygame.font.SysFont('Verdana', 20)
font_tiny = pygame.font.SysFont('Verdana', 14)
font_symbol = pygame.font.SysFont('Arial', 40, bold=True) # Fonte específica para X e O
font_winner = pygame.font.SysFont('Arial', 80, bold=True)

# ARQUIVOS DE DADOS
FILE_PLAYERS = "players.json"
FILE_MATCHES = "matches.json"
FILE_MOVES = "moves.json"

# Estado do jogo
class GameState:
    MENU = 0
    JOGO = 1
    SCORES = 2
    INSTRUCOES = 3  # <--- NOVO
    NOME = 4
    SENHA = 5