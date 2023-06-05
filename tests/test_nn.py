import sys
sys.path.append('..')

import chess

from src.libs.chess_nn import Chess_NN

# Evaluate the position

board = chess.Board()

cnn = Chess_NN()

tensor = cnn.board_to_tensor(board)

print (cnn.tensor_to_str(tensor))

cnn.save_model()

print("First Eval)")

eval = cnn.eval_board(board)

print(f"Eval: {eval}")

cnn = cnn.load_model()

eval = cnn.eval_board(board)

print("Scond Eval)")

print(f"Eval: {eval}")