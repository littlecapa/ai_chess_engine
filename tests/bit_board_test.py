import sys
sys.path.append('..')

import src.bit_board as bb

print("Start")
bitboard = bb.Bitboard()
bitboard.setup_from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
current_bitboard = bitboard.get_bitboard()
print(current_bitboard)


bitboard.setup_from_fen('r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4')
current_bitboard = bitboard.get_bitboard()
print(current_bitboard)