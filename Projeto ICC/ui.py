import pygame
from settings import *
from scores import ler_arquivo, gerar_ranking, realizar_login, verificar_usuario, obter_estatisticas_gerais

# --- FERRAMENTAS AUXILIARES DE DESENHO ---
# --- VARIÁVEIS DE ANIMAÇÃO ---
# --- VARIÁVEIS DE ANIMAÇÃO ---
tamanho_titulo = 48
direcao_titulo = 1
ultimo_update = 0
intervalo = 10  # tempo em ms para atualizar (quanto maior, mais lento)

def desenhar_texto_centralizado(tela, texto, fonte, cor, centro_x, centro_y):
    """Escreve texto centralizado na posição X, Y."""
    superficie_texto = fonte.render(texto, True, cor)
    retangulo = superficie_texto.get_rect(center=(centro_x, centro_y))
    tela.blit(superficie_texto, retangulo)
    return retangulo

def desenhar_botao(tela, texto, x, y, largura, altura, posicao_mouse):
    """Desenha um botão e retorna seu retângulo para detecção de clique."""
    retangulo = pygame.Rect(x, y, largura, altura)
    
    # Efeito de 'Hover' (mudar cor quando o mouse passa por cima)
    cor_atual = COR_BOTAO_HOVER if retangulo.collidepoint(posicao_mouse) else COR_BOTAO
    
    pygame.draw.rect(tela, cor_atual, retangulo, border_radius=10)
    desenhar_texto_centralizado(tela, texto, fonte_media, COR_TEXTO, retangulo.centerx, retangulo.centery)
    
    return retangulo

# --- TELAS DO JOGO ---

def desenhar_menu(tela, posicao_mouse):
    """Tela Principal (Menu)."""
 
    global tamanho_titulo, direcao_titulo, ultimo_update
    
    tela.fill(COR_FUNDO)

    # Atualiza tamanho da fonte (efeito pulso lento)
    agora = pygame.time.get_ticks()
    if agora - ultimo_update > intervalo:
        tamanho_titulo += direcao_titulo * 0.2  # passo menor = mais suave
        if tamanho_titulo > 54 or tamanho_titulo < 48:
            direcao_titulo *= -1
        ultimo_update = agora

    fonte_animada = pygame.font.Font("PixelifySans-VariableFont_wght.ttf", int(tamanho_titulo))

    # Cor alternada suave (muda a cada 500ms)
    cor_animada = (255, 0, 0) if agora // 500 % 2 == 0 else COR_TEXTO

    # Título com sombra + animação
    desenhar_texto_centralizado(tela, TITULO_JANELA, fonte_animada, (0,0,0), LARGURA_TELA//2 + 3, 80 + 3)
    desenhar_texto_centralizado(tela, TITULO_JANELA, fonte_animada,COR_TEXTO, LARGURA_TELA//2, 80)

    # Botões do menu
    lista_botoes = ["Jogar", "Instruções", "Scores", "Sair"]
    inicio_y = 180
    espacamento = 70

    botoes_rects = {}
    for i, texto in enumerate(lista_botoes):
        rect = desenhar_botao(tela, texto, LARGURA_TELA//2 - 100, inicio_y + (i * espacamento), 200, 50, posicao_mouse)
        botoes_rects[texto.upper()] = rect

    return botoes_rects

def desenhar_instrucoes(tela, posicao_mouse):
    """Tela de Como Jogar."""
    tela.fill(COR_FUNDO)
    desenhar_texto_centralizado(tela, "COMO JOGAR", fonte_titulo, COR_TEXTO, LARGURA_TELA//2, 50)

    regras = [
        "O Jogo da Velha Ultimate é jogado em um tabuleiro 9x9.",
        "O objetivo é ganhar 3 tabuleiros menores em linha.",
        "",
        "REGRAS PRINCIPAIS:",
        "1. Onde você joga define onde o oponente deve jogar.",
        "2. Ex: Jogou no canto dir., oponente vai p/ o tabuleiro dir.",
        "3. Se o tabuleiro alvo estiver cheio, jogue em qualquer um.",
        "4. Ganhe o jogo alinhando 3 vitórias de tabuleiros."
    ]

    pos_y = 120
    for linha in regras:
        if "REGRAS" in linha:
            cor, fonte = COR_JOGADOR_O, fonte_media
        else:
            cor, fonte = COR_TEXTO, fonte_pequena

        surf = fonte.render(linha, True, cor)
        tela.blit(surf, (LARGURA_TELA//2 - 250, pos_y))
        pos_y += 35

    desenhar_texto_centralizado(tela, "Jogue para aprender!", fonte_pequena, COR_BOTAO, LARGURA_TELA//2, ALTURA_TELA - 130)
    
    # Botão de voltar (Centralizado embaixo)
    botao_voltar = desenhar_botao(tela, "Voltar", LARGURA_TELA//2 - 100, ALTURA_TELA - 80, 200, 50, posicao_mouse)
    return {"VOLTAR_CENTRO": botao_voltar}

def desenhar_tabuleiro_ultimate(tela, jogo, simbolo_jogador, simbolo_ia, posicao_mouse):
    """Desenha o tabuleiro complexo 9x9 e o estado do jogo."""
    tela.fill(COR_FUNDO)
    desenhar_texto_centralizado(tela, "JOGO DA VELHA", fonte_titulo, COR_TEXTO, LARGURA_TELA//2, 35)

    # Configuração Geométrica
    tamanho_tabuleiro = 600
    inicio_x = (LARGURA_TELA - tamanho_tabuleiro) // 2
    inicio_y = 80
    tamanho_pequeno = tamanho_tabuleiro // 3
    tamanho_celula = tamanho_pequeno // 3

    # Busca dados do objeto Jogo
    tabuleiro_global = jogo.tabuleiro_global
    tabuleiros_locais = jogo.tabuleiros_locais

    # 1. DESENHAR FUNDOS (Destaques e Vitórias)
    for idx_grande in range(9):
        linha_g, col_g = divmod(idx_grande, 3)
        base_x = inicio_x + col_g * tamanho_pequeno
        base_y = inicio_y + linha_g * tamanho_pequeno

        # Destaque: Tabuleiro onde o jogador DEVE jogar agora
        # (Se o jogo não acabou E (o foco é livre OU o foco é este tabuleiro) E o tabuleiro não tem dono)
        eh_tabuleiro_foco = (jogo.proximo_tabuleiro_foco is None or jogo.proximo_tabuleiro_foco == idx_grande)
        if not jogo.jogo_acabou and eh_tabuleiro_foco and tabuleiro_global[idx_grande] == '':
            pygame.draw.rect(tela, COR_TABULEIRO_ATIVO, (base_x+4, base_y+4, tamanho_pequeno-8, tamanho_pequeno-8), border_radius=5)

        # Destaque: Tabuleiro já VENCIDO
        if tabuleiro_global[idx_grande] != '':
            cor_fundo = COR_VITORIA_X if tabuleiro_global[idx_grande] == 'X' else COR_VITORIA_O
            pygame.draw.rect(tela, cor_fundo, (base_x, base_y, tamanho_pequeno, tamanho_pequeno))

    # 2. DESENHAR LINHAS DA GRADE
    # Linhas Finas (dividem as células pequenas)
    for row in range(9):
        py = inicio_y + row * tamanho_celula
        if row % 3 != 0: 
            # CORRIGIDO AQUI EMBAIXO (Adicionei o parametro width=2 corretamente)
            pygame.draw.line(tela, COR_GRADE_PEQUENA, (inicio_x, py), (inicio_x + tamanho_tabuleiro, py), 2)
            
    for col in range(9):
        px = inicio_x + col * tamanho_celula
        if col % 3 != 0: 
            # CORRIGIDO AQUI EMBAIXO
            pygame.draw.line(tela, COR_GRADE_PEQUENA, (px, inicio_y), (px, inicio_y + tamanho_tabuleiro), 2)
    
    # Linhas Grossas (dividem os tabuleiros grandes)
    for i in range(1, 3):
        pos = i * tamanho_pequeno
        pygame.draw.line(tela, COR_GRADE_GLOBAL, (inicio_x, inicio_y + pos), (inicio_x + tamanho_tabuleiro, inicio_y + pos), 6)
        pygame.draw.line(tela, COR_GRADE_GLOBAL, (inicio_x + pos, inicio_y), (inicio_x + pos, inicio_y + tamanho_tabuleiro), 6)

    # 3. DESENHAR SÍMBOLOS (X e O)
    for linha_g in range(3):
        for col_g in range(3):
            idx_grande = linha_g * 3 + col_g
            base_x = inicio_x + col_g * tamanho_pequeno
            base_y = inicio_y + linha_g * tamanho_pequeno

            # Se o tabuleiro grande já tem dono, desenha um Símbolo Gigante
            if tabuleiro_global[idx_grande] != '':
                vencedor_local = tabuleiro_global[idx_grande]
                desenhar_texto_centralizado(tela, vencedor_local, fonte_vencedor, (255,255,255), base_x + tamanho_pequeno//2, base_y + tamanho_pequeno//2)
                continue

            # Caso contrário, desenha os símbolos pequenos das células
            tabuleiro_atual = tabuleiros_locais[idx_grande]
            for sr in range(3):
                for sc in range(3):
                    simbolo = tabuleiro_atual[sr][sc]
                    centro_cx = base_x + sc * tamanho_celula + tamanho_celula//2
                    centro_cy = base_y + sr * tamanho_celula + tamanho_celula//2

                    if simbolo == 'X':
                        desenhar_texto_centralizado(tela, "X", fonte_simbolo, COR_JOGADOR_X, centro_cx, centro_cy)
                    elif simbolo == 'O':
                        desenhar_texto_centralizado(tela, "O", fonte_simbolo, COR_JOGADOR_O, centro_cx, centro_cy)
                    
                    # Feedback visual (Hover) nas células vazias válidas
                    elif not jogo.jogo_acabou and jogo.jogador_atual == simbolo_jogador:
                        rect_celula = pygame.Rect(base_x + sc*tamanho_celula, base_y + sr*tamanho_celula, tamanho_celula, tamanho_celula)
                        
                        # Verifica se o mouse está sobre e se é um tabuleiro válido
                        if rect_celula.collidepoint(posicao_mouse) and (jogo.proximo_tabuleiro_foco is None or jogo.proximo_tabuleiro_foco == idx_grande):
                            superficie_transparente = pygame.Surface((tamanho_celula-4, tamanho_celula-4), pygame.SRCALPHA)
                            superficie_transparente.fill((255, 255, 255, 30)) # Branco transparente
                            tela.blit(superficie_transparente, (rect_celula.x+2, rect_celula.y+2))

    # Botões de controle in-game
    botoes = {
        "VOLTAR_CANTO": desenhar_botao(tela, "Voltar", 50, 50, 100, 40, posicao_mouse),
        "REINICIAR": desenhar_botao(tela, "Reiniciar", LARGURA_TELA - 150, 50, 120, 40, posicao_mouse)
    }

    # Barra de Status Inferior
    if not jogo.jogo_acabou:
        msg = "Sua vez" if jogo.jogador_atual == simbolo_jogador else "IA Pensando..."
        cor_status = COR_JOGADOR_X if jogo.jogador_atual == simbolo_jogador else COR_JOGADOR_O
    else:
        msg = f"Vencedor: {jogo.vencedor}" if jogo.vencedor else "Empate!"
        cor_status = COR_TEXTO

    desenhar_texto_centralizado(tela, msg, fonte_media, cor_status, LARGURA_TELA//2, inicio_y + tamanho_tabuleiro + 30)
    
    return botoes

def desenhar_placar(tela, posicao_mouse):
    """Tela de Ranking e Estatísticas."""
    tela.fill(COR_FUNDO)
    desenhar_texto_centralizado(tela, "HALL DA FAMA", fonte_titulo, COR_TEXTO, LARGURA_TELA//2, 50)

    # Linha divisória vertical
    pygame.draw.line(tela, COR_GRADE_PEQUENA, (LARGURA_TELA//2, 140), (LARGURA_TELA//2, ALTURA_TELA - 120), 2)

    # --- COLUNA ESQUERDA: ESTATÍSTICAS GERAIS ---
    desenhar_texto_centralizado(tela, "Estatísticas Globais", fonte_media, COR_BOTAO, 200, 150)
    
    stats = obter_estatisticas_gerais() 

    linhas_stats = [
        (f"Jogos: {stats['total_partidas']}", COR_TEXTO),
        (f"Vit. Player: {stats['vitorias_jogador']}", COR_JOGADOR_X),
        (f"Vit. IA: {stats['vitorias_ia']}", COR_JOGADOR_O),
        (f"Empates: {stats['empates']}", (200,200,200))
    ]

    for i, (txt, cor) in enumerate(linhas_stats):
        desenhar_texto_centralizado(tela, txt, fonte_pequena, cor, 200, 220 + i*40)

    # --- COLUNA DIREITA: TOP JOGADORES ---
    desenhar_texto_centralizado(tela, "Top Jogadores", fonte_media, (255, 215, 0), LARGURA_TELA - 200, 150)
    
    ranking = gerar_ranking()
    
    if not ranking:
        desenhar_texto_centralizado(tela, "Sem dados...", fonte_pequena, (100,100,100), LARGURA_TELA - 200, 220)
    else:
        # Exibe apenas os Top 5
        for i, dados in enumerate(ranking[:5]):
            nome = dados["nome"]
            vitorias = dados["vitorias"]
            taxa = dados["taxa"]
            total = dados["total"]

            # Cores baseadas na posição (Ouro, Prata, Bronze)
            if i == 0: cor_rank = (255, 215, 0)      
            elif i == 1: cor_rank = (192, 192, 192)  
            elif i == 2: cor_rank = (205, 127, 50)   
            else: cor_rank = COR_TEXTO
            
            y_pos = 220 + i * 45 

            # Nome do Jogador (Esquerda da coluna)
            # Trunca nomes muito longos
            nome_exibicao = nome[:10] + ".." if len(nome) > 10 else nome
            surf_nome = fonte_pequena.render(f"{i+1}. {nome_exibicao}", True, cor_rank)
            tela.blit(surf_nome, (LARGURA_TELA//2 + 40, y_pos))

            # Estatísticas (Direita da coluna)
            texto_stats = f"{vitorias}v/{total}j ({taxa}%)"
            
            # Se taxa de vitória > 50%, destaca em verde
            cor_stat = COR_BOTAO_HOVER if taxa >= 50 else cor_rank
            surf_stats = fonte_minuscula.render(texto_stats, True, cor_stat)
            
            tela.blit(surf_stats, (LARGURA_TELA - 40 - surf_stats.get_width(), y_pos + 5))
            
            # Linha separadora sutil
            pygame.draw.line(tela, (40, 45, 60), (LARGURA_TELA//2 + 30, y_pos + 30), (LARGURA_TELA - 30, y_pos + 30), 1)

    botao_voltar = desenhar_botao(tela, "Voltar", LARGURA_TELA//2 - 100, ALTURA_TELA - 80, 200, 50, posicao_mouse)
    return {"VOLTAR_CENTRO": botao_voltar}

def desenhar_entrada_nome(tela, nome_atual):
    """Tela de Input de Nome (Login)."""
    tela.fill(COR_FUNDO)
    desenhar_texto_centralizado(tela, "LOGIN / REGISTRO", fonte_titulo, COR_JOGADOR_O, LARGURA_TELA//2, 120)
    desenhar_texto_centralizado(tela, "Digite seu Nickname:", fonte_pequena, COR_TEXTO, LARGURA_TELA//2, 200)

    rect_input = pygame.Rect(LARGURA_TELA//2 - 200, 260, 400, 60)

    # Verifica se usuário já existe para dar feedback visual
    existe = verificar_usuario(nome_atual) if nome_atual else False
    
    cor_borda = (255, 215, 0) if existe and len(nome_atual) > 0 else (COR_BOTAO_HOVER if len(nome_atual) > 0 else COR_TEXTO)
    msg = "Usuário encontrado!" if existe else "Novo usuário"

    pygame.draw.rect(tela, COR_TABULEIRO_ATIVO, rect_input, border_radius=10)
    pygame.draw.rect(tela, cor_borda, rect_input, 2, border_radius=10)

    texto_exibicao = nome_atual.upper() if nome_atual else "_"
    desenhar_texto_centralizado(tela, texto_exibicao, fonte_media, COR_TEXTO, rect_input.centerx, rect_input.centery)

    botoes = {}
    if len(nome_atual) > 0:
        desenhar_texto_centralizado(tela, msg, fonte_minuscula, cor_borda, LARGURA_TELA//2, 340)
        desenhar_texto_centralizado(tela, "Pressione ENTER", fonte_minuscula, COR_BOTAO_HOVER, LARGURA_TELA//2, 380)
        botoes["ENTER"] = rect_input

    return botoes

def desenhar_entrada_senha(tela, pin_atual, nome_jogador, eh_novo_registro, msg_erro=""):
    """Tela de Input de Senha (PIN)."""
    tela.fill(COR_FUNDO)
    titulo = f"CRIAR SENHA: {nome_jogador}" if eh_novo_registro else f"OLÁ, {nome_jogador}"
    desenhar_texto_centralizado(tela, titulo, fonte_titulo, (255, 215, 0), LARGURA_TELA//2, 120)
    desenhar_texto_centralizado(tela, "Digite PIN (4 números):", fonte_pequena, COR_TEXTO, LARGURA_TELA//2, 200)

    rect_input = pygame.Rect(LARGURA_TELA//2 - 100, 260, 200, 60)
    cor_borda = COR_JOGADOR_X if msg_erro else COR_JOGADOR_O

    pygame.draw.rect(tela, COR_TABULEIRO_ATIVO, rect_input, border_radius=10)
    pygame.draw.rect(tela, cor_borda, rect_input, 2, border_radius=10)

    # Mascara a senha com asteriscos
    mascara = "*" * len(str(pin_atual))
    desenhar_texto_centralizado(tela, mascara, fonte_media, COR_TEXTO, rect_input.centerx, rect_input.centery)

    if msg_erro:
        desenhar_texto_centralizado(tela, msg_erro, fonte_minuscula, COR_JOGADOR_X, LARGURA_TELA//2, 340)

    desenhar_texto_centralizado(tela, "ESC para voltar", fonte_minuscula, (100,100,100), LARGURA_TELA//2, 430)

    return {"ESC": rect_input}
