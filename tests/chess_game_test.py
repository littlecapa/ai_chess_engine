import sys
sys.path.append('..')

import chess

from src.chess_game import *

# Evaluate the position

game = ChessGame()
# The FEN (Forsyth-Edwards Notation) for the position after the moves "1.d4 d5 2.c4 e6 3.Nc3 Nf6 4.Bg5 Be7" is:
game.setup_from_fen('rnbqk2r/ppp1bppp/4pn2/3p2B1/2PP4/2N5/PP2PPPP/R2QKBNR w KQkq - 0 5')
#game.setup_from_fen('4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1')

print (f"Evaluation: {game.evaluate()}")

print (f"Move List: {game.get_move_list(evaluated=True)}")
print (f"Move List: {game.get_move_list(evaluated=False)}")

print (game.get_board())