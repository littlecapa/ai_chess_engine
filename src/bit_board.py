import chess

# Bitboard representation of the chess board
# currently not used!


class Bitboard:
    def __init__(self):
        # Initialize the bitboards for each piece type
        self.white_pawns = 0
        self.white_knights = 0
        self.white_bishops = 0
        self.white_rooks = 0
        self.white_queens = 0
        self.white_king = 0

        self.black_pawns = 0
        self.black_knights = 0
        self.black_bishops = 0
        self.black_rooks = 0
        self.black_queens = 0
        self.black_king = 0

        # Initialize the bitboards for occupied squares
        self.occupied = 0
        self.empty = 0xFFFFFFFFFFFFFFFF

        # Initialize the side to move
        self.side_to_move = chess.WHITE
        # Initialize the castling rights
        self.castling_rights = chess.BB_A1 | chess.BB_H1 | chess.BB_A8 | chess.BB_H8

    def set_piece(self, piece, square):
        # Set the bitboard for a given piece and square
        if piece == chess.PAWN:
            self.white_pawns |= 1 << square
        elif piece == chess.KNIGHT:
            self.white_knights |= 1 << square
        elif piece == chess.BISHOP:
            self.white_bishops |= 1 << square
        elif piece == chess.ROOK:
            self.white_rooks |= 1 << square
        elif piece == chess.QUEEN:
            self.white_queens |= 1 << square
        elif piece == chess.KING:
            self.white_king |= 1 << square
        elif piece == chess.PAWN | chess.BLACK:
            self.black_pawns |= 1 << square
        elif piece == chess.KNIGHT | chess.BLACK:
            self.black_knights |= 1 << square
        elif piece == chess.BISHOP | chess.BLACK:
            self.black_bishops |= 1 << square
        elif piece == chess.ROOK | chess.BLACK:
            self.black_rooks |= 1 << square
        elif piece == chess.QUEEN | chess.BLACK:
            self.black_queens |= 1 << square
        elif piece == chess.KING | chess.BLACK:
            self.black_king |= 1 << square

        # Update the occupied and empty bitboards
        self.occupied |= 1 << square
        self.empty = ~self.occupied

        # Get the piece at the given square
        if self.occupied & (1 << square):
            if self.white_pawns & (1 << square):
                return chess.PAWN
            elif self.white_knights & (1 << square):
                return chess.KNIGHT
            elif self.white_bishops & (1 << square):
                return chess.BISHOP
            elif self.white_rooks & (1 << square):
                return chess.ROOK
            elif self.white_queens & (1 << square):
                return chess.QUEEN
            elif self.white_king & (1 << square):
                return chess.KING
            elif self.black_pawns & (1 << square):
                return chess.PAWN | chess.BLACK
            elif self.black_knights & (1 << square):
                return chess.KNIGHT | chess.BLACK
            elif self.black_bishops & (1 << square):
                return chess.BISHOP | chess.BLACK
            elif self.black_rooks & (1 << square):
                return chess.ROOK | chess.BLACK
            elif self.black_queens & (1 << square):
                return chess.QUEEN

    def get_bitboard(self):
        # Get the bit vector representation of the current board
        bitboard = [
            self.white_pawns,
            self.white_knights,
            self.white_bishops,
            self.white_rooks,
            self.white_queens,
            self.white_king,
            self.black_pawns,
            self.black_knights,
            self.black_bishops,
            self.black_rooks,
            self.black_queens,
            self.black_king
        ]
        bitboard.extend([
            self.side_to_move,
            self.castling_rights
        ])
        return bitboard

    def print_board(self):
        # Print the bitboard representation of the chess board
        for rank in range(7, -1, -1):
            for file in range(8):
                square = rank * 8 + file
                piece = chess.EMPTY
                if self.occupied & (1 << square):
                    if self.white_pawns & (1 << square):
                        piece = chess.PAWN
                    elif self.white_knights & (1 << square):
                        piece = chess.KNIGHT
                    elif self.white_bishops & (1 << square):
                        piece = chess.BISHOP
                    elif self.white_rooks & (1 << square):
                        piece = chess.ROOK
                    elif self.white_queens & (1 << square):
                        piece = chess.QUEEN
                    elif self.white_king & (1 << square):
                        piece = chess.KING
                    elif self.black_pawns & (1 << square):
                        piece = chess.PAWN | chess.BLACK
                    elif self.black_knights & (1 << square):
                        piece = chess.KNIGHT | chess.BLACK
                    elif self.black_bishops & (1 << square):
                        piece = chess.BISHOP | chess.BLACK
                    elif self.black_rooks & (1 << square):
                        piece = chess.ROOK | chess.BLACK
                    elif self.black_queens & (1 << square):
                        piece = chess.QUEEN

    def setup_from_fen(self, fen):
        # Set up the bitboard representation from a FEN string
        board = chess.Board(fen)
        
        for square, piece in board.piece_map().items():
            self.set_piece(piece.piece_type, square)

        self.side_to_move = board.turn
        self.castling_rights = board.castling_rights
