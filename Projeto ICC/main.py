import pygame
import sys
from settings import *
from game import JogoDaVelha
from IA import UltimateAI
from scores import update_score
from ui import draw_menu, draw_ultimate_board, draw_scores

# Inicialização
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)

# Configurar Jogo
game = JogoDaVelha()
ai_symbol = 'O'
player_symbol = 'X'
ai = UltimateAI(ai_symbol)

current_state = GameState.MENU
running = True
ai_thinking = False
score_update_pending = False
score_result = None

def make_ai_move():
    if not game.game_over and game.current_player == ai_symbol:
        move = ai.get_best_move(game)
        if move:
            game.make_move(*move)

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # --- Lógica do Menu ---
            if current_state == GameState.MENU:
                # Jogar
                if WIDTH//2 - 100 <= mouse_pos[0] <= WIDTH//2 + 100 and 200 <= mouse_pos[1] <= 250:
                    current_state = GameState.JOGO
                    game.reset_game()
                    ai_thinking = False
                    score_update_pending = False
                # Scores
                elif WIDTH//2 - 100 <= mouse_pos[0] <= WIDTH//2 + 100 and 270 <= mouse_pos[1] <= 320:
                    current_state = GameState.SCORES
                # Sair
                elif WIDTH//2 - 100 <= mouse_pos[0] <= WIDTH//2 + 100 and 340 <= mouse_pos[1] <= 390:
                    running = False
            
            # --- Lógica do Jogo ---
            elif current_state == GameState.JOGO:
                # Voltar
                if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 90:
                    current_state = GameState.MENU
                    score_update_pending = False
                # Reiniciar
                elif WIDTH - 150 <= mouse_pos[0] <= WIDTH - 50 and 50 <= mouse_pos[1] <= 90:
                    game.reset_game()
                    ai_thinking = False
                    score_update_pending = False
                
                # Clique no tabuleiro
                elif not game.game_over and game.current_player == player_symbol:
                    board_size = 600
                    start_x = (WIDTH - board_size) // 2
                    start_y = 80
                    small_board_size = board_size // 3
                    cell_size = small_board_size // 3
                    
                    for big_row in range(3):
                        for big_col in range(3):
                            board_idx = big_row * 3 + big_col
                            board_x = start_x + big_col * small_board_size
                            board_y = start_y + big_row * small_board_size
                            
                            if (board_x <= mouse_pos[0] <= board_x + small_board_size and
                                board_y <= mouse_pos[1] <= board_y + small_board_size):
                                
                                if game.next_board is None or game.next_board == board_idx:
                                    rel_x = mouse_pos[0] - board_x
                                    rel_y = mouse_pos[1] - board_y
                                    small_col = rel_x // cell_size
                                    small_row = rel_y // cell_size
                                    
                                    if 0 <= small_row < 3 and 0 <= small_col < 3:
                                        if game.make_move(board_idx, int(small_row), int(small_col)):
                                            ai_thinking = True
            
            # --- Lógica de Scores ---
            elif current_state == GameState.SCORES:
                if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 90:
                    current_state = GameState.MENU

    # IA Logic
    if current_state == GameState.JOGO and not game.game_over and game.current_player == ai_symbol and ai_thinking:
        pygame.time.delay(500)
        make_ai_move()
        ai_thinking = False
    
    if current_state == GameState.JOGO and not game.game_over and game.current_player == ai_symbol and not ai_thinking:
        ai_thinking = True

    # Salvar Score
    if current_state == GameState.JOGO and game.game_over and not game.score_saved:
        if game.winner == player_symbol: score_result = "player"
        elif game.winner == ai_symbol: score_result = "ai"
        else: score_result = "draw"
        score_update_pending = True
        game.score_saved = True

    if score_update_pending:
        pygame.time.delay(1000)
        update_score(score_result)
        score_update_pending = False

# ... resto do código do main.py ...

    # Desenho (ATUALIZADO PARA INCLUIR mouse_pos)
    if current_state == GameState.MENU:
        draw_menu(screen, mouse_pos)
        
    elif current_state == GameState.JOGO:
        # Passamos mouse_pos aqui para fazer o efeito de hover funcionar
        draw_ultimate_board(screen, game, player_symbol, ai_symbol, mouse_pos)
        
    elif current_state == GameState.SCORES:
        draw_scores(screen, mouse_pos)
    
    pygame.display.flip()

pygame.quit()
sys.exit()