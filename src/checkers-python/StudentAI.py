from random import randint
from BoardClasses import Move, Board
import copy

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.depth = 5 # look ahead depth
        self.previous_boards = {}  # Track past board states


    # returns best move 
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        
        # convert board state to a hashable string
        board_state = str(self.board.board)

        # if board has been seen before, add a penalty
        if board_state in self.previous_boards:
            self.previous_boards[board_state] += 1
        else:
            self.previous_boards[board_state] = 1

        
        best_move = self.minimax(self.board, self.depth, True, float('-inf'), float('inf'))[-1]
        self.board.make_move(best_move, self.color)
        return best_move

    # minimax algorithm with alpha bera pruning
    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if depth == 0 or board.is_win(self.color) != 0:
            return self.evaluate_board(board), None
        
        moves = board.get_all_possible_moves(self.color if is_maximizing else self.opponent[self.color])
        best_move = None

        if is_maximizing:
            max_eval = float('-inf')
            for move_list in moves:
                for move in move_list:
                    new_board = copy.deepcopy(board)
                    new_board.make_move(move, self.color)
                    
                    eval_score = self.minimax(new_board, depth -1, False, alpha, beta)[0]
                    
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_move = move
                    alpha = max(alpha, eval_score)
                    
                    if beta <= alpha:
                        break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move_list in moves:
                for move in move_list:
                    new_board = copy.deepcopy(board)
                    new_board.make_move(move, self.opponent[self.color])

                    eval_score = self.minimax(new_board, depth - 1, True, alpha, beta)[0]

                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_move = move

                    beta = min(beta, eval_score)

                    if beta <= alpha:
                        break
            return min_eval, best_move
    
    # heuristic func. to evaluate board state
    def evaluate_board(self, board):
        win_status = board.is_win(self.color)

        if win_status == self.color:
            return 1000 # win state 
        elif win_status == self.opponent[self.color]:
            return -1000 # loose state
        
        ai_pieces, opp_pieces = 0,0
        for row in range(self.row):
            for col in range(self.col):
                piece = board.board[row][col]

                if piece:
                    # piece value
                    piece_value = 5 if piece.is_king else 1

                    # center control bonus
                    position_value = (self.row - abs(row - self.row // 2)) * 0.2

                    # edge penalty (discourage weak edge pieces)
                    edge_penalty = -0.3 if col == 0 or col == self.col - 1 else 0

                    # encourage forward movement
                    direction_bonus = 0.5 if (piece.color == 'W' and row < self.row // 2) or (piece.color == 'B' and row > self.row // 2) else 0

                    # add to AI or opponent score
                    if piece.color == ('W' if self.color == 2 else 'B'):
                        ai_pieces += piece_value + position_value + edge_penalty + direction_bonus
                    else:
                        opp_pieces += piece_value + position_value + edge_penalty + direction_bonus
            
        # add a penalty for repetition (avoid loops)
        board_state = str(board.board)
        repetition_penalty = -5 * self.previous_boards.get(board_state, 0)
        
        return ai_pieces - opp_pieces + repetition_penalty # higher score is better for AI


