import pygame
import os

# Inicializa fontes do pygame para evitar erros de init
pygame.font.init()

# --- DIMENSÕES E TÍTULO ---
LARGURA_TELA = 900
ALTURA_TELA = 700
TITULO_JANELA = "JOGO DA VELHA ULTIMATE"

# --- PALETA DE CORES (DARK NEON) ---
# Fundo e Elementos Base
COR_FUNDO = (20, 23, 30)           # Azul muito escuro (quase preto)
COR_GRADE_GLOBAL = (255, 255, 255) # Branco para as linhas grossas principais
COR_GRADE_PEQUENA = (60, 70, 85)   # Cinza azulado para as linhas finas
COR_TABULEIRO_ATIVO = (40, 45, 60) # Fundo destaque para onde o jogador deve jogar

# Botões e Interface
COR_BOTAO = (50, 168, 82)          # Verde suave
COR_BOTAO_HOVER = (60, 188, 92)    # Verde mais claro (ao passar mouse)
COR_TEXTO = (235, 235, 235)        # Branco gelo

# Jogadores (Cores Neon)
COR_JOGADOR_X = (255, 80, 80)      # Vermelho Neon
COR_JOGADOR_O = (0, 200, 255)      # Ciano Neon
COR_VITORIA_X = (255, 80, 80, 80)  # Vermelho transparente (fundo de vitória local)
COR_VITORIA_O = (0, 200, 255, 80)  # Azul transparente

# --- FONTES ---
# Usamos nomes descritivos para facilitar o uso na UI
fonte_titulo = pygame.font.SysFont('Verdana', 48, bold=True)
fonte_media = pygame.font.SysFont('Verdana', 30)
fonte_pequena = pygame.font.SysFont('Verdana', 20)
fonte_minuscula = pygame.font.SysFont('Verdana', 14)
fonte_simbolo = pygame.font.SysFont('Arial', 40, bold=True) # Para desenhar X e O
fonte_vencedor = pygame.font.SysFont('Arial', 80, bold=True) # Para o X/O gigante

# --- ARQUIVOS DE DADOS ---
ARQUIVO_JOGADORES = "jogadores.json"
ARQUIVO_PARTIDAS = "partidas.json"
ARQUIVO_MOVIMENTOS = "movimentos.json"

# --- ESTADOS DO JOGO ---
class EstadoJogo:
    MENU = 0
    JOGANDO = 1
    RANKING = 2     # Antigo SCORES
    INSTRUCOES = 3
    NOME = 4
    SENHA = 5