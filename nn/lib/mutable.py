from converter import *

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

    def get_next(self, move_str):
        move = self.get_move(move_str)

        # set move as expected
        self.set_expected(move, '1')

        # assemble output string
        ret = "\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n-\n\n%s\n\n%s\n\n%s\n" % (
            out_square(rotate(self.horizontal_walls, self.o_on_turn)),
            out_square(rotate(self.vertical_walls, self.o_on_turn)),
            out_square(rotate(self.onturn_pawn, self.o_on_turn)),
            self.onturn_walls,
            out_square(rotate(self.other_pawn, self.o_on_turn)),
            self.other_walls,
            out_square(rotate(self.expected_horizontal, self.o_on_turn)),
            out_square(rotate(self.expected_vertical, self.o_on_turn)),
            out_square(rotate(self.expected_pawn, self.o_on_turn)),
        )

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

        return ret

    def convert(self, record):
        self.reset()
        self.moves = record.split(";")

        z = []
        for i in range(0, len(self.moves)):
            try:
                z.append(self.get_next(self.moves[i]))
            except IndexError as err:
                print(self.moves[i])
                print(record)
                raise err

        return z
