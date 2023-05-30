import logging.config

import sys
sys.path.append('..')
from src.engine import Stockfish
from src.chess_game import ChessGame
import chess

engine_path = "/usr/local/bin/stockfish"

def main():
    
    board = chess.Board()
    fish = Stockfish(engine_path, 0.1)
    aichess = ChessGame(3)
    while True:
        if board.turn == chess.WHITE:
            eval, move = aichess.get_best_move()
            logging.debug(eval)
        else:
            move = fish.get_best_move()
        logging.debug(move)
        #logging.debug(fish.get_moves())
        board.push(move)
        logging.debug(board.fen())
        fish.make_move(move)
        aichess.make_move(move)
        if board.is_game_over():
            break
    print(chess.Board.variation_san(board.move_stack))
        
    fish.quit()

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    main()
