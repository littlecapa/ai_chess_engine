import logging.config
import logging
logger = logging.getLogger()

import sys
sys.path.append('..')

from src.chess_game import ChessGame
import chess

FEN = "rnb1k2r/p5pp/2p4q/1p1p4/4p1nK/1B2P3/PPPP1PP1/RNBQ1R2 w - - 5 14"

def main():
    
    
    aichess = ChessGame(3)
    aichess.setup_from_fen(FEN)
    board = aichess.get_board()
    moves = aichess.get_move_list()
    
    logger.debug("Moves:")
    for move in moves:
        logger.debug(move)

    move = aichess.get_best_move()
    logger.debug("Move:")
    logger.debug(move)
        

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    main()
