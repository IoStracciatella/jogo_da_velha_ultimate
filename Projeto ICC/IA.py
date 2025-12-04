import random
from game import JogoDaVelha

class UltimateAI:
    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = 'X' if symbol == 'O' else 'O'
    
    def evaluate_small_board(self, board, player):
        score = 0
        opponent = 'X' if player == 'O' else 'O'
        lines = [[(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)],
                 [(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)],
                 [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]]
        
        for line in lines:
            values = [board[i][j] for i, j in line]
            player_count = values.count(player)
            opponent_count = values.count(opponent)
            empty_count = values.count('')
            
            if player_count == 3: score += 100
            elif player_count == 2 and empty_count == 1: score += 10
            elif player_count == 1 and empty_count == 2: score += 1
            elif opponent_count == 3: score -= 100
            elif opponent_count == 2 and empty_count == 1: score -= 10
            elif opponent_count == 1 and empty_count == 2: score -= 1
        return score
    
    def evaluate_global_board(self, game, player):
        score = 0
        opponent = 'X' if player == 'O' else 'O'
        global_board = game.global_board
        lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        
        for line in lines:
            values = [global_board[i] for i in line]
            player_count = values.count(player)
            opponent_count = values.count(opponent)
            empty_count = values.count('')
            
            if player_count == 3: score += 10000
            elif player_count == 2 and empty_count == 1: score += 1000
            elif player_count == 1 and empty_count == 2: score += 100
            elif opponent_count == 3: score -= 10000
            elif opponent_count == 2 and empty_count == 1: score -= 1000
            elif opponent_count == 1 and empty_count == 2: score -= 100
        return score
    
    def evaluate_position(self, game, player):
        score = self.evaluate_global_board(game, player)
        for board_idx in range(9):
            if game.global_board[board_idx] == '':
                board_score = self.evaluate_small_board(game.boards[board_idx], player)
                if board_idx == 4: score += board_score * 2
                elif board_idx in [0, 2, 6, 8]: score += board_score * 1.5
                else: score += board_score
        
        if game.next_board is not None and game.global_board[game.next_board] == '':
            next_board_score = self.evaluate_small_board(game.boards[game.next_board], player)
            if next_board_score < 0: score -= 50
            else: score += 50
        return score
    
    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.game_over:
            return self.evaluate_position(game, self.symbol)
        
        valid_moves = game.get_valid_moves()
        
        if maximizing_player:
            max_eval = -float('inf')
            for move in valid_moves:
                game_copy = JogoDaVelha()
                game_copy.boards = [[row[:] for row in board] for board in game.boards]
                game_copy.global_board = game.global_board[:]
                game_copy.current_player = game.current_player
                game_copy.next_board = game.next_board
                game_copy.game_over = game.game_over
                game_copy.winner = game.winner
                
                game_copy.make_move(*move)
                eval = self.minimax(game_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                game_copy = JogoDaVelha()
                game_copy.boards = [[row[:] for row in board] for board in game.boards]
                game_copy.global_board = game.global_board[:]
                game_copy.current_player = game.current_player
                game_copy.next_board = game.next_board
                game_copy.game_over = game.game_over
                game_copy.winner = game.winner
                
                game_copy.make_move(*move)
                eval = self.minimax(game_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval
    
    def get_best_move(self, game):
        valid_moves = game.get_valid_moves()
        if not valid_moves: return None
        
        if len(valid_moves) > 20:
            good_moves = []
            for move in valid_moves:
                board_idx, row, col = move
                if board_idx == 4: good_moves.append(move)
                elif board_idx in [0, 2, 6, 8]: good_moves.append(move)
            
            if good_moves:
                return random.choice(good_moves)
        
        best_score = -float('inf')
        best_moves = []
        depth = 2 if len(valid_moves) > 15 else 3
        
        for move in valid_moves:
            game_copy = JogoDaVelha()
            game_copy.boards = [[row[:] for row in board] for board in game.boards]
            game_copy.global_board = game.global_board[:]
            game_copy.current_player = game.current_player
            game_copy.next_board = game.next_board
            game_copy.game_over = game.game_over
            game_copy.winner = game.winner
            
            game_copy.make_move(*move)
            score = self.minimax(game_copy, depth, -float('inf'), float('inf'), False)
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        
        return random.choice(best_moves) if best_moves else random.choice(valid_moves)