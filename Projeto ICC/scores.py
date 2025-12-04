import json
import os
from settings import *

# --- FUNÇÕES BÁSICAS DE ARQUIVO ---
def load_json(filename):
    """Carrega um arquivo JSON de forma segura."""
    if not os.path.exists(filename):
        return {} if filename != FILE_MATCHES else []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f: # Adicionado encoding utf-8
            return json.load(f)
    except Exception as e:
        print(f"Erro ao ler {filename}: {e}")
        return {} if filename != FILE_MATCHES else []

def save_json(filename, data):
    """Salva dados em um arquivo JSON."""
    try:
        with open(filename, 'w', encoding='utf-8') as f: # Adicionado encoding utf-8
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar {filename}: {e}")

# --- GERENCIAMENTO DE JOGADORES (players.json) ---
def check_user_exists(name):
    players = load_json(FILE_PLAYERS)
    return name.upper() in players

def verify_pin(name, input_pin):
    players = load_json(FILE_PLAYERS)
    if name.upper() in players:
        return players[name.upper()] == input_pin
    return False

def register_user(name, pin):
    players = load_json(FILE_PLAYERS)
    players[name.upper()] = pin
    save_json(FILE_PLAYERS, players)
    print(f"Usuário {name} registrado com sucesso!")

# --- GERENCIAMENTO DE PARTIDAS ---
def save_full_match(match_id, match_data, moves_list):
    # 1. Salvar Resumo em matches.json
    matches = load_json(FILE_MATCHES)
    if not isinstance(matches, list): matches = [] # Garante que é lista
    
    matches.insert(0, match_data)
    save_json(FILE_MATCHES, matches)
    
    # 2. Salvar Movimentos em moves.json
    all_moves = load_json(FILE_MOVES)
    all_moves[match_id] = moves_list
    save_json(FILE_MOVES, all_moves)
    
    print(f"Partida {match_id} salva! Total de partidas: {len(matches)}")

# --- ESTATÍSTICAS E RANKING ---
def get_general_stats():
    matches = load_json(FILE_MATCHES)
    stats = {"total_partidas": 0, "vitorias_player": 0, "vitorias_ai": 0, "empates": 0}
    
    if not isinstance(matches, list): return stats

    stats["total_partidas"] = len(matches)
    
    for m in matches:
        vencedor = m.get("vencedor", "")
        if vencedor == "X":
            stats["vitorias_player"] += 1
        elif vencedor == "O":
            stats["vitorias_ai"] += 1
        else:
            stats["empates"] += 1     
    return stats

def get_ranking():
    matches = load_json(FILE_MATCHES)
    if not isinstance(matches, list): return []

    ranking = {}
    
    for m in matches:
        # Só conta se o humano (X) ganhou
        if m.get("vencedor") == "X":
            nome = "Desconhecido"
            
            # Tenta pegar o nome de várias formas (compatibilidade)
            if "jogadores" in m and isinstance(m["jogadores"], dict):
                nome = m["jogadores"].get("X", "Desconhecido")
            elif "jogador_nome" in m: # Formato antigo
                nome = m["jogador_nome"]
            
            nome = nome.upper().strip()
            ranking[nome] = ranking.get(nome, 0) + 1
            
    # Retorna lista de tuplas: [('NOME', QTD), ('NOME2', QTD)]
    lista_ordenada = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    return lista_ordenada