import player
import random
import time
import torch
import numpy as np
from board import Cells

class AIPlayer(player.IPlayer):

    def __init__(self):
        self.model = NeuralNet()
        self.model.load_state_dict(torch.load('model_augmented.pt'))

    def make_move(self, board, viable_moves):

        self.model = NeuralNet()
        self.model.load_state_dict(torch.load('model_augmented.pt'))

        cnn_input = torch.from_numpy(self.format_input(self, board, viable_moves))
        time.sleep(1)

        output = self.model(cnn_input.float()).detach().numpy()
        label_outputs = np.argsort(output[0])

        label_counter = 0
        for label in reversed(label_outputs):
            index = self.label_to_index(self, label)
            
            index = index[::-1]
            
            for move in viable_moves:
                if index == move.position:
                    print('Selecting {}. best label => ({}, {})'.format(label_counter + 1, index[0], index[1]))
                    return index

            label_counter += 1

        random.shuffle(viable_moves)
        return viable_moves[0].position

    def label_to_index(self, label):
        j = label % 8
        i = int(label / 8)

        return (i, j)

    def format_input(self, board, viable_moves):
        board_state = board.board

        cnn_input = np.zeros((10, 3, 8, 8))

        color = Cells.white
        if self.color == 'black':
            color = Cells.black

        for i in range(8):
            for j in range(8):
                if board_state[i][j] == color:
                    cnn_input[0][0][i][j] = 1
                elif not board_state[i][j] == Cells.empty:
                    cnn_input[0][1][i][j] = 1

    
        for viable_move in viable_moves:
            position = viable_move.position

            cnn_input[0][2][position[0]][position[1]] = 1

        return cnn_input


import torch.nn as nn
import torch.nn.functional as F

train_on_gpu = torch.cuda.is_available()

class NeuralNet(nn.Module):
    def __init__(self):
        super(NeuralNet, self).__init__()

        self.conv1 = nn.Conv2d(3, 64, 3, padding=1)
        
        self.conv2 = nn.Conv2d(64, 64, 3, padding=1)
        
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        
        self.conv4 = nn.Conv2d(128, 128, 3, padding=1)

        self.fc1 = nn.Linear(8192, 128)
        
        self.fc2 = nn.Linear(128, 64)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))

        x = x.view(x.shape[0], -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x