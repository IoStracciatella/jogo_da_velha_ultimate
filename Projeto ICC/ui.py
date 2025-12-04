import pygame
from settings import *
from scores import load_scores

def draw_button(screen, text, x, y, w, h, mouse_pos):
    # Efeito simples de hover no botão
    rect = pygame.Rect(x, y, w, h)
    color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    
    pygame.draw.rect(screen, color, rect, border_radius=10) # Bordas arredondadas
    
    text_surf = font_medium.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    return rect

def draw_menu(screen, mouse_pos):
    screen.fill(BACKGROUND_COLOR)
    
    # Título
    title_shadow = font_large.render("JOGO DA VELHA", True, (0, 0, 0))
    title = font_large.render("JOGO DA VELHA", True, TEXT_COLOR)
    screen.blit(title_shadow, (WIDTH//2 - title.get_width()//2 + 3, 80 + 3)) # Subi um pouco (era 100)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    
    # Ajustei as alturas (Y) para caber 4 botões
    draw_button(screen, "Jogar", WIDTH//2 - 100, 180, 200, 50, mouse_pos)
    draw_button(screen, "Instruções", WIDTH//2 - 100, 250, 200, 50, mouse_pos) # Novo botão
    draw_button(screen, "Scores", WIDTH//2 - 100, 320, 200, 50, mouse_pos)
    draw_button(screen, "Sair", WIDTH//2 - 100, 390, 200, 50, mouse_pos)

def draw_ultimate_board(screen, game, player_symbol, ai_symbol, mouse_pos):
    screen.fill(BACKGROUND_COLOR)
    
    title = font_large.render("JOGO DA VELHA", True, TEXT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    board_size = 600
    start_x = (WIDTH - board_size) // 2
    start_y = 80
    small_board_size = board_size // 3
    cell_size = small_board_size // 3
    
    # Desenhar cada tabuleiro pequeno
    for big_row in range(3):
        for big_col in range(3):
            board_idx = big_row * 3 + big_col
            board_x = start_x + big_col * small_board_size
            board_y = start_y + big_row * small_board_size
            
            # Destacar fundo do tabuleiro ativo
            if game.next_board == board_idx or (game.next_board is None and game.global_board[board_idx] == ''):
                pygame.draw.rect(screen, ACTIVE_BOARD_BG, 
                               (board_x + 4, board_y + 4, small_board_size - 8, small_board_size - 8), border_radius=5)
            
            # Linhas do tabuleiro pequeno
            for i in range(1, 3):
                pygame.draw.line(screen, GRID_COLOR_SMALL, 
                               (board_x, board_y + i * cell_size), 
                               (board_x + small_board_size, board_y + i * cell_size), 2)
                pygame.draw.line(screen, GRID_COLOR_SMALL, 
                               (board_x + i * cell_size, board_y), 
                               (board_x + i * cell_size, board_y + small_board_size), 2)
            
            # Desenhar Células (X, O e Hover)
            for small_row in range(3):
                for small_col in range(3):
                    cell_x = board_x + small_col * cell_size
                    cell_y = board_y + small_row * cell_size
                    center_x = cell_x + cell_size // 2
                    center_y = cell_y + cell_size // 2
                    
                    # 1. Lógica do HOVER (Visualização da jogada)
                    cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
                    if cell_rect.collidepoint(mouse_pos):
                        # Só mostra hover se for válido
                        if (game.boards[board_idx][small_row][small_col] == '' and 
                            (game.next_board is None or game.next_board == board_idx) and 
                            game.global_board[board_idx] == '' and 
                            not game.game_over and 
                            game.current_player == player_symbol):
                            
                            hover_surf = pygame.Surface((cell_size-4, cell_size-4), pygame.SRCALPHA)
                            hover_surf.fill((255, 255, 255, 20)) # Branco bem transparente
                            screen.blit(hover_surf, (cell_x+2, cell_y+2))

                    # 2. Desenhar Símbolos
                    symbol = game.boards[board_idx][small_row][small_col]
                    if symbol == 'X':
                        text = font_symbol.render("X", True, PLAYER_X_COLOR)
                        text_rect = text.get_rect(center=(center_x, center_y))
                        screen.blit(text, text_rect)
                    elif symbol == 'O':
                        text = font_symbol.render("O", True, PLAYER_O_COLOR)
                        text_rect = text.get_rect(center=(center_x, center_y))
                        screen.blit(text, text_rect)
            
            # Vencedor do tabuleiro pequeno (Overlay Transparente)
            if game.global_board[board_idx] != '':
                s = pygame.Surface((small_board_size, small_board_size), pygame.SRCALPHA)
                winner_char = game.global_board[board_idx]
                
                if winner_char == 'X':
                    s.fill(WINNER_X_BG)
                    color = PLAYER_X_COLOR
                else:
                    s.fill(WINNER_O_BG)
                    color = PLAYER_O_COLOR
                
                screen.blit(s, (board_x, board_y))
                
                # Letra Grande do vencedor
                winner_text = font_winner.render(winner_char, True, (255, 255, 255))
                # Adicionar uma sombra preta para contraste
                winner_shadow = font_winner.render(winner_char, True, (0,0,0))
                
                w_pos = (board_x + small_board_size//2 - winner_text.get_width()//2, 
                         board_y + small_board_size//2 - winner_text.get_height()//2)
                
                screen.blit(winner_shadow, (w_pos[0]+2, w_pos[1]+2))
                screen.blit(winner_text, w_pos)

    # Linhas da Grade Global (Desenhadas por último para ficar por cima)
    for i in range(1, 3):
        # Horizontal
        pygame.draw.line(screen, GRID_COLOR_GLOBAL, 
                       (start_x, start_y + i * small_board_size), 
                       (start_x + board_size, start_y + i * small_board_size), 6)
        # Vertical
        pygame.draw.line(screen, GRID_COLOR_GLOBAL, 
                       (start_x + i * small_board_size, start_y), 
                       (start_x + i * small_board_size, start_y + board_size), 6)

    # Botões de controle
    draw_button(screen, "Voltar", 50, 50, 100, 40, mouse_pos)
    draw_button(screen, "Reiniciar", WIDTH - 150, 50, 120, 40, mouse_pos)
    
    # Barra de Status inferior
    info_y = start_y + board_size + 20
    if not game.game_over:
        if game.current_player == player_symbol: 
            status_text = font_medium.render("Sua vez", True, PLAYER_X_COLOR)
        else: 
            status_text = font_medium.render("IA Pensando...", True, PLAYER_O_COLOR)
    else:
        if game.winner == player_symbol: 
            status_text = font_medium.render("VITÓRIA DO JOGADOR!", True, PLAYER_X_COLOR)
        elif game.winner == ai_symbol: 
            status_text = font_medium.render("VITÓRIA DA IA!", True, PLAYER_O_COLOR)
        else: 
            status_text = font_medium.render("EMPATE!", True, TEXT_COLOR)
            
    screen.blit(status_text, (WIDTH//2 - status_text.get_width()//2, info_y))

def draw_scores(screen, mouse_pos):
    screen.fill(BACKGROUND_COLOR)
    
    title = font_large.render("ESTATÍSTICAS", True, TEXT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    
    scores = load_scores()
    
    # Cards de estatísticas
    player_text = font_medium.render(f"Jogador (X): {scores['player_wins']}", True, PLAYER_X_COLOR)
    ai_text = font_medium.render(f"IA (O): {scores['ai_wins']}", True, PLAYER_O_COLOR)
    draws_text = font_medium.render(f"Empates: {scores['draws']}", True, TEXT_COLOR)
    
    screen.blit(player_text, (WIDTH//2 - player_text.get_width()//2, 180))
    screen.blit(ai_text, (WIDTH//2 - ai_text.get_width()//2, 230))
    screen.blit(draws_text, (WIDTH//2 - draws_text.get_width()//2, 280))
    
    total_games = scores['player_wins'] + scores['ai_wins'] + scores['draws']
    if total_games > 0:
        win_rate = (scores['player_wins'] / total_games) * 100
        rate_text = font_medium.render(f"Taxa de Vitória: {win_rate:.1f}%", True, BUTTON_COLOR)
        screen.blit(rate_text, (WIDTH//2 - rate_text.get_width()//2, 330))
    
    draw_button(screen, "Voltar", 50, 50, 100, 40, mouse_pos)