import pygame
import sys
from datetime import datetime
from settings import *
from game import JogoDaVelha
from IA import InteligenciaArtificial
from ui import (
    desenhar_menu, 
    desenhar_tabuleiro_ultimate, 
    desenhar_placar, 
    desenhar_instrucoes, 
    desenhar_entrada_nome, 
    desenhar_entrada_senha,
    desenhar_fim_de_jogo
)
from data import salvar_partida_completa, realizar_login, registrar_usuario

pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(TITULO_JANELA)

jogo = JogoDaVelha()
simbolo_ia = 'O'
simbolo_jogador = 'X'
inteligencia_artificial = InteligenciaArtificial(simbolo_ia)

estado_atual = EstadoJogo.MENU
jogo_rodando = True
ia_pensando = False
atualizacao_pendente = False
momento_inicio_partida = None

#login
nome_jogador = ""
senha_jogador = ""
estamos_registrando_senha = False
mensagem_erro_senha = ""

def realizar_jogada_ia():
    #verifica se o jogo não acabou e se é a vez da IA
    if not jogo.jogo_acabou and jogo.jogador_atual == simbolo_ia:
        movimento = inteligencia_artificial.obter_melhor_jogada(jogo)
        if movimento:
            jogo.fazer_jogada(*movimento)

def criar_areas_de_clique_tabuleiro():
    """
    aqui vai gerar retângulos de colisão para cada célula do tabuleiro e retonar
    uma lista de tuplas
    """
    lista_clicavel = []
    tamanho_tabuleiro = 600
    inicio_x = (LARGURA_TELA - tamanho_tabuleiro) // 2
    inicio_y = 80
    
    tamanho_pequeno = tamanho_tabuleiro // 3
    tamanho_celula = tamanho_pequeno // 3
    
    for linha_g in range(3):
        for col_g in range(3):
            indice = linha_g * 3 + col_g
            pos_x_grande = inicio_x + col_g * tamanho_pequeno
            pos_y_grande = inicio_y + linha_g * tamanho_pequeno
            
            for linha_p in range(3):
                for col_p in range(3):
                    pos_x_celula = pos_x_grande + col_p * tamanho_celula
                    pos_y_celula = pos_y_grande + linha_p * tamanho_celula
                    
                    retangulo = pygame.Rect(pos_x_celula, pos_y_celula, tamanho_celula, tamanho_celula)
                    lista_clicavel.append((retangulo, indice, linha_p, col_p))
    return lista_clicavel

def criar_botoes_interacao():
    #cliques do botão
    botoes = {}
    centro_x = LARGURA_TELA // 2
    meia_largura = 100 
    altura = 50 
    
    #menu
    botoes['JOGAR']      = pygame.Rect(centro_x - meia_largura, 180, 200, altura)
    botoes['INSTRUCOES'] = pygame.Rect(centro_x - meia_largura, 250, 200, altura)
    botoes['SCORES']     = pygame.Rect(centro_x - meia_largura, 320, 200, altura) # Vai para o RANKING
    botoes['SAIR']       = pygame.Rect(centro_x - meia_largura, 390, 200, altura)
    
    #do jogo
    botoes['VOLTAR_CENTRO'] = pygame.Rect(centro_x - meia_largura, ALTURA_TELA - 80, 200, 50)
    botoes['VOLTAR_CANTO']  = pygame.Rect(50, 50, 100, 40)
    botoes['REINICIAR']     = pygame.Rect(LARGURA_TELA - 150, 50, 120, 40)
    
    botoes['GO_JOGAR'] = pygame.Rect(centro_x - 120, ALTURA_TELA - 180, 250, 60)
    botoes['GO_MENU']  = pygame.Rect(centro_x - 120, ALTURA_TELA - 110, 240, 50)

    return botoes


areas_do_tabuleiro = criar_areas_de_clique_tabuleiro()
meus_botoes = criar_botoes_interacao()

#LOOP PRINCIPAL
while jogo_rodando:
    posicao_mouse = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
             jogo_rodando = False

        if evento.type == pygame.KEYDOWN:
            
            #digitar NOME
            if estado_atual == EstadoJogo.NOME:
                if evento.key == pygame.K_RETURN:
                    if len(nome_jogador) > 0:
                        #senha
                        estado_atual = EstadoJogo.SENHA
                        senha_jogador = "" 
                        mensagem_erro_senha = ""
                elif evento.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]
                else:
                    if len(nome_jogador) < 12: nome_jogador += evento.unicode

            #SENHA
            elif estado_atual == EstadoJogo.SENHA:
                if evento.key == pygame.K_ESCAPE:
                    estado_atual = EstadoJogo.NOME
                    mensagem_erro_senha = ""
                elif evento.key == pygame.K_RETURN:
                    if len(senha_jogador) == 4:
                        if realizar_login(nome_jogador, senha_jogador):
                            estado_atual = EstadoJogo.JOGANDO
                            jogo.reiniciar_jogo()
                            momento_inicio_partida = datetime.now()
                        else:

                            if registrar_usuario(nome_jogador, senha_jogador):
                                estado_atual = EstadoJogo.JOGANDO
                                jogo.reiniciar_jogo()
                                momento_inicio_partida = datetime.now()
                            else:
                                mensagem_erro_senha = "SENHA INCORRETA"
                                senha_jogador = ""
                                
                elif evento.key == pygame.K_BACKSPACE:
                    senha_jogador = senha_jogador[:-1]
                elif evento.unicode.isnumeric() and len(senha_jogador) < 4:
                    senha_jogador += evento.unicode

        #CLIQUES
        if evento.type == pygame.MOUSEBUTTONDOWN:
            
            if estado_atual == EstadoJogo.MENU:
                if meus_botoes['JOGAR'].collidepoint(posicao_mouse):
                    estado_atual = EstadoJogo.NOME
                    nome_jogador = "" 
                    atualizacao_pendente = False
                elif meus_botoes['INSTRUCOES'].collidepoint(posicao_mouse):
                    estado_atual = EstadoJogo.INSTRUCOES
                elif meus_botoes['SCORES'].collidepoint(posicao_mouse):
                    estado_atual = EstadoJogo.RANKING
                elif meus_botoes['SAIR'].collidepoint(posicao_mouse):
                    jogo_rodando = False
            
            #Botão voltar
            elif estado_atual in [EstadoJogo.INSTRUCOES, EstadoJogo.RANKING]:
                if meus_botoes['VOLTAR_CENTRO'].collidepoint(posicao_mouse):
                    estado_atual = EstadoJogo.MENU

            #JOGO
            elif estado_atual == EstadoJogo.JOGANDO:
                if meus_botoes['VOLTAR_CANTO'].collidepoint(posicao_mouse):
                    estado_atual = EstadoJogo.MENU
                    atualizacao_pendente = False
                elif meus_botoes['REINICIAR'].collidepoint(posicao_mouse):
                    jogo.reiniciar_jogo()
                    ia_pensando = False
                    atualizacao_pendente = False
                
                #clique nas células do tabuleiro
                elif not jogo.jogo_acabou and jogo.jogador_atual == simbolo_jogador:
                    for retangulo, idx_tab, linha, coluna in areas_do_tabuleiro:
                        if retangulo.collidepoint(posicao_mouse):
                            #verifica se o clique foi num tabuleiro válido
                            if jogo.proximo_tabuleiro_foco is None or jogo.proximo_tabuleiro_foco == idx_tab:
                                if jogo.fazer_jogada(idx_tab, linha, coluna):
                                    ia_pensando = True
                            break 
            
            #FIM DE JOGO
            elif estado_atual == EstadoJogo.FIM:
                if meus_botoes['GO_JOGAR'].collidepoint(posicao_mouse):
                    #reinicia e joga direto
                    jogo.reiniciar_jogo()
                    momento_inicio_partida = datetime.now()
                    estado_atual = EstadoJogo.JOGANDO
                    ia_pensando = False
                elif meus_botoes['GO_MENU'].collidepoint(posicao_mouse):
                    #volta pro menu
                    estado_atual = EstadoJogo.MENU

    #IA
    if estado_atual == EstadoJogo.JOGANDO and not jogo.jogo_acabou and jogo.jogador_atual == simbolo_ia:
        if not ia_pensando: 
            ia_pensando = True
        elif ia_pensando:
            #delay na ia
            pygame.time.delay(1000)
            realizar_jogada_ia()
            ia_pensando = False

    #salvamento no final
    if estado_atual == EstadoJogo.JOGANDO and jogo.jogo_acabou and not jogo.pontuacao_salva:
        duracao = 0
        if momento_inicio_partida:
            fim_jogo = datetime.now()
            duracao = (fim_jogo - momento_inicio_partida).total_seconds()
        
        id_partida = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        resumo_partida = {
            "id_partida": id_partida,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "duracao_segundos": round(duracao, 2),
            "jogadores": { "X": nome_jogador.upper(), "O": "IA" },
            "vencedor": jogo.vencedor if jogo.vencedor else "Empate",
            "total_jogadas": len(jogo.historico_jogadas),
            "status": "FINALIZADO"
        }

        lista_movimentos = jogo.historico_jogadas
        atualizacao_pendente = True
        jogo.pontuacao_salva = True 
        
        desenhar_tabuleiro_ultimate(tela, jogo, simbolo_jogador, simbolo_ia, posicao_mouse)
        pygame.display.flip()
        pygame.time.delay(1000)
        salvar_partida_completa(id_partida, resumo_partida, lista_movimentos)

        #vai para a tela de Game Over
        estado_atual = EstadoJogo.FIM
        atualizacao_pendente = False

    #DESENHO NA TELA
    if estado_atual == EstadoJogo.MENU:
        desenhar_menu(tela, posicao_mouse)
    elif estado_atual == EstadoJogo.JOGANDO:
        desenhar_tabuleiro_ultimate(tela, jogo, simbolo_jogador, simbolo_ia, posicao_mouse)
    elif estado_atual == EstadoJogo.RANKING:
        desenhar_placar(tela, posicao_mouse)
    elif estado_atual == EstadoJogo.INSTRUCOES:
        desenhar_instrucoes(tela, posicao_mouse)
    elif estado_atual == EstadoJogo.NOME:
        desenhar_entrada_nome(tela, nome_jogador)
    elif estado_atual == EstadoJogo.SENHA:
        #decide se mostra "Criar Senha" baseado se o login já existe
        usuario_ja_existe = realizar_login(nome_jogador, "") 
        desenhar_entrada_senha(tela, senha_jogador, nome_jogador.upper(), not usuario_ja_existe, mensagem_erro_senha)
    elif estado_atual == EstadoJogo.FIM:
        desenhar_fim_de_jogo(tela, jogo.vencedor, posicao_mouse)


    pygame.display.flip()

pygame.quit()
sys.exit()