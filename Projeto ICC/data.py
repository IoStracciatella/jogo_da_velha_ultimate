import json
import os
from settings import *

def ler_arquivo(nome_arquivo, valor_padrao):
    #Lê o JSON
    if os.path.exists(nome_arquivo):
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            print(f"Não li o arquivo {nome_arquivo}.")
    return valor_padrao

def salvar_arquivo(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def verificar_usuario(nome):
    #verifica se o nome já existe no banco de dados
    jogadores = ler_arquivo(ARQUIVO_JOGADORES, {})
    return nome.upper() in jogadores

def realizar_login(nome, senha): #verifica se nome e senha batem
    jogadores = ler_arquivo(ARQUIVO_JOGADORES, {})
    nome = nome.upper()
    if nome in jogadores and jogadores[nome] == senha:
        return True
    return False

def registrar_usuario(nome, senha): #criar novo usuario
    jogadores = ler_arquivo(ARQUIVO_JOGADORES, {})
    jogadores[nome.upper()] = senha
    salvar_arquivo(ARQUIVO_JOGADORES, jogadores)
    print(f"Usuário {nome} registrado com sucesso!")
    return True

#SALVAR
def salvar_partida_completa(id_partida, resumo_partida, lista_movimentos):
    #salva para o ranking
    historico = ler_arquivo(ARQUIVO_PARTIDAS, [])
    historico.insert(0, resumo_partida) 
    salvar_arquivo(ARQUIVO_PARTIDAS, historico)

    #salva os movimentos
    todos_movimentos = ler_arquivo(ARQUIVO_MOVIMENTOS, {})
    todos_movimentos[id_partida] = lista_movimentos
    salvar_arquivo(ARQUIVO_MOVIMENTOS, todos_movimentos)
    print("Partida salva com sucesso!")

def obter_estatisticas_gerais(): #vai retornar a contagem total de jogos, vitórias e empates
    partidas = ler_arquivo(ARQUIVO_PARTIDAS, [])
    stats = {
        "total_partidas": len(partidas),
        "vitorias_jogador": 0,
        "vitorias_ia": 0,
        "empates": 0
    }
    
    for p in partidas:
        vencedor = p.get("vencedor", "Empate")
        if vencedor == "X":
            stats["vitorias_jogador"] += 1
        elif vencedor == "O":
            stats["vitorias_ia"] += 1
        else:
            stats["empates"] += 1
            
    return stats

def gerar_ranking(): #lista dos melhores jogadores
    partidas = ler_arquivo(ARQUIVO_PARTIDAS, [])
    placar = {} 

    for p in partidas:
        nome = p.get("jogadores", {}).get("X", "Desconhecido").upper()
        vencedor = p.get("vencedor")

        if nome not in placar:
            placar[nome] = {"vitorias": 0, "total": 0}
        
        placar[nome]["total"] += 1
        
        if vencedor == "X": 
            placar[nome]["vitorias"] += 1

    lista_final = []
    for nome, dados in placar.items():
        taxa_vitoria = 0
        if dados["total"] > 0:
            taxa_vitoria = (dados["vitorias"] / dados["total"]) * 100
            
        lista_final.append({
            "nome": nome,
            "vitorias": dados["vitorias"],
            "total": dados["total"],
            "taxa": round(taxa_vitoria, 1)
        })

    return sorted(lista_final, key=lambda x: x["vitorias"], reverse=True)