import chess
import torch
import torch.nn as nn
import numpy as np
from src.libs.convert_lib import substitute_piece, int_tensor_to_bool, bool_to_int_tensor

FILEPATH = "/Users/littlecapa/GIT/python/ai_chess_engine/model/nn"

class Chess_NN(nn.Module):

    def __init__(self):
        super(Chess_NN, self).__init__()
        
        self.optimizer = torch.optim.Adam
        self.loss = nn.MSELoss()
        
        self.dense1 = nn.Linear(13, 64)
        self.dense2 = nn.Linear(64, 128)
        self.dense3 = nn.Linear(128, 256)
        self.dense4 = nn.Linear(256, 128)
        self.dense5 = nn.Linear(128, 64)
        self.dense6 = nn.Linear(64, 1)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        x = self.dense1(x.float())
        x = self.relu(x)
        x = self.dense2(x)
        x = self.relu(x)
        x = self.dense3(x)
        x = self.relu(x)
        x = self.dense4(x)
        x = self.relu(x)
        x = self.dense5(x)
        x = self.relu(x)
        output = self.dense6(x)
        
        return output
    
    def save_model(self):
        torch.save(self, FILEPATH)

    @classmethod
    def load_model(cls):
        return torch.load(FILEPATH)

    def board_to_tensor(_, board):
        
        # Initialize the tensor with zeros
        # bool_tensor = torch.zeros((13, 8, 8), dtype=torch.bool)
        bool_array = np.zeros((13, 8, 8), dtype=bool)
        # Iterate over the board and update the tensor
        for rank in range(8):
            for file in range(8):
                square = chess.square(file, 7 - rank)
                piece = board.piece_at(square)

                if piece is not None:
                    piece_type = piece.piece_type - 1
                    if piece.color == chess.BLACK:
                        piece_type += 6
                    bool_array[piece_type][rank][file] = True

        # Encode the castling rights
        if board.castling_rights & chess.BB_H1:
            bool_array[12][0][0] = True
        if board.castling_rights & chess.BB_A1:
            bool_array[12][1][0] = True
        if board.castling_rights & chess.BB_H8:
            bool_array[12][2][0] = True
        if board.castling_rights & chess.BB_A8:
            bool_array[12][3][0] = True

        # Encode the turn
        bool_array[12][4][0] = board.turn
        # Missing: EP Field
        # 61 Bits remain unused
        int_tensor = bool_to_int_tensor(bool_array)
        return int_tensor
    
    def tensor_to_str(_, int_tensor):

        bool_array = int_tensor_to_bool(int_tensor)
        blank_string = " " * 8
        board_string = [blank_string] * 8
        for rank in range(8):
            for file in range(8):
                for piece_type in range(12):
                    if bool_array[piece_type][rank][file]:
                        board_string[rank] = substitute_piece(board_string[rank], file, piece_type)
        extra_string = ""
        if bool_array[12][4][0]:
            extra_string += "White "
        else:
            extra_string += "Black "
        if bool_array[12][0][0]:
            extra_string += "K"
        if bool_array[12][1][0]:
            extra_string += "Q"
        if bool_array[12][2][0]:
            extra_string += "k"
        if bool_array[12][3][0]:
            extra_string += "q"
        
        return_string = ""
        for i in range(8):
            return_string += board_string[i] +"\n"
        return_string += extra_string
        return return_string
    

    def eval_board(self, board):
        tensor = self.board_to_tensor(board)
        eval = self.forward(tensor)
        return eval