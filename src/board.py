from enum import IntEnum
import enum
from game import colors
import pygame

class Cells(IntEnum):
    empty = 0
    black = 1
    white = 2

class Directions(enum.Enum):
    north = 0
    north_east = 1
    east = 2
    south_east = 3
    south = 4
    south_west = 5
    west = 6
    north_west = 7

class PlayerMove:

    def __init__(self, position, pieces_to_flip, player_color):
        self.position = position
        self.pieces_to_flip = pieces_to_flip
        self.player_color = player_color

class Board:
    def __init__(self, board_width, board_height, board_offset, board_render_width, board_render_height):
        self.board_width = board_width
        self.board_height = board_height
        self.board_render_width = board_render_width
        self.board_render_height = board_render_height
        self.cell_render_width = board_render_width / board_width
        self.cell_render_height = board_render_height / board_height
        self.board_offset = board_offset
        self.font = pygame.font.Font(None, 20)

        self.board = [[Cells.empty for x in range(board_width)] for y in range(board_height)]

        # Starting pieces
        self.board[int(self.board_width / 2)][int(self.board_height / 2)] = Cells.white
        self.board[int(self.board_width / 2) - 1][int(self.board_height / 2)] = Cells.black
        self.board[int(self.board_width / 2)][int(self.board_height / 2) - 1] = Cells.black
        self.board[int(self.board_width / 2) - 1][int(self.board_height / 2) - 1] = Cells.white

        self.viable_moves = list()

    def calculate_viable_positions_for_player(self, player):

        self.viable_moves.clear()

        if player == 'black':
            stop_condition = Cells.black
            keep_checking_condition = Cells.white
        elif player == 'white':
            stop_condition = Cells.white
            keep_checking_condition = Cells.black

        for i in range(self.board_width):
            for j in range(self.board_height):
                if self.board[i][j] == Cells.empty:
                    
                    for direction, member in Directions.__members__.items():
                        offsets = self.get_direction_offset(member)
                        i_offset = offsets[0]
                        j_offset = offsets[1]

                        done = False
                        tmp_i = i + i_offset
                        tmp_j = j + j_offset
                        pieces_to_flip = list()
                        while not done:
                            if tmp_i < 0 or tmp_j < 0 or tmp_i >= self.board_width or tmp_j >= self.board_height:
                                break

                            if self.board[tmp_i][tmp_j] == keep_checking_condition:
                                pieces_to_flip.append((tmp_i, tmp_j))
                                tmp_i += i_offset
                                tmp_j += j_offset
                                continue
                                
                            if self.board[tmp_i][tmp_j] == stop_condition:
                                if len(pieces_to_flip) > 0:
                                    self.viable_moves.append(PlayerMove((i, j), pieces_to_flip, player))
                                break
                                
                            if self.board[tmp_i][tmp_j] == Cells.empty or tmp_i == 0:
                                break


    def make_move(self, piece_color, piece_position):
        for move in self.viable_moves:
            if move.position == piece_position:
                for piece_to_flip in move.pieces_to_flip:
                    self.flip_piece(piece_to_flip)

                if piece_color == 'black':
                    self.board[piece_position[0]][piece_position[1]] = Cells.black
                else:
                    self.board[piece_position[0]][piece_position[1]] = Cells.white

    def flip_piece(self, position):
        if self.board[position[0]][position[1]] == Cells.empty:
            print("Can't flip empty cell")
            return
        
        if self.board[position[0]][position[1]] == Cells.black:
            self.board[position[0]][position[1]] = Cells.white
            return

        if self.board[position[0]][position[1]] == Cells.white:
            self.board[position[0]][position[1]] = Cells.black
            return

    def render_board(self, screen, board_position, last_played_piece):
        
        pygame.draw.rect(screen, colors.DARK_GREEN, [board_position[0], board_position[1], self.board_render_width, self.board_render_height])

        # Cell lines
        for i in range(self.board_width):
            vertical_point1 = (board_position[0] + self.cell_render_width * i, board_position[1])
            vertical_point2 = (board_position[0] + self.cell_render_width * i, board_position[1] + self.board_render_height)

            horizontal_point1 = (board_position[0], board_position[1] + self.cell_render_height * i)
            horizontal_point2 = (board_position[0] + self.board_render_width, board_position[1] + self.cell_render_height * i)

            pygame.draw.line(screen, colors.WHITE, vertical_point1, vertical_point2)
            pygame.draw.line(screen, colors.WHITE, horizontal_point1, horizontal_point2)

        # Pieces
        piece_count = 0
        for i in range(self.board_width):
            for j in range(self.board_height):
                if not self.board[i][j] == Cells.empty:
                    piece_count += 1
                    position_x = self.cell_render_width * i + board_position[0] + self.cell_render_width / 2
                    position_y = self.cell_render_height * j + board_position[1] + self.cell_render_height / 2

                    piece_color = colors.WHITE
                    if self.board[i][j] == Cells.black:
                        piece_color = colors.BLACK
                    
                    if last_played_piece:
                        if i == last_played_piece[0] and j == last_played_piece[1]:
                            piece_color = colors.BLUE

                    pygame.draw.circle(screen, piece_color, [int(position_x), int(position_y)], int(self.board_render_width / (self.board_width * 2) - 2))

        # Highlight viable positions
        for move in self.viable_moves:
            position_i = move.position[0]
            position_j = move.position[1]
            screen_position_x = self.cell_render_width * position_i + board_position[0]
            screen_position_y = self.cell_render_height * position_j + board_position[1]
            pygame.draw.rect(screen, colors.YELLOW, [screen_position_x, screen_position_y, self.cell_render_width, self.cell_render_height], 4)

        # Board letters - A, B, C, D, E, F, G, H
        current_letter = 65
        for i in range(self.board_width):
            position_x = self.cell_render_width * i + board_position[0] + self.cell_render_width / 2
            position_y = self.cell_render_height * 0 + board_position[1] + self.cell_render_height / 2
            textsurface = self.font.render(chr(current_letter), False, (0, 0, 0))
            screen.blit(textsurface,(position_x - 4, position_y - 4 - self.cell_render_height * 0.75))
            current_letter += 1

        # Board numbers - 1, 2, 3, 4, 5, 6, 7, 8
        for i in range(self.board_height):
            position_x = self.cell_render_width * 0 + board_position[0] + self.cell_render_width / 2
            position_y = self.cell_render_height * i + board_position[1] + self.cell_render_height / 2
            textsurface = self.font.render(str(i + 1), False, (0, 0, 0))
            screen.blit(textsurface,(position_x - 4 - self.cell_render_width * 0.75, position_y - 4))

        textsurface = self.font.render('# of pieces: {}'.format(piece_count), False, (0, 0, 0))
        screen.blit(textsurface, (500, 580))

    def get_cell_index_from_position(self, position_2d):
        if position_2d[0] > self.board_offset and position_2d[1] > self.board_offset and position_2d[0] < self.board_offset + self.board_render_width and position_2d[1] < self.board_offset + self.board_render_height:

            return (int((position_2d[0] - self.board_offset) / self.cell_render_width), int((position_2d[1] - self.board_offset) / self.cell_render_height))

        else:
            return False

    def is_move_viable(self, position):
        for move in self.viable_moves:
            if move.position == position:
                return True

        return False

    def get_viable_moves(self):
        return self.viable_moves

    def get_direction_offset(self, direction):

        if direction == Directions.north:
            return (0, -1)
        if direction == Directions.north_east:
            return (1, -1)
        if direction == Directions.east:
            return (1, 0)
        if direction == Directions.south_east:
            return (1, 1)
        if direction == Directions.south:
            return (0, 1)
        if direction == Directions.south_west:
            return (-1, 1)
        if direction == Directions.west:
            return (-1, 0)
        if direction == Directions.north_west:
            return (-1, -1)