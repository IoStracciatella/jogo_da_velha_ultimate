from settings import *

class JogoDaVelha:
    def __init__(self):
        self.reiniciar_jogo()
    
    def reiniciar_jogo(self):
        # --- CRIANDO OS 9 TABULEIROS ---
        # Fizemos de um jeito mais "iniciante": montar tudo na mão, passo a passo.
        self.tabuleiros_locais = []

        # Criar nove tabuleiros pequenos (3x3)
        for i in range(9):
            # cada tabuleiro é simplesmente uma lista de 3 listas
            tab = [
                ['', '', ''],
                ['', '', ''],
                ['', '', '']
            ]
            self.tabuleiros_locais.append(tab)

        # --- TABULEIRO GLOBAL ---
        # Lista simples de 9 posições vazias
        self.tabuleiro_global = ['', '', '', '', '', '', '', '', '']

        # Jogador inicial
        self.jogador_atual = 'X'

        # Se None, pode jogar em qualquer tabuleiro
        self.proximo_tabuleiro_foco = None

        # Estado geral
        self.jogo_acabou = False
        self.vencedor = None
        self.pontuacao_salva = False
        self.historico_jogadas = []

        # Gabarito para vitória local (jeito clássico, sem compactar)
        self.combinacoes_vitoria_local = [
            [(0,0), (0,1), (0,2)],
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],

            [(0,0), (1,0), (2,0)],
            [(0,1), (1,1), (2,1)],
            [(0,2), (1,2), (2,2)],

            [(0,0), (1,1), (2,2)],
            [(0,2), (1,1), (2,0)]
        ]
    
    def obter_movimentos_validos(self):
        movimentos = []
        tabuleiros_onde_posso_jogar = []

        # Se tiver foco obrigatório
        if self.proximo_tabuleiro_foco is not None:
            if self.tabuleiro_global[self.proximo_tabuleiro_foco] == '':
                tabuleiros_onde_posso_jogar.append(self.proximo_tabuleiro_foco)

        # Se ainda não tiver nenhum tabuleiro selecionado
        if len(tabuleiros_onde_posso_jogar) == 0:
            for i in range(9):
                if self.tabuleiro_global[i] == '':
                    tabuleiros_onde_posso_jogar.append(i)

        # Procurar casas vazias nos tabuleiros permitidos
        for idx_tab in tabuleiros_onde_posso_jogar:
            tab = self.tabuleiros_locais[idx_tab]
            for lin in range(3):
                for col in range(3):
                    if tab[lin][col] == '':
                        movimentos.append((idx_tab, lin, col))

        return movimentos
    
    def fazer_jogada(self, idx_tabuleiro, linha, coluna):
        if self.jogo_acabou:
            return False

        jogada = (idx_tabuleiro, linha, coluna)
        validas = self.obter_movimentos_validos()

        if jogada not in validas:
            return False

        # Marcação de X ou O
        self.tabuleiros_locais[idx_tabuleiro][linha][coluna] = self.jogador_atual

        # Registrar jogada (iniciante costuma usar dicionário assim)
        self.historico_jogadas.append({
            "jogador": self.jogador_atual,
            "tabuleiro": idx_tabuleiro,
            "posicao": [linha, coluna]
        })

        # Verificar vitória no tabuleiro pequeno
        ganhou = self.verificar_vitoria_local(idx_tabuleiro, self.jogador_atual)
        if ganhou:
            self.tabuleiro_global[idx_tabuleiro] = self.jogador_atual

        # Definir próximo foco (linha*3+coluna)
        destino = (linha * 3) + coluna

        # Verificar se destino está disponível
        destino_ok = True

        # Se já tem dono ou está cheio, não pode focar nele
        if self.tabuleiro_global[destino] != '':
            destino_ok = False
        else:
            if self.tabuleiro_local_cheio(destino):
                destino_ok = False

        if destino_ok:
            self.proximo_tabuleiro_foco = destino
        else:
            self.proximo_tabuleiro_foco = None

        self.verificar_vencedor_global()
        self.trocar_turno()
        return True
    
    def trocar_turno(self):
        # Estilo bem iniciante e simples
        if self.jogador_atual == 'X':
            self.jogador_atual = 'O'
        else:
            self.jogador_atual = 'X'

    def verificar_vitoria_local(self, idx, jogador):
        tab = self.tabuleiros_locais[idx]

        # Checar cada combinação manualmente
        for comb in self.combinacoes_vitoria_local:
            p1 = comb[0]
            p2 = comb[1]
            p3 = comb[2]

            a = tab[p1[0]][p1[1]]
            b = tab[p2[0]][p2[1]]
            c = tab[p3[0]][p3[1]]

            if a == jogador and b == jogador and c == jogador:
                return True
        
        return False
    
    def verificar_vencedor_global(self):
        # Mesmas combinações do jogo normal
        combinacoes = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]

        tg = self.tabuleiro_global

        # Checar vencedor
        for trio in combinacoes:
            a, b, c = trio[0], trio[1], trio[2]
            if tg[a] != '' and tg[a] == tg[b] and tg[b] == tg[c]:
                self.vencedor = tg[a]
                self.jogo_acabou = True
                return

        # Checar empate global
        tem_espaco = False
        for i in range(9):
            if tg[i] == '' and not self.tabuleiro_local_cheio(i):
                tem_espaco = True
                break

        if not tem_espaco:
            self.jogo_acabou = True
            self.vencedor = None

    def tabuleiro_local_cheio(self, idx):
        tab = self.tabuleiros_locais[idx]

        # Contador “iniciante”
        vazios = 0
        for l in range(3):
            for c in range(3):
                if tab[l][c] == '':
                    vazios += 1
        
        if vazios == 0:
            return True
        else:
            return False
