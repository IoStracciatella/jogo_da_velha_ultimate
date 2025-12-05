from settings import *

class JogoDaVelha:
    def __init__(self):
        self.reiniciar_jogo()
    
    def reiniciar_jogo(self):
        # A estrutura continua a mesma para não quebrar o resto do seu código
        # 9 tabuleiros, cada um com 3 linhas e 3 colunas
        self.tabuleiros_locais = [[['' for _ in range(3)] for _ in range(3)] for _ in range(9)]
        
        # Quem ganhou cada um dos 9 grandes blocos
        self.tabuleiro_global = [''] * 9
        
        self.jogador_atual = 'X'
        self.proximo_tabuleiro_foco = None # None significa "livre para jogar onde quiser"
        
        self.jogo_acabou = False
        self.vencedor = None
        self.pontuacao_salva = False
        self.historico_jogadas = []
    
    def obter_movimentos_validos(self):
        movimentos = []
        
        # 1. Descobrir em quais tabuleiros podemos jogar
        tabuleiros_permitidos = []
        
        # Se temos um foco obrigatório e esse tabuleiro ainda não foi ganho:
        if self.proximo_tabuleiro_foco is not None and self.tabuleiro_global[self.proximo_tabuleiro_foco] == '':
            tabuleiros_permitidos.append(self.proximo_tabuleiro_foco)
        else:
            # Caso contrário, podemos jogar em qualquer tabuleiro que não tenha terminado
            for i in range(9):
                if self.tabuleiro_global[i] == '':
                    tabuleiros_permitidos.append(i)
        
        # 2. Olhar dentro desses tabuleiros e achar os espaços vazios
        for idx in tabuleiros_permitidos:
            for linha in range(3):
                for coluna in range(3):
                    # Se a célula está vazia, é uma jogada válida
                    if self.tabuleiros_locais[idx][linha][coluna] == '':
                        movimentos.append((idx, linha, coluna))
                        
        return movimentos
    
    def fazer_jogada(self, idx_tabuleiro, linha, coluna):
        # Proteção básica
        if self.jogo_acabou:
            return False
            
        # Verifica se a jogada está na lista de permitidas
        if (idx_tabuleiro, linha, coluna) not in self.obter_movimentos_validos():
            return False
        
        # --- Passo 1: Marcar a jogada ---
        self.tabuleiros_locais[idx_tabuleiro][linha][coluna] = self.jogador_atual
        
        self.historico_jogadas.append({
            "jogador": self.jogador_atual,
            "tabuleiro": idx_tabuleiro,
            "posicao": [linha, coluna]
        })
        
        # --- Passo 2: Verificou se ganhou o tabuleiro local? ---
        if self.verificar_vitoria_local(idx_tabuleiro, self.jogador_atual):
            self.tabuleiro_global[idx_tabuleiro] = self.jogador_atual
            
        # --- Passo 3: Definir onde será a próxima jogada ---
        # A regra é: jogou na posição (linha, coluna), manda o oponente para o tabuleiro correspondente.
        # Ex: Linha 0, Coluna 2 -> Tabuleiro 2
        # Ex: Linha 1, Coluna 1 -> Tabuleiro 4
        # A conta matemática simples para isso é:
        destino = linha * 3 + coluna
        self.proximo_tabuleiro_foco = destino
        
        # Mas se o destino já estiver cheio ou alguém já ganhou lá, libera o jogo (None)
        if self.tabuleiro_global[destino] != '' or self.tabuleiro_local_cheio(destino):
            self.proximo_tabuleiro_foco = None 
            
        # --- Passo 4: Verificar fim de jogo e trocar turno ---
        self.verificar_vencedor_global()
        self.trocar_turno()
        return True
    
    def trocar_turno(self):
        if self.jogador_atual == 'X':
            self.jogador_atual = 'O'
        else:
            self.jogador_atual = 'X'

    def verificar_vitoria_local(self, idx, jogador):
        # Pegamos o tabuleiro pequeno para facilitar a leitura
        t = self.tabuleiros_locais[idx]
        
        # Checa as 3 Linhas
        if t[0][0] == t[0][1] == t[0][2] == jogador: return True
        if t[1][0] == t[1][1] == t[1][2] == jogador: return True
        if t[2][0] == t[2][1] == t[2][2] == jogador: return True
        
        # Checa as 3 Colunas
        if t[0][0] == t[1][0] == t[2][0] == jogador: return True
        if t[0][1] == t[1][1] == t[2][1] == jogador: return True
        if t[0][2] == t[1][2] == t[2][2] == jogador: return True
        
        # Checa as 2 Diagonais
        if t[0][0] == t[1][1] == t[2][2] == jogador: return True
        if t[0][2] == t[1][1] == t[2][0] == jogador: return True
        
        return False
    
    def verificar_vencedor_global(self):
        tg = self.tabuleiro_global
        
        # Lista simples de trios que ganham o jogo
        combinacoes = [
            (0,1,2), (3,4,5), (6,7,8), # Linhas
            (0,3,6), (1,4,7), (2,5,8), # Colunas
            (0,4,8), (2,4,6)           # Diagonais
        ]
        
        # 1. Alguém completou uma linha/coluna/diagonal global?
        for a, b, c in combinacoes:
            if tg[a] == tg[b] == tg[c] and tg[a] != '':
                self.vencedor = tg[a]
                self.jogo_acabou = True
                return

        # 2. Se ninguém ganhou, verifica se empatou (tabuleiro cheio)
        ainda_tem_espaco = False
        for i in range(9):
            # Se o tabuleiro global tá vazio E o local não tá cheio, ainda tem jogo
            if tg[i] == '' and not self.tabuleiro_local_cheio(i):
                ainda_tem_espaco = True
                break
        
        if not ainda_tem_espaco:
            self.jogo_acabou = True
            self.vencedor = None # Empate

    def tabuleiro_local_cheio(self, idx):
        # Percorre todas as células do tabuleiro local
        for linha in range(3):
            for coluna in range(3):
                # Se achar UM espaço vazio, não está cheio
                if self.tabuleiros_locais[idx][linha][coluna] == '':
                    return False
        # Se passou por tudo e não retornou False, é porque está cheio
        return True