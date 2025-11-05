from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math

class StudentAI():
    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2
        self.max_depth = 3  # Adjust based on performance needs

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        
        # Get all possible moves
        moves = self.board.get_all_possible_moves(self.color)
        
        # If only one move available, take it
        if len(moves) == 1 and len(moves[0]) == 1:
            chosen_move = moves[0][0]
        else:
            # Use minimax to find best move
            best_score = -math.inf
            best_move = None
            
            for move_list in moves:
                for move_option in move_list:
                    # Make the move
                    self.board.make_move(move_option, self.color)
                    
                    # Evaluate the position
                    score = self.minimax(self.max_depth - 1, False, -math.inf, math.inf)
                    
                    # Undo the move
                    self.board.undo()
                    
                    # Update best move
                    if score > best_score:
                        best_score = score
                        best_move = move_option
            
            chosen_move = best_move if best_move else moves[0][0]
        
        self.board.make_move(chosen_move, self.color)
        return chosen_move

    def minimax(self, depth, maximizing_player, alpha, beta):
        # Base case: reached maximum depth or game over
        if depth == 0 or self.board.is_win(self.color if maximizing_player else self.opponent[self.color]) != 0:
            return self.evaluate_board()
        
        current_color = self.color if maximizing_player else self.opponent[self.color]
        moves = self.board.get_all_possible_moves(current_color)
        
        if maximizing_player:
            max_eval = -math.inf
            for move_list in moves:
                for move_option in move_list:
                    self.board.make_move(move_option, current_color)
                    eval_score = self.minimax(depth - 1, False, alpha, beta)
                    self.board.undo()
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = math.inf
            for move_list in moves:
                for move_option in move_list:
                    self.board.make_move(move_option, current_color)
                    eval_score = self.minimax(depth - 1, True, alpha, beta)
                    self.board.undo()
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval

    def evaluate_board(self):
        """
        Evaluate the current board state from the perspective of the current player.
        Higher scores are better for the current player.
        """
        score = 0
        piece_weight = 1
        king_weight = 2
        mobility_weight = 0.1
        positional_weight = 0.05
        
        # Count pieces and evaluate positions
        for i in range(self.row):
            for j in range(self.col):
                checker = self.board.board[i][j]
                if checker.color != '.':
                    # Base piece value
                    value = piece_weight
                    if checker.is_king:
                        value = king_weight
                    
                    # Positional advantage - kings in center, regular pieces advancing
                    if checker.is_king:
                        # Kings are better in center
                        center_distance = abs(i - self.row/2) + abs(j - self.col/2)
                        positional_bonus = (self.row + self.col) / 2 - center_distance
                    else:
                        # Regular pieces get bonus for being closer to promotion
                        if checker.color == 'B':  # Black moves downward
                            positional_bonus = i / self.row
                        else:  # White moves upward
                            positional_bonus = (self.row - i - 1) / self.row
                    
                    value += positional_bonus * positional_weight
                    
                    # Add or subtract based on piece color
                    if checker.color == ('B' if self.color == 1 else 'W'):
                        score += value
                    else:
                        score -= value
        
        # Mobility bonus - more moves are better
        my_moves = len(self.board.get_all_possible_moves(self.color))
        opponent_moves = len(self.board.get_all_possible_moves(self.opponent[self.color]))
        score += (my_moves - opponent_moves) * mobility_weight
        
        return score

if __name__ == "__main__":
    import sys
    col = int(sys.argv[1])
    row = int(sys.argv[2])
    p = int(sys.argv[3])
    ai = StudentAI(col, row, p)

    while True:
        move_str = sys.stdin.readline().strip()
        if move_str == "":
            continue

        if move_str == "(-1,-1)":
            move = Move([])
        else:
            move = Move.from_str(move_str)

        our_move = ai.get_move(move)
        print(our_move)
        sys.stdout.flush()