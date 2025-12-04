class JogoDaVelha:
    def __init__(self):
        self.reiniciar_jogo()
    
    def reiniciar_jogo(self):
        # 9 tabuleiros de 3x3
        self.tabuleiros = [[['' for _ in range(3)] for _ in range(3)] for _ in range(9)]
        # Tabuleiro principal que guarda quem ganhou cada setor
        self.tabuleiro_global = [''] * 9
        
        self.jogador_atual = 'X'
        self.proximo_tabuleiro = None # None = Pode jogar em qualquer lugar
        self.jogo_acabou = False
        self.vencedor = None
        self.pontuacao_salva = False
        self.historico_jogadas = []
    
    def obter_movimentos_validos(self):
        movimentos = []
        
        # Define em quais tabuleiros o jogador pode jogar
        # Se 'proximo_tabuleiro' for None ou o alvo já estiver cheio/vencido, libera todos
        alvos = range(9)
        if self.proximo_tabuleiro is not None and self.tabuleiro_global[self.proximo_tabuleiro] == '':
            alvos = [self.proximo_tabuleiro]
            
        for idx in alvos:
            # Só pode jogar se o tabuleiro local não foi vencido
            if self.tabuleiro_global[idx] == '':
                for linha in range(3):
                    for coluna in range(3):
                        if self.tabuleiros[idx][linha][coluna] == '':
                            movimentos.append((idx, linha, coluna))
        return movimentos
    
    def fazer_jogada(self, idx_tabuleiro, linha, coluna):
        # Validação básica
        if self.jogo_acabou:
            return False
            
        movimento_solicitado = (idx_tabuleiro, linha, coluna)
        if movimento_solicitado not in self.obter_movimentos_validos():
            return False
        
        # Aplica a jogada
        self.tabuleiros[idx_tabuleiro][linha][coluna] = self.jogador_atual
        
        # Registra no log (mantive chaves compatíveis com seu JSON)
        self.historico_jogadas.append({
            "jogador": self.jogador_atual,
            "tabuleiro": idx_tabuleiro,
            "posicao": [linha, coluna]
        })
        
        # Verifica se ganhou o tabuleiro local
        if self.verificar_vitoria_local(idx_tabuleiro, self.jogador_atual):
            self.tabuleiro_global[idx_tabuleiro] = self.jogador_atual
            
        # Define onde será a próxima jogada (regra do Ultimate)
        self.proximo_tabuleiro = linha * 3 + coluna
        
        # Se o tabuleiro de destino já estiver fechado, libera o jogo (None)
        if self.tabuleiro_global[self.proximo_tabuleiro] != '':
            self.proximo_tabuleiro = None 
            
        # Verifica estado final e troca turno
        self.verificar_vencedor_global()
        self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'
        return True
    
    def verificar_vitoria_local(self, idx, jogador):
        # Acesso direto é mais rápido e legível para matriz 3x3
        tab = self.tabuleiros[idx]
        
        # Linhas e Colunas
        for i in range(3):
            if tab[i][0] == tab[i][1] == tab[i][2] == jogador: return True
            if tab[0][i] == tab[1][i] == tab[2][i] == jogador: return True
            
        # Diagonais
        if tab[0][0] == tab[1][1] == tab[2][2] == jogador: return True
        if tab[0][2] == tab[1][1] == tab[2][0] == jogador: return True
        
        return False
    
    def verificar_vencedor_global(self):
        combinacoes = [
            (0,1,2), (3,4,5), (6,7,8), # Linhas
            (0,3,6), (1,4,7), (2,5,8), # Colunas
            (0,4,8), (2,4,6)           # Diagonais
        ]
        
        tg = self.tabuleiro_global # Alias curto para facilitar leitura
        
        for a, b, c in combinacoes:
            if tg[a] == tg[b] == tg[c] and tg[a] != '':
                self.vencedor = tg[a]
                self.jogo_acabou = True
                return

        # Verifica empate (se todos os tabuleiros têm dono ou estão cheios)
        tabuleiro_cheio = True
        for i in range(9):
            if tg[i] == '' and not self.tabuleiro_local_cheio(i):
                tabuleiro_cheio = False
                break
        
        if tabuleiro_cheio:
            self.jogo_acabou = True
            self.vencedor = None

    def tabuleiro_local_cheio(self, idx):
        # Verifica se não há espaços vazios no tabuleiro pequeno
        return all(celula != '' for linha in self.tabuleiros[idx] for celula in linha)