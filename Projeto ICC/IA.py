import random

class InteligenciaArtificial:
    def __init__(self, simbolo_ia):
        self.simbolo = simbolo_ia
        self.simbolo_oponente = 'X' if simbolo_ia == 'O' else 'O'

    def verificar_vitoria_simulada(self, tabuleiro_local, jogador):
        """Verifica se um tabuleiro 3x3 tem vencedor."""
        linhas_vitoria = [
            [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)], # H
            [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)], # V
            [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]                       # D
        ]
        for linha in linhas_vitoria:
            if all(tabuleiro_local[r][c] == jogador for r,c in linha):
                return True
        return False

    def obter_melhor_jogada(self, jogo):
        """
        Estratégia:
        1. Se puder ganhar um tabuleiro local agora, ganhe.
        2. Se o oponente for ganhar um tabuleiro local na próxima, bloqueie.
        3. Caso contrário, jogue aleatório.
        """
        movimentos_possiveis = jogo.obter_movimentos_validos()
        
        if not movimentos_possiveis:
            return None

        # 1. Tenta ganhar (Ataque)
        for (idx_tab, lin, col) in movimentos_possiveis:
            # Cria cópia simples do tabuleiro local para simular
            copia_local = [linha[:] for linha in jogo.tabuleiros_locais[idx_tab]]
            copia_local[lin][col] = self.simbolo
            
            if self.verificar_vitoria_simulada(copia_local, self.simbolo):
                return (idx_tab, lin, col)

        # 2. Tenta bloquear (Defesa)
        for (idx_tab, lin, col) in movimentos_possiveis:
            copia_local = [linha[:] for linha in jogo.tabuleiros_locais[idx_tab]]
            copia_local[lin][col] = self.simbolo_oponente
            
            if self.verificar_vitoria_simulada(copia_local, self.simbolo_oponente):
                return (idx_tab, lin, col)

        # 3. Aleatório
        return random.choice(movimentos_possiveis)