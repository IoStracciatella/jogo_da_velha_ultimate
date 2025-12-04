import pygame
import sys
from datetime import datetime
from settings import *
from game import JogoDaVelha
from IA import UltimateAI
from ui import draw_menu, draw_ultimate_board, draw_scores, draw_instructions, draw_name_input, draw_pin_input
from scores import save_full_match, check_user_exists, verify_pin, register_user

# Inicialização
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)

# Configurar Jogo
game = JogoDaVelha()
ai_symbol = 'O'
player_symbol = 'X'
ai = UltimateAI(ai_symbol)

# Variáveis Globais
current_state = GameState.MENU
running = True
ai_thinking = False
score_update_pending = False
game_start_time = None
player_name = ""
player_pin = ""
is_registering_pin = False
pin_error_message = ""

def make_ai_move():
    # ATUALIZADO: game.jogo_acabou e game.jogador_atual
    if not game.jogo_acabou and game.jogador_atual == ai_symbol:
        move = ai.get_best_move(game)
        if move:
            # ATUALIZADO: game.fazer_jogada
            game.fazer_jogada(*move)

def criar_areas_de_clique():
    lista_clicavel = []
    board_size = 600
    start_x = (WIDTH - board_size) // 2
    start_y = 80
    small_board_size = board_size // 3
    cell_size = small_board_size // 3
    
    for big_row in range(3):
        for big_col in range(3):
            big_idx = big_row * 3 + big_col
            big_x = start_x + big_col * small_board_size
            big_y = start_y + big_row * small_board_size
            
            for small_row in range(3):
                for small_col in range(3):
                    cell_x = big_x + small_col * cell_size
                    cell_y = big_y + small_row * cell_size
                    
                    retangulo = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
                    lista_clicavel.append((retangulo, big_idx, small_row, small_col))
    return lista_clicavel

def criar_botoes_menu():
    botoes = {}
    center_x = WIDTH // 2
    half_width = 100 
    h = 50 
    
    botoes['JOGAR']      = pygame.Rect(center_x - half_width, 180, 200, h)
    botoes['INSTRUCOES'] = pygame.Rect(center_x - half_width, 250, 200, h)
    botoes['SCORES']     = pygame.Rect(center_x - half_width, 320, 200, h)
    botoes['SAIR']       = pygame.Rect(center_x - half_width, 390, 200, h)
    
    botoes['VOLTAR_CENTRO'] = pygame.Rect(center_x - half_width, HEIGHT - 80, 200, 50)
    botoes['VOLTAR_CANTO']  = pygame.Rect(50, 50, 100, 40)
    botoes['REINICIAR']     = pygame.Rect(WIDTH - 150, 50, 120, 40)
    
    return botoes

# --- PREPARAÇÃO ---
areas_do_tabuleiro = criar_areas_de_clique()
meus_botoes = criar_botoes_menu()

# --- LOOP PRINCIPAL ---
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             running = False

        if event.type == pygame.KEYDOWN:
            if current_state == GameState.NOME:
                if event.key == pygame.K_RETURN:
                    if len(player_name) > 0:
                        user_exists = check_user_exists(player_name)
                        current_state = GameState.SENHA
                        player_pin = "" 
                        pin_error_message = ""
                        is_registering_pin = not user_exists
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 12: player_name += event.unicode

            elif current_state == GameState.SENHA:
                if event.key == pygame.K_ESCAPE:
                    current_state = GameState.NOME
                    pin_error_message = ""
                elif event.key == pygame.K_RETURN:
                    if len(player_pin) == 4:
                        if is_registering_pin:
                            register_user(player_name, player_pin)
                            current_state = GameState.JOGO
                            # ATUALIZADO: reiniciar_jogo
                            game.reiniciar_jogo()
                            game_start_time = datetime.now()
                        else:
                            if verify_pin(player_name, player_pin):
                                current_state = GameState.JOGO
                                # ATUALIZADO: reiniciar_jogo
                                game.reiniciar_jogo()
                                game_start_time = datetime.now()
                            else:
                                pin_error_message = "SENHA INCORRETA!"
                                player_pin = "" 
                elif event.key == pygame.K_BACKSPACE:
                    player_pin = player_pin[:-1]
                elif event.unicode.isnumeric() and len(player_pin) < 4:
                    player_pin += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == GameState.MENU:
                if meus_botoes['JOGAR'].collidepoint(mouse_pos):
                    current_state = GameState.NOME
                    player_name = "" 
                    score_update_pending = False
                elif meus_botoes['INSTRUCOES'].collidepoint(mouse_pos):
                    current_state = GameState.INSTRUCOES
                elif meus_botoes['SCORES'].collidepoint(mouse_pos):
                    current_state = GameState.SCORES
                elif meus_botoes['SAIR'].collidepoint(mouse_pos):
                    running = False
            
            elif current_state in [GameState.INSTRUCOES, GameState.SCORES]:
                if meus_botoes['VOLTAR_CENTRO'].collidepoint(mouse_pos):
                    current_state = GameState.MENU

            elif current_state == GameState.JOGO:
                if meus_botoes['VOLTAR_CANTO'].collidepoint(mouse_pos):
                    current_state = GameState.MENU
                    score_update_pending = False
                elif meus_botoes['REINICIAR'].collidepoint(mouse_pos):
                    # ATUALIZADO: reiniciar_jogo
                    game.reiniciar_jogo()
                    ai_thinking = False
                    score_update_pending = False
                
                # CLIQUE NO TABULEIRO
                # ATUALIZADO: game.jogo_acabou e game.jogador_atual
                elif not game.jogo_acabou and game.jogador_atual == player_symbol:
                    for retangulo, board_idx, row, col in areas_do_tabuleiro:
                        if retangulo.collidepoint(mouse_pos):
                            # ATUALIZADO: game.proximo_tabuleiro
                            if game.proximo_tabuleiro is None or game.proximo_tabuleiro == board_idx:
                                # ATUALIZADO: game.fazer_jogada
                                if game.fazer_jogada(board_idx, row, col):
                                    ai_thinking = True
                            break 

    # IA Logic
    # ATUALIZADO: game.jogo_acabou e game.jogador_atual
    if current_state == GameState.JOGO and not game.jogo_acabou and game.jogador_atual == ai_symbol:
        if not ai_thinking: ai_thinking = True
        elif ai_thinking:
            pygame.time.delay(500)
            make_ai_move()
            ai_thinking = False

    # Salvar Score
    # ATUALIZADO: game.jogo_acabou e game.pontuacao_salva
    if current_state == GameState.JOGO and game.jogo_acabou and not game.pontuacao_salva:
        duration = 0
        if game_start_time:
            end_time = datetime.now()
            duration = (end_time - game_start_time).total_seconds()
        
        match_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # ATUALIZADO: game.vencedor e game.historico_jogadas
        match_summary = {
            "id_partida": match_id,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "duracao_segundos": round(duration, 2),
            "jogadores": { "X": player_name.upper(), "O": "IA Ultimate" },
            "vencedor": game.vencedor if game.vencedor else "Empate",
            "total_jogadas": len(game.historico_jogadas),
            "status": "FINALIZADO"
        }

        moves_list = game.historico_jogadas
        score_update_pending = True
        game.pontuacao_salva = True # ATUALIZADO
        
        pygame.time.delay(500)
        save_full_match(match_id, match_summary, moves_list)
        score_update_pending = False

    # Desenho
    if current_state == GameState.MENU: draw_menu(screen, mouse_pos)
    elif current_state == GameState.JOGO: draw_ultimate_board(screen, game, player_symbol, ai_symbol, mouse_pos)
    elif current_state == GameState.SCORES: draw_scores(screen, mouse_pos)
    elif current_state == GameState.INSTRUCOES: draw_instructions(screen, mouse_pos)
    elif current_state == GameState.NOME: draw_name_input(screen, player_name)
    elif current_state == GameState.SENHA: draw_pin_input(screen, player_pin, player_name.upper(), is_registering_pin, pin_error_message)
    
    pygame.display.flip()

pygame.quit()
sys.exit()