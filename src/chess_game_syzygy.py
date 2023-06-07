import chess

import logging
logger = logging.getLogger()

from src.libs.chess_lib import *

import sys
from chess_game import ChessGame

# Specify the path to the local library/module
library_path = "/Users/littlecapa/GIT/python/move_logger/src"

# Add the library path to the system path
sys.path.append(library_path)

from logger import Move_Logger
checkmate_value = 999.0

SYZYGY_PATH = "/Users/littlecapa/chess/Syzygy"

MAX_SYZYGY_PIECES = 5

class ChessSyzygyGame(ChessGame):

    def __init__(self, max_depth=3, extra_depth_capture = 3):
        super.__init__(self, max_depth, extra_depth_capture)
        # Load the Tablebase
        
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