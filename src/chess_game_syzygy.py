import chess
import chess.syzygy

from src.chess_game import ChessGame

checkmate_value = 999.0

SYZYGY_PATH = "/Users/littlecapa/chess/syzygy"

MAX_SYZYGY_PIECES = 5

class ChessSyzygyGame(ChessGame):

    def __init__(self, max_depth=3, extra_depth_capture = 3):
        super().__init__(max_depth, extra_depth_capture)
        # Load the Tablebase
        self.tablebases = chess.syzygy.Tablebase()
        self.tablebases.add_directory(SYZYGY_PATH)
        
    
    def get_best_move(self):

        # Generate all legal moves
        legal_moves = list(self.board.legal_moves)
        print(self.board)

        # Initialize variables
        best_move = None
        shortest_distance = float('inf')

        # Iterate through each legal move
        for move in legal_moves:
            # Make the move on a temporary board
            temp_board = self.board.copy()
            temp_board.push(move)

            # Probe the table bases to get the distance to mate
            distance = -self.tablebases.probe_dtz(temp_board)
            print(f"Move: {move}, Distance: {distance}")

            # Check if the distance is shorter than the current best distance
            if distance is not None and distance > 0 and distance < shortest_distance:
                shortest_distance = distance
                best_move = move
       
        return shortest_distance, best_move
