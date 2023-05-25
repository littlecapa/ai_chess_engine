import chess

def is_castling_move(move):
        if move.from_square == chess.E1 and move.to_square == chess.G1:
            return True  # White kingside castling
        elif move.from_square == chess.E1 and move.to_square == chess.C1:
            return True  # White queenside castling
        elif move.from_square == chess.E8 and move.to_square == chess.G8:
            return True  # Black kingside castling
        elif move.from_square == chess.E8 and move.to_square == chess.C8:
            return True  # Black queenside castling
        else:
            return False