import logging.config

import sys
sys.path.append('..')
from src.engine import Stockfish
from src.chess_game_syzygy import ChessSyzygyGame
import chess

engine_path = "/usr/local/bin/stockfish"
FEN = "8/8/8/8/8/3k4/2R5/1K6 w - - 0 1"

def main():
    
    board = chess.Board()
    board.set_fen(FEN)

    fish = Stockfish(engine_path, 0.1)
    aichess = ChessSyzygyGame(3)
    aichess.set_board(board)
    fish.set_board(board)
    while True:
        if board.turn == chess.WHITE:
            eval, move = aichess.get_best_move()
            logging.debug(f"Eval: {eval}")
        else:
            move = fish.get_best_move()
        logging.debug(f"Move: {move}")
        #logging.debug(fish.get_moves())
        board.push(move)
        #logging.debug(board.fen())
        #fish.make_move(move)
        #aichess.make_move(move)
        if board.is_game_over():
            break
    for i, move in enumerate(board.move_stack):
        move_number = (i // 2) + 1
        if i % 2 == 0:
            print(f"{move_number}. {move}")
        else:
            print(f"    {move}")
        
    fish.quit()

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    main()
