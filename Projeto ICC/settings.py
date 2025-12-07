import pygame
import os

pygame.font.init()

#DIMENSÕES
LARGURA_TELA = 900
ALTURA_TELA = 700
TITULO_JANELA = "JOGO DA VELHA ULTIMATE"


COR_FUNDO = (20, 23, 30)
COR_GRADE_GLOBAL = (255, 255, 255)
COR_GRADE_PEQUENA = (60, 70, 85)
COR_TABULEIRO_ATIVO = (40, 45, 60)

#botões e interface
COR_BOTAO = (50, 168, 82)
COR_BOTAO_HOVER = (60, 188, 92)
COR_TEXTO = (235, 235, 235)

#Jogadores
COR_JOGADOR_X = (255, 80, 80)
COR_JOGADOR_O = (0, 200, 255)
COR_VITORIA_X = (255, 80, 80, 80)
COR_VITORIA_O = (0, 200, 255, 80)

#FONTES
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_FONTE = os.path.join(BASE_DIR, "PixelifySans-VariableFont_wght.ttf")

fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 48)
fonte_media = pygame.font.Font(CAMINHO_FONTE, 30)
fonte_pequena = pygame.font.Font(CAMINHO_FONTE, 20)
fonte_minuscula = pygame.font.Font(CAMINHO_FONTE, 14)

fonte_simbolo = pygame.font.Font(CAMINHO_FONTE, 40)
fonte_vencedor = pygame.font.Font(CAMINHO_FONTE, 80)

#ARQUIVOS DE DADOS DO JSON
ARQUIVO_JOGADORES = "jogadores.json"
ARQUIVO_PARTIDAS = "partidas.json"
ARQUIVO_MOVIMENTOS = "movimentos.json"

#ESTADOS DO JOGO
class EstadoJogo:
    MENU = 0
    JOGANDO = 1
    RANKING = 2
    INSTRUCOES = 3
    NOME = 4
    SENHA = 5
    FIM = 6