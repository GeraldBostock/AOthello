import pygame

import colors

import board

import json

import threading

class Game:
    def __init__(self, screen_width, screen_height):
            pygame.init()
            pygame.font.init()
            pygame.display.set_caption('AOthello')

            self.screen = pygame.display.set_mode((screen_width, screen_height))
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.board_offset = 30

            self.board = board.Board(8, 8, self.board_offset, self.screen_width - self.board_offset * 2, self.screen_height - self.board_offset * 2)

            # Index 0 is black player, 1 is white player
            self.players = [None] * 2
            self.current_player_index = 1

            self.board.calculate_viable_positions_for_player(self.get_player_color())

            self.font = pygame.font.Font(None, 20)

            self.currently_playing = False
            self.last_played_piece = None

    def run(self):
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            
            self.screen.fill(colors.WHITE)

            if not self.currently_playing:
                thread = threading.Thread(target=self.players[self.current_player_index].run, args=(self.board, self.board.get_viable_moves()))
                thread.start()
                self.currently_playing = True

            self.board.render_board(self.screen, (self.board_offset, self.board_offset), self.last_played_piece)

            textsurface = self.font.render('Turn: ' + str(self.get_player_color()), False, (0, 0, 0))
            self.screen.blit(textsurface,(5, self.screen_height - 15))

            pygame.display.flip()

    def move_played_callback(self, move):

        self.currently_playing = False

        if self.board.is_move_viable(move):
            player_color = self.get_player_color()
            self.board.make_move(player_color, move)
            self.current_player_index += 1
            self.current_player_index %= 2
            player_color = self.get_player_color()
            self.board.calculate_viable_positions_for_player(player_color)
            self.last_played_piece = move

            viable_moves = self.board.get_viable_moves()
            if len(viable_moves) == 0:
                print('Player has no viable moves. Passing.')
                self.current_player_index += 1
                self.current_player_index %= 2
                player_color = self.get_player_color()
                self.board.calculate_viable_positions_for_player(player_color)

        if not self.currently_playing:
            #print('a')
            self.currently_playing = False

    def get_player_color(self):
        if self.current_player_index == 0:
            return 'white'
        else:
            return 'black'

    def set_black_player(self, player):
        self.players[1] = player
        self.players[1].set_parent(self)
        self.players[1].set_color('black')

    def set_white_player(self, player):
        self.players[0] = player
        self.players[0].set_parent(self)
        self.players[0].set_color('white')

    def save_board_state(self):
        board_state = dict()

        board_state['player_turn'] = self.current_player_index
        board_state['board_state'] = self.board.board

        with open('data.json', 'w') as fp:
            json.dump(board_state, fp)

    def load_board_state(self, file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
            self.current_player_index = data['player_turn']
            self.board.board = data['board_state']

        self.board.calculate_viable_positions_for_player(self.get_player_color())
