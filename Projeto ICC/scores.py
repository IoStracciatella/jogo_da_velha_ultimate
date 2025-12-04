import json
import os

SCORE_FILE = "ultimate_scores.json"

def load_scores():
    """Carrega os scores do arquivo JSON"""
    try:
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, 'r') as f:
                scores = json.load(f)
                if "player_wins" not in scores: scores["player_wins"] = 0
                if "ai_wins" not in scores: scores["ai_wins"] = 0
                if "draws" not in scores: scores["draws"] = 0
                return scores
        else:
            default_scores = {"player_wins": 0, "ai_wins": 0, "draws": 0}
            save_scores(default_scores)
            return default_scores
    except Exception as e:
        print(f"Erro ao carregar scores: {e}")
        return {"player_wins": 0, "ai_wins": 0, "draws": 0}

def save_scores(scores):
    """Salva os scores no arquivo JSON"""
    try:
        with open(SCORE_FILE, 'w') as f:
            json.dump(scores, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar scores: {e}")

def update_score(result):
    """Atualiza os scores baseado no resultado"""
    scores = load_scores()
    
    if result == "player":
        scores["player_wins"] += 1
    elif result == "ai":
        scores["ai_wins"] += 1
    elif result == "draw":
        scores["draws"] += 1
    
    save_scores(scores)