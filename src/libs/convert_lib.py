import numpy as np
import torch

def bool_to_int_tensor(bool_array):

    shape = bool_array.shape
    if shape[1] != 8 or shape[2] != 8:
        raise("Wrong Shape of Bitboard Error")
    length = shape[0]
    int_array = []
    for i in range(length):
        int_array.append(np.packbits(bool_array[i].astype(np.uint8)).view(np.int64)[0])
    int_tensor = torch.tensor(int_array, dtype=torch.int64)
    return int_tensor

def int_tensor_to_bool(int_tensor):
    int64_list = int_tensor.tolist()
    length = len(int64_list)
    bool_array = []
    for i in range(length):
        boolean_array = np.unpackbits(np.array([int64_list[i]], dtype=np.int64).view(np.uint8))
        boolean_array = boolean_array[-64:].reshape((8, 8)).astype(bool)
        bool_array.append(boolean_array)
    return bool_array

def piece2char(piece):
    piece_chars = {
            0: "P", 1: "N", 2: "B", 3: "R", 4: "Q", 5: "K", 
            6: "p", 7: "n", 8: "b", 9: "r", 10: "q", 11: "k"
                }
    return piece_chars.get(piece, " ")

def substitute_piece(string, position, piece):
                
    if position < 0 or position >= len(string):
        return string  # Return the original string if position is out of range
    else:
        return string[:position] + piece2char(piece) + string[position+1:]

                

    