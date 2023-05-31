import logging.config
import logging
logger = logging.getLogger()

import sys
sys.path.append('..')

from src.chess_game import ChessGame
import chess

# Mate in Three:
#FEN = "rnb1k2r/p5pp/2pq4/1p1p4/4p1nK/1B2P3/PPPP1PP1/RNBQ1R2 b - - 5 13"

# Mate in Two:
#FEN = "rnb1k2r/p5pp/2p4q/1p1p4/4p1nK/1B2P3/PPPP1PP1/RNBQ1R2 w - - 5 14"

# Mate in One:
#FEN = "rnb1k2r/p5pp/2p4q/1p1p4/4p1n1/1B2P1K1/PPPP1PP1/RNBQ1R2 b - - 5 15"

# Why allow mate in 3
FEN = "rnbqk1nr/1pp2pp1/3b3p/p2pN3/P6P/5p2/1PPPP1P1/RNBQKB1R w KQkq - 0 7"

def main():
    
    
    aichess = ChessGame(3)
    aichess.setup_from_fen(FEN)
    board = aichess.get_board()
    moves = aichess.get_move_list()
    
    logger.debug("Moves:")
    for move in moves:
        logger.debug(move)

    aichess.logger_on()
    eval, move = aichess.get_best_move()
    logger.debug("Move:")
    logger.debug(move)
    logger.debug("Evaluation:")
    logger.debug(eval)
    print(aichess.get_logger_data())
        

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    main()
