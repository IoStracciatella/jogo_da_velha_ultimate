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

# Caminho ABSOLUTO seguro baseado na pasta do arquivo .py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_FONTE = os.path.join(BASE_DIR, "PixelifySans-VariableFont_wght.ttf")

# Carregando fontes Pixelify
fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 48)
fonte_media = pygame.font.Font(CAMINHO_FONTE, 30)
fonte_pequena = pygame.font.Font(CAMINHO_FONTE, 20)
fonte_minuscula = pygame.font.Font(CAMINHO_FONTE, 14)

# Fonte dos símbolos X e O (também pixel)
fonte_simbolo = pygame.font.Font(CAMINHO_FONTE, 40)
fonte_vencedor = pygame.font.Font(CAMINHO_FONTE, 80)

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
