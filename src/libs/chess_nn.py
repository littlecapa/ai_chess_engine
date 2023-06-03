import chess
import torch
import torch.nn as nn
import numpy as np
from src.libs.convert_lib import substitute_piece, int_tensor_to_bool, bool_to_int_tensor

FILEPATH = "/Users/littlecapa/GIT/python/ai_chess_engine/model/nn"

class Chess_NN:

    def __init__(self):
        super(Chess_NN, self).__init__()
        
        #self.input_layer = nn.Linear(13, 128)
        #self.hidden_layers = nn.ModuleList([nn.Linear(128, 128) for _ in range(4)])
        #self.output_layer = nn.Linear(128, 1)
        #self.relu = nn.ReLU()
        self.optimizer = torch.optim.Adam
        self.loss = nn.CrossEntropyLoss()

        self.conv1 = nn.Conv2d(1, 64, kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=2, stride=2)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=2, stride=2)
        self.flatten = nn.Flatten()
        self.dense1 = nn.Linear(4096, 512)
        self.dense2 = nn.Linear(512, 1)
        self.sigmoid = nn.Sigmoid()
        self.relu = nn.ReLU()

    def forward(self, x):
        x = x.view(-1, 1, 13, 1)  # Reshape input to match channel and height dimensions
        x = self.conv1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.conv3(x)
        x = self.relu(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.relu(x)
        x = self.sigmoid(x)
        output = self.dense2(x)

        return output
        #x = x.unsqueeze(0).float()
        #x = self.input_layer(x)
        #x = self.relu(x)
        #
        #for layer in self.hidden_layers:
        #    x = layer(x)
        #    x = self.relu(x)
        #
        #x = self.output_layer(x)
        #x = torch.sigmoid(x)
        #return x.item()
    
    def save_model(self):
        torch.save(self, FILEPATH)

    def load_model(self):
        torch.load(self, FILEPATH)

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