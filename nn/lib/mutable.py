from converter import *
from collections import namedtuple

import numpy as np

Example = namedtuple('Example', [
    'horizontal',
    'vertical',
    'onturn_pawn',
    'onturn_walls',
    'other_pawn',
    'other_walls',
    'expected_horizontal',
    'expected_vertical',
    'expected_pawn',
])

class Converter:
    def reset(self):
        self.o_on_turn = False

        self.horizontal_walls = square(8)
        self.vertical_walls = square(8)

        self.x_pawn = square(9)
        self.x_pawn[8][4] = '1'
        self.o_pawn = square(9)
        self.o_pawn[0][4] = '1'

        self.x_walls_left = 10
        self.o_walls_left = 10

        self.onturn_pawn = self.x_pawn
        self.onturn_walls = self.x_walls_left
        self.other_pawn = self.o_pawn
        self.other_walls = self.o_walls_left

        self.expected_horizontal = square(8)
        self.expected_vertical = square(8)
        self.expected_pawn = square(9)

    def get_move(self, move):
        if len(move) == 3:
            col = columns.index(move[0])
            row = 8 - int(move[1])
            return [row, col, move[2]]
        elif len(move) == 2:
            col = columns.index(move[0])
            row = 9 - int(move[1])
            return [row, col]
        else:
            raise Exception(move)

    def set_expected(self, move, value):
        if len(move) == 3:
            if move[2] == 'h':
                self.expected_horizontal[move[0]][move[1]] = value
            else:
                self.expected_vertical[move[0]][move[1]] = value
        else:
            self.expected_pawn[move[0]][move[1]] = value

    def play(self, move):
        if len(move) == 3:
            if self.o_on_turn:
                self.o_walls_left -= 1
            else:
                self.x_walls_left -= 1

            if move[2] == 'h':
                self.horizontal_walls[move[0]][move[1]] = '1'
            else:
                self.vertical_walls[move[0]][move[1]] = '1'
        else:
            if self.o_on_turn:
                self.o_pawn = square(9)
                self.o_pawn[move[0]][move[1]] = '1'
            else:
                self.x_pawn = square(9)
                self.x_pawn[move[0]][move[1]] = '1'

    def get_next(self, move_str, transfunc):
        move = self.get_move(move_str)

        # set move as expected
        self.set_expected(move, '1')

        # assemble output
        example = transfunc(Example(
            rotate(self.horizontal_walls, self.o_on_turn),
            rotate(self.vertical_walls, self.o_on_turn),
            rotate(self.onturn_pawn, self.o_on_turn),
            self.onturn_walls,
            rotate(self.other_pawn, self.o_on_turn),
            self.other_walls,
            rotate(self.expected_horizontal, self.o_on_turn),
            rotate(self.expected_vertical, self.o_on_turn),
            rotate(self.expected_pawn, self.o_on_turn),
        ))

        # reset expected
        self.set_expected(move, '0')

        # modify state with move
        self.play(move)

        self.o_on_turn = not self.o_on_turn
        if self.o_on_turn:
            self.onturn_pawn = self.o_pawn
            self.onturn_walls = self.o_walls_left
            self.other_pawn = self.x_pawn
            self.other_walls = self.x_walls_left
        else:
            self.onturn_pawn = self.x_pawn
            self.onturn_walls = self.x_walls_left
            self.other_pawn = self.o_pawn
            self.other_walls = self.o_walls_left

        return example

    def example_as_string(self, example):
        return "\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n-\n\n%s\n\n%s\n\n%s\n" % (
            out_square(example.horizontal),
            out_square(example.vertical),
            out_square(example.onturn_pawn),
            example.onturn_walls,
            out_square(example.other_pawn),
            example.other_walls,
            out_square(example.expected_horizontal),
            out_square(example.expected_vertical),
            out_square(example.expected_pawn),
        )

    def example_as_numpy(self, example):
        return Example(
            np.array(example.horizontal),
            np.array(example.vertical),
            np.array(example.onturn_pawn),
            example.onturn_walls,
            np.array(example.other_pawn),
            example.other_walls,
            np.array(example.expected_horizontal),
            np.array(example.expected_vertical),
            np.array(example.expected_pawn),
        )

    def convert(self, record):
        self.reset()
        self.moves = record.split(";")

        z = []
        for i in range(0, len(self.moves)):
            try:
                z.append(self.get_next(self.moves[i], self.example_as_numpy))
            except IndexError as err:
                print(self.moves[i])
                print(record)
                raise err

        return z
