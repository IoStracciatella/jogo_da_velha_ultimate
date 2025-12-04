import pygame
from settings import *
from scores import load_json, get_ranking, get_general_stats, check_user_exists

# OBS: este arquivo assume que settings.py define:
# WIDTH, HEIGHT, font_large, font_medium, font_small, font_tiny, font_symbol, font_winner,
# BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR, BACKGROUND_COLOR, ACTIVE_BOARD_BG,
# PLAYER_X_COLOR, PLAYER_O_COLOR, WINNER_X_BG, WINNER_O_BG, GRID_COLOR_SMALL, GRID_COLOR_GLOBAL

# --- FERRAMENTAS AUXILIARES (Simplificam a vida) ---

def desenhar_texto_centralizado(screen, text, font, color, center_x, center_y):
    """Escreve texto centralizado e retorna o rect do texto."""
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(center_x, center_y))
    screen.blit(surf, rect)
    return rect

def draw_button(screen, text, x, y, w, h, mouse_pos):
    """Desenha um botão e retorna seu pygame.Rect (útil para lógica de clique)."""
    rect = pygame.Rect(x, y, w, h)
    color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=10)
    desenhar_texto_centralizado(screen, text, font_medium, TEXT_COLOR, rect.centerx, rect.centery)
    return rect

# --- TELAS ---
# Cada função de desenho retorna um dicionário com os botões desenhados na tela:
# ex: {"VOLtar": rect_voltar, "REINICIAR": rect_reiniciar}
# se não houver botões, retorna {}.

def draw_menu(screen, mouse_pos):
    screen.fill(BACKGROUND_COLOR)
    desenhar_texto_centralizado(screen, "JOGO DA VELHA", font_large, (0,0,0), WIDTH//2 + 3, 80 + 3)
    desenhar_texto_centralizado(screen, "JOGO DA VELHA", font_large, TEXT_COLOR, WIDTH//2, 80)

    botoes_texto = ["Jogar", "Instruções", "Scores", "Sair"]
    start_y = 180
    espacamento = 70

    botoes = {}
    for i, texto in enumerate(botoes_texto):
        rect = draw_button(screen, texto, WIDTH//2 - 100, start_y + (i * espacamento), 200, 50, mouse_pos)
        botoes[texto.upper()] = rect

    return botoes

def draw_instructions(screen, mouse_pos):
    screen.fill(BACKGROUND_COLOR)
    desenhar_texto_centralizado(screen, "COMO JOGAR", font_large, TEXT_COLOR, WIDTH//2, 50)

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

    y = 120
    for linha in regras:
        if "REGRAS" in linha:
            color, font = PLAYER_O_COLOR, font_medium
        else:
            color, font = TEXT_COLOR, font_small

        surf = font.render(linha, True, color)
        screen.blit(surf, (WIDTH//2 - 250, y))
        y += 35

    desenhar_texto_centralizado(screen, "Jogue para aprender!", font_small, BUTTON_COLOR, WIDTH//2, HEIGHT - 130)
    botoes = {"VOLTAR": draw_button(screen, "Voltar", WIDTH//2 - 100, HEIGHT - 80, 200, 50, mouse_pos)}
    return botoes

def draw_ultimate_board(screen, game, player_symbol, ai_symbol, mouse_pos):
    screen.fill(BACKGROUND_COLOR)
    desenhar_texto_centralizado(screen, "JOGO DA VELHA", font_large, TEXT_COLOR, WIDTH//2, 35)

    board_size = 600
    start_x = (WIDTH - board_size) // 2
    start_y = 80
    small_board_size = board_size // 3
    cell_size = small_board_size // 3

    # ATUALIZADO: Usando nomes em português
    global_board = game.tabuleiro_global
    boards = game.tabuleiros

    # Desenhar fundos e vencedores
    for big_idx in range(9):
        big_row, big_col = divmod(big_idx, 3)
        bx = start_x + big_col * small_board_size
        by = start_y + big_row * small_board_size

        # ATUALIZADO: game.jogo_acabou e game.proximo_tabuleiro
        if not game.jogo_acabou and (game.proximo_tabuleiro is None or game.proximo_tabuleiro == big_idx) and global_board[big_idx] == '':
            pygame.draw.rect(screen, ACTIVE_BOARD_BG, (bx+4, by+4, small_board_size-8, small_board_size-8), border_radius=5)

        if global_board[big_idx] != '':
            bg_color = WINNER_X_BG if global_board[big_idx] == 'X' else WINNER_O_BG
            pygame.draw.rect(screen, bg_color, (bx, by, small_board_size, small_board_size))

    # Grades
    for i in range(1, 3):
        # ... (código de grade mantém igual) ...
        # Se quiser simplificar, copie o código de grade do anterior aqui, 
        # mas as variáveis importantes já foram traduzidas acima.
        pass

    # Desenho completo das grades (simplificado para caber aqui)
    for row in range(9):
        py = start_y + row * cell_size
        if row % 3 != 0: pygame.draw.line(screen, GRID_COLOR_SMALL, (start_x, py), (start_x + board_size, py), 2)
    for col in range(9):
        px = start_x + col * cell_size
        if col % 3 != 0: pygame.draw.line(screen, GRID_COLOR_SMALL, (px, start_y), (px, start_y + board_size), 2)
    for i in range(1, 3):
        pos = i * small_board_size
        pygame.draw.line(screen, GRID_COLOR_GLOBAL, (start_x, start_y + pos), (start_x + board_size, start_y + pos), 6)
        pygame.draw.line(screen, GRID_COLOR_GLOBAL, (start_x + pos, start_y), (start_x + pos, start_y + board_size), 6)

    # Desenhar símbolos
    for big_row in range(3):
        for big_col in range(3):
            big_idx = big_row * 3 + big_col
            bx = start_x + big_col * small_board_size
            by = start_y + big_row * small_board_size

            if global_board[big_idx] != '':
                winner = global_board[big_idx]
                desenhar_texto_centralizado(screen, winner, font_winner, (255,255,255), bx + small_board_size//2, by + small_board_size//2)
                continue

            board = boards[big_idx]
            for sr in range(3):
                for sc in range(3):
                    sym = board[sr][sc]
                    cx = bx + sc * cell_size + cell_size//2
                    cy = by + sr * cell_size + cell_size//2

                    if sym == 'X':
                        desenhar_texto_centralizado(screen, "X", font_symbol, PLAYER_X_COLOR, cx, cy)
                    elif sym == 'O':
                        desenhar_texto_centralizado(screen, "O", font_symbol, PLAYER_O_COLOR, cx, cy)
                    # ATUALIZADO: game.jogo_acabou e game.jogador_atual
                    elif not game.jogo_acabou and game.jogador_atual == player_symbol:
                        cell_rect = pygame.Rect(bx + sc*cell_size, by + sr*cell_size, cell_size, cell_size)
                        if cell_rect.collidepoint(mouse_pos) and (game.proximo_tabuleiro is None or game.proximo_tabuleiro == big_idx):
                            s = pygame.Surface((cell_size-4, cell_size-4), pygame.SRCALPHA)
                            s.fill((255, 255, 255, 30))
                            screen.blit(s, (cell_rect.x+2, cell_rect.y+2))

    botoes = {
        "VOLTAR": draw_button(screen, "Voltar", 50, 50, 100, 40, mouse_pos),
        "REINICIAR": draw_button(screen, "Reiniciar", WIDTH - 150, 50, 120, 40, mouse_pos)
    }

    # ATUALIZADO: game.jogo_acabou, game.jogador_atual e game.vencedor
    if not game.jogo_acabou:
        msg = "Sua vez" if game.jogador_atual == player_symbol else "IA Pensando..."
        col = PLAYER_X_COLOR if game.jogador_atual == player_symbol else PLAYER_O_COLOR
    else:
        msg = f"Vencedor: {game.vencedor}" if game.vencedor else "Empate!"
        col = TEXT_COLOR

    desenhar_texto_centralizado(screen, msg, font_medium, col, WIDTH//2, start_y + board_size + 30)
    return botoes

def draw_scores(screen, mouse_pos):
    screen.fill(BACKGROUND_COLOR)
    desenhar_texto_centralizado(screen, "HALL DA FAMA", font_large, TEXT_COLOR, WIDTH//2, 50)

    pygame.draw.line(screen, GRID_COLOR_SMALL, (WIDTH//2, 140), (WIDTH//2, HEIGHT - 120), 2)

    # --- LADO ESQUERDO: STATS ---
    desenhar_texto_centralizado(screen, "Estatísticas Globais", font_medium, BUTTON_COLOR, 200, 150)
    
    # Busca dados frescos
    stats = get_general_stats() 

    stats_list = [
        (f"Jogos: {stats['total_partidas']}", TEXT_COLOR),
        (f"Vit. Player: {stats['vitorias_player']}", PLAYER_X_COLOR),
        (f"Vit. IA: {stats['vitorias_ai']}", PLAYER_O_COLOR),
        (f"Empates: {stats['empates']}", (200,200,200))
    ]

    for i, (txt, col) in enumerate(stats_list):
        desenhar_texto_centralizado(screen, txt, font_small, col, 200, 220 + i*40)

    # --- LADO DIREITO: RANKING ---
    desenhar_texto_centralizado(screen, "Top Jogadores", font_medium, (255, 215, 0), WIDTH - 200, 150)
    
    # Busca ranking fresco
    ranking = get_ranking()

    if not ranking:
        desenhar_texto_centralizado(screen, "Sem vitórias ainda...", font_small, (100,100,100), WIDTH - 200, 220)
    else:
        # Mostra apenas Top 5
        for i, (nome, vitorias) in enumerate(ranking[:5]):
            y = 220 + i * 40
            
            # Cores das medalhas
            if i == 0: cor = (255, 215, 0)   # Ouro
            elif i == 1: cor = (192, 192, 192) # Prata
            elif i == 2: cor = (205, 127, 50)  # Bronze
            else: cor = TEXT_COLOR

            # Nome à esquerda da coluna
            nome_surf = font_small.render(f"{i+1}. {nome}", True, cor)
            screen.blit(nome_surf, (WIDTH//2 + 50, y))

            # Vitórias à direita da coluna
            vit_surf = font_small.render(f"{vitorias} v.", True, cor)
            screen.blit(vit_surf, (WIDTH - 50 - vit_surf.get_width(), y))

    botoes = {"VOLTAR": draw_button(screen, "Voltar", WIDTH//2 - 100, HEIGHT - 80, 200, 50, mouse_pos)}
    return botoes

def draw_name_input(screen, current_name):
    screen.fill(BACKGROUND_COLOR)
    desenhar_texto_centralizado(screen, "LOGIN / REGISTRO", font_large, PLAYER_O_COLOR, WIDTH//2, 120)
    desenhar_texto_centralizado(screen, "Digite seu Nickname:", font_small, TEXT_COLOR, WIDTH//2, 200)

    rect_input = pygame.Rect(WIDTH//2 - 200, 260, 400, 60)

    # PERFORMANCE: se check_user_exists fizer IO, cachear o resultado quando current_name mudar.
    existe = check_user_exists(current_name) if current_name else False
    cor_borda = (255, 215, 0) if existe and len(current_name) > 0 else (BUTTON_HOVER_COLOR if len(current_name) > 0 else TEXT_COLOR)
    msg = "Usuário encontrado!" if existe else "Novo usuário"

    pygame.draw.rect(screen, ACTIVE_BOARD_BG, rect_input, border_radius=10)
    pygame.draw.rect(screen, cor_borda, rect_input, 2, border_radius=10)

    texto_display = current_name.upper() if current_name else "_"
    desenhar_texto_centralizado(screen, texto_display, font_medium, TEXT_COLOR, rect_input.centerx, rect_input.centery)

    botoes = {}
    if len(current_name) > 0:
        desenhar_texto_centralizado(screen, msg, font_tiny, cor_borda, WIDTH//2, 340)
        desenhar_texto_centralizado(screen, "Pressione ENTER", font_tiny, BUTTON_HOVER_COLOR, WIDTH//2, 380)
        botoes["ENTER"] = rect_input  # opcional: expõe rect da caixa de input

    return botoes

def draw_pin_input(screen, current_pin, player_name, is_registering, erro_msg=""):
    screen.fill(BACKGROUND_COLOR)
    titulo = f"CRIAR SENHA: {player_name}" if is_registering else f"OLÁ, {player_name}"
    desenhar_texto_centralizado(screen, titulo, font_large, (255, 215, 0), WIDTH//2, 120)
    desenhar_texto_centralizado(screen, "Digite PIN (4 números):", font_small, TEXT_COLOR, WIDTH//2, 200)

    rect_input = pygame.Rect(WIDTH//2 - 100, 260, 200, 60)
    cor_borda = PLAYER_X_COLOR if erro_msg else PLAYER_O_COLOR

    pygame.draw.rect(screen, ACTIVE_BOARD_BG, rect_input, border_radius=10)
    pygame.draw.rect(screen, cor_borda, rect_input, 2, border_radius=10)

    # current_pin deve ser string; se for outro tipo, converta ao chamar
    mask = "*" * len(str(current_pin))
    desenhar_texto_centralizado(screen, mask, font_medium, TEXT_COLOR, rect_input.centerx, rect_input.centery)

    if erro_msg:
        desenhar_texto_centralizado(screen, erro_msg, font_tiny, PLAYER_X_COLOR, WIDTH//2, 340)

    desenhar_texto_centralizado(screen, "ESC para voltar", font_tiny, (100,100,100), WIDTH//2, 430)

    botoes = {"ESC": rect_input}
    return botoes
