import chess

import logging
logger = logging.getLogger()

from src.libs.chess_lib import *

import sys

# Specify the path to the local library/module
library_path = "/Users/littlecapa/GIT/python/move_logger/src"

# Add the library path to the system path
sys.path.append(library_path)

from logger import Move_Logger

piece_values = {
            chess.PAWN: 10.0,
            chess.KNIGHT: 30.0,
            chess.BISHOP: 35.0,
            chess.ROOK: 50.0,
            chess.QUEEN: 90.0
        }

promotion_value = 45.0
check_value = piece_values[chess.PAWN] + 1.0
castle_value = piece_values[chess.PAWN] + 2.0
checkmate_value = 999.0
MIN_MAX_VALUE = float('inf')
capture_value = 2.0

class ChessGame:

    def __init__(self, max_depth=3, extra_depth_capture = 3):
        self.max_depth = max_depth
        self.extra_depth_capture = extra_depth_capture
        self.board = chess.Board()
        self.logger_off()

    def logger_on(self):
        self.logging = True

    def logger_off(self):
        self.logging = False

    def get_logger_data(self):
        if self.logging:
            return self.ml.get_pgn()
        else:
            return "No logger data!"

    def set_board(self, board):
        self.board = board

    def get_board(self):
        return self.board
    
    def setup_from_fen(self, fen):
        self.board.set_fen(fen)

    def make_move(self, move):
        self.board.push(move)

    def get_move_list(self, evaluated = True):
        legal_moves = list(self.board.legal_moves)
        if evaluated:
            legal_moves.sort(key=lambda move: self.evaluate_move(move), reverse=True)
        return legal_moves

    def get_best_move(self):
        if self.logging:
            self.ml = Move_Logger(self.board)
        eval, best_move = self.minimax(self.max_depth, -MIN_MAX_VALUE, MIN_MAX_VALUE,  True)
        return eval, best_move
    
    def evaluate_move(self, move):
        score = 0.0

        # Evaluate captures
        if self.board.is_capture(move):
            captured_piece = self.board.piece_at(move.to_square)
            capturing_piece = self.board.piece_at(move.from_square)
            if captured_piece is not None and capturing_piece is not None:
                if piece_values.get(capturing_piece.piece_type, 0) > piece_values.get(captured_piece.piece_type, 0):
                    score += piece_values.get(captured_piece.piece_type, 0)
                else:
                   score += capture_value 

        # Evaluate promotions
        if move.promotion is not None:
            score += promotion_value

        # Evaluate checkmate
        self.board.push(move)
        if self.board.is_checkmate():
            score += checkmate_value
        if self.board.is_check():
            score += check_value
        if is_castling_move(move):
            score += castle_value

        self.board.pop()
        return float(score)

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate(), None

        best_move = None
        if maximizing_player:
            best_eval = -MIN_MAX_VALUE
        else:
            best_eval = MIN_MAX_VALUE
        for move in self.get_move_list():
            self.board.push(move)
            if self.logging:
                self.ml.make_move(move)
            eval_score, _ = self.minimax(depth - 1, alpha, beta, not maximizing_player)
            if eval_score == checkmate_value:
                logger.debug(f"Move: {move} Scores: {eval_score}, {best_eval}, {alpha}, {beta}")
            self.board.pop()
            if self.logging:
                self.ml.add_eval(eval_score)
                self.ml.take_move_back()
            if maximizing_player:
                if eval_score > best_eval:
                    best_eval = eval_score
                    best_move = move
                    if eval_score >= checkmate_value:
                        break
                alpha = max(alpha, best_eval)
            else:
                if eval_score < best_eval:
                    best_eval = eval_score
                    best_move = move
                    if eval_score <= -checkmate_value:
                        break
                beta = min(beta, best_eval)
            if beta <= alpha:
                break
        return best_eval, best_move
    
    def evaluate(self):
        score = 0
        if self.board.is_game_over():
            if self.board.is_checkmate():
                logger.debug(f"Mate, Turn: {self.board.turn}")
                if self.board.turn == chess.BLACK:
                    score = checkmate_value
                else:
                    score = -checkmate_value
            # else: score = 0
            return score
        
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)

            if piece is not None:
                if piece.color == chess.WHITE:
                    score += piece_values.get(piece.piece_type, 0)
                else:
                    score -= piece_values.get(piece.piece_type, 0)

        return score

    def play(self):
        while not self.board.is_game_over():
            if self.board.turn:
                # Player's turn
                print(self.board)
                user_move = input("Enter your move: ")
                move = chess.Move.from_uci(user_move)
                if move in self.board.legal_moves:
                    self.board.push(move)
                else:
                    print("Invalid move, try again.")
            else:
                # AI's turn
                eval, best_move = self.get_best_move()
                self.board.push(best_move)

        print(self.board.result())

    def cleanup(self):
        pass
