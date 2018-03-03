import unittest
import textwrap
from pprint import pprint

columns = list('abcdefghi')

def square(dim):
    return [['0' for i in range(dim)] for j in range(dim)]

def is_wall(move):
    if len(move) == 2:
        return False
    elif len(move) == 3:
        return True
    else:
        raise Exception(move)

def is_movement(move):
    return not is_wall(move)

def get_walls(moves):
    return list(filter(is_wall, moves))

def find_position(moves, default):
    filtered = list(filter(is_movement, moves))
    if len(filtered) > 0:
        return filtered[-1]
    else:
        return default

def find_walls(moves, direction):
    filtered = filter(lambda wall: wall[-1] == direction, get_walls(moves))
    return [wall[:2] for wall in filtered]

def out_square(lst):
    rows = [''.join(row) for row in lst]
    return '\n'.join(rows)

def out_walls(moves, direction):
    occupied = square(8)

    for wall in find_walls(moves, direction):
        col = columns.index(wall[0])
        row = 8 - int(wall[1])
        occupied[row][col] = '1'

    return out_square(occupied)

def out_pawn(location):
    col = columns.index(location[0])
    row = 9 - int(location[1])

    occupied = square(9)
    occupied[row][col] = '1'

    return out_square(occupied)

def out_expected(expected):
    horizontal = out_walls([expected], 'h')
    vertical = out_walls([expected], 'v')

    if is_movement(expected):
        pawn = out_pawn(expected)
    else:
        pawn = out_square(square(9))

    return (horizontal, vertical, pawn)

def rotate(square, should_rotate):
    if should_rotate == False:
        return square

    lst = list(map(lambda row: row[::-1], square.split('\n')))

    rows = [''.join(row) for row in lst[::-1]]
    return '\n'.join(rows)

def convert_one(moves, expected):
    horizontal_walls = out_walls(moves, 'h')
    vertical_walls = out_walls(moves, 'v')

    x_moves = moves[0::2]
    o_moves = moves[1::2]

    x_location = find_position(x_moves, 'e1')
    o_location = find_position(o_moves, 'e9')

    x_pawn = out_pawn(x_location)
    o_pawn = out_pawn(o_location)

    x_walls_left = 10 - len(get_walls(x_moves))
    o_walls_left = 10 - len(get_walls(o_moves))

    expected_horizontal, expected_vertical, expected_pawn = out_expected(expected)

    should_rotate = False
    if len(moves) % 2 == 1:
        should_rotate = True

    return "\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n-\n\n%s\n\n%s\n\n%s\n" % (
        rotate(horizontal_walls, should_rotate),
        rotate(vertical_walls, should_rotate),
        rotate(x_pawn, should_rotate),
        x_walls_left,
        rotate(o_pawn, should_rotate),
        o_walls_left,
        rotate(expected_horizontal, should_rotate),
        rotate(expected_vertical, should_rotate),
        rotate(expected_pawn, should_rotate),
    )

def convert(record):
    split = record.split(";")

    z = []
    for i in range(1, len(split)):
        z.append(convert_one(split[0:i-1], split[i]))

    return z


class Test(unittest.TestCase):
    record = "e2;e8;e3;e7;e4;e6;e3h;e5;c3h;e5h;d3v;g5h;d1v;d5v;g3h;a3h;h6v;h2v;h8v;f4;f3v;f5;e5;g5;f5;g4;g5;h4;h5;i4;i5;i3"

    def test_is_wall_nope(self):
        self.assertEqual(is_wall('e2'), False)

    def test_is_wall_yes(self):
        self.assertEqual(is_wall('e3h'), True)

    def test_find_position(self):
        self.assertEqual(find_position(['e2', 'e3', 'e4', 'e3h', 'c3h', 'd3v'], 'e1'), 'e4')

    def test_find_position_no_move(self):
        self.assertEqual(find_position(['e3h', 'c3h', 'd3v'], 'e1'), 'e1')

    def test_get_walls_horizontal(self):
        self.assertEqual(find_walls(['e2', 'e3', 'e4', 'e3h', 'c3h', 'd3v'], 'h'), ['e3', 'c3'])

    def test_get_walls_vertical(self):
        self.assertEqual(find_walls(['e2', 'e3', 'e4', 'e3h', 'c3h', 'd3v'], 'v'), ['d3'])

    def test_one(self):
        self.assertEqual(convert_one("e2;e8;e3;e7;e4;e6;e3h;e5;c3h;e5h;d3v;g5h".split(";"), "d1v"), textwrap.dedent(
            """
                00000000
                00000000
                00000000
                00001010
                00000000
                00101000
                00000000
                00000000

                00000000
                00000000
                00000000
                00000000
                00000000
                00010000
                00000000
                00000000

                000000000
                000000000
                000000000
                000000000
                000000000
                000010000
                000000000
                000000000
                000000000

                7

                000000000
                000000000
                000000000
                000000000
                000010000
                000000000
                000000000
                000000000
                000000000

                8

                -

                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000

                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00010000

                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
            """
        ))

    def test_rotation(self):
        self.assertEqual(convert_one("e2;e8;e3;e7;e4;e6;e3h;e5;c3h;e5h;d3v".split(";"), "g5h"), textwrap.dedent(
            """
                00000000
                00000000
                00010100
                00000000
                00010000
                00000000
                00000000
                00000000

                00000000
                00000000
                00001000
                00000000
                00000000
                00000000
                00000000
                00000000

                000000000
                000000000
                000000000
                000010000
                000000000
                000000000
                000000000
                000000000
                000000000

                7

                000000000
                000000000
                000000000
                000000000
                000010000
                000000000
                000000000
                000000000
                000000000

                9

                -

                00000000
                00000000
                00000000
                00000000
                01000000
                00000000
                00000000
                00000000

                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000

                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
            """
        ))


    def test_border(self):
        self.assertEqual(convert_one(["a1h", "h8v"], "e2"), textwrap.dedent(
            """
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                10000000

                00000001
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000

                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000010000

                9

                000010000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000

                9

                -

                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000

                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000
                00000000

                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000000000
                000010000
                000000000
            """
        ))

if __name__ == "__main__":
    unittest.main()
