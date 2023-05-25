import chess

import logging
logger = logging.getLogger()

from src.libs.chess_lib import *

piece_values = {
            chess.PAWN: 10,
            chess.KNIGHT: 30,
            chess.BISHOP: 35,
            chess.ROOK: 50,
            chess.QUEEN: 90
        }

promotion_value = 45
check_value = 1
castle_value = 2
checkmate_value = 999
capture_value = 2

class ChessGame:

    def __init__(self, max_depth=3, extra_depth_capture = 3):
        self.max_depth = max_depth
        self.extra_depth_capture = extra_depth_capture
        self.board = chess.Board()

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
        best_move = None
        logger.debug(f'New best move: NONE')
        best_score = float("-inf")

        legal_moves = self.get_move_list(evaluated=True)
        logger.debug(f'LEN: {len(legal_moves)}')
        for move in legal_moves:
            logger.debug(f'Move in Loop: {move}')
            self.board.push(move)
            score = self.minimax(self.max_depth, float("-inf"), float("inf"), False)
            logger.debug(f'Score: {score}')
            self.board.pop()

            if score > best_score:
                logger.debug(f'New best move: {move}')
                best_score = score
                best_move = move

        return best_move
    

    def evaluate_move(self, move):
        score = 0

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

        return score

    def minimax(self, depth, alpha, beta, is_maximizing):
        if depth == 0:
            return self.evaluate()

        if is_maximizing:
            max_eval = float("-inf")

            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board.pop()

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    break

            return max_eval
        else:
            min_eval = float("inf")

            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board.pop()

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    break

            return min_eval

    def evaluate(self):

        score = 0

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
                best_move = self.get_best_move()
                self.board.push(best_move)

        print(self.board.result())

    def cleanup(self):
        pass
