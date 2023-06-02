import chess
import torch
import torch.nn as nn

FILEPATH = "/Users/littlecapa/GIT/python/ai_chess_engine/model/nn"

class Chess_NN:

    def __init__(self):
        super(Chess_NN, self).__init__()

        self.conv1 = nn.Conv2d(13, 64, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1)
        self.conv5 = nn.Conv2d(256, 128, kernel_size=3, stride=1, padding=1)
        self.conv6 = nn.Conv2d(128, 1, kernel_size=3, stride=1, padding=1)

        self.fc1 = nn.Linear(64, 32)
        self.fc2 = nn.Linear(32, 1)

        self.relu = nn.ReLU()
    
    def save_model(self, filepath = FILEPATH):
        torch.save(self.relu.state_dict(), filepath)

    def load_model(self, filepath = FILEPATH):
        self.relu.load_state_dict(torch.load(filepath))

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        x = self.relu(self.conv4(x))
        x = self.relu(self.conv5(x))
        x = self.relu(self.conv6(x))

        x = x.view(x.size(0), -1)  # Flatten the tensor
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def board_to_tensor(_, board):
        
        # Initialize the tensor with zeros
        tensor = torch.zeros((14, 8, 8), dtype=torch.bool)

        # Iterate over the board and update the tensor
        for rank in range(8):
            for file in range(8):
                square = chess.square(file, 7 - rank)
                piece = board.piece_at(square)

                if piece is not None:
                    piece_type = piece.piece_type - 1
                    if piece.color == chess.BLACK:
                        piece_type += 6
                    tensor[piece_type][rank][file] = True

        # Encode the castling rights
        if board.castling_rights & chess.BB_H1:
            tensor[12][0][0] = True
        if board.castling_rights & chess.BB_A1:
            tensor[12][1][0] = True
        if board.castling_rights & chess.BB_H8:
            tensor[12][2][0] = True
        if board.castling_rights & chess.BB_A8:
            tensor[12][3][0] = True

        # Encode the turn
        tensor[12][4][0] = board.turn
        # 61 Bits remain unused

        return tensor
    
    def tensor_to_str(_, tensor):

        def substitute_piece(string, position, piece):

            def piece2char(piece):
                piece_chars = {
                    0: "P", 1: "N", 2: "B", 3: "R", 4: "Q", 5: "K", 
                    6: "p", 7: "n", 8: "b", 9: "r", 10: "q", 11: "k"
                }
                return piece_chars.get(piece, " ")

                
            if position < 0 or position >= len(string):
                return string  # Return the original string if position is out of range
            else:
                return string[:position] + piece2char(piece) + string[position+1:]

        blank_string = " " * 8
        board_string = [blank_string] * 8
        for rank in range(8):
            for file in range(8):
                for piece_type in range(12):
                    if tensor[piece_type][rank][file]:
                        board_string[rank] = substitute_piece(board_string[rank], file, piece_type)
        extra_string = ""
        if tensor[12][4][0]:
            extra_string += "White "
        else:
            extra_string += "Black "
        if tensor[12][0][0]:
            extra_string += "K"
        if tensor[12][1][0]:
            extra_string += "Q"
        if tensor[12][2][0]:
            extra_string += "k"
        if tensor[12][3][0]:
            extra_string += "q"
        
        return_string = ""
        for i in range(8):
            return_string += board_string[i] +"\n"
        return_string += extra_string
        return return_string
    

    def eval_board(self, board):
        tensor = self.board_to_tensor(board)
        eval = self.forward(tensor.unsqueeze(0))
        return eval
