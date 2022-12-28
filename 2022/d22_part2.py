CUBE_SIDE_SIZE = 50

class GameBoard:
    # Define constants
    FACE_RIGHT = 0
    FACE_DOWN  = 1
    FACE_LEFT  = 2
    FACE_UP    = 3

    STEPS = {
        FACE_RIGHT: (1, 0),
        FACE_DOWN: (0, 1),
        FACE_LEFT: (-1, 0),
        FACE_UP: (0, -1)
    }

    # This is all hardcoded for the input
    # ¯\_(ツ)_/¯
    CUBE_WRAP_RULES = {
        # Defined as (side, facing) -> 
        #   (new side, new facing, side coordinates transform)
        1: {
            FACE_UP: (6, FACE_UP, lambda t: (t[0], CUBE_SIDE_SIZE-1)),
            FACE_RIGHT: (4, FACE_LEFT, lambda t: (CUBE_SIDE_SIZE-1, CUBE_SIDE_SIZE-1-t[1])),
            FACE_DOWN: (3, FACE_LEFT, lambda t: (CUBE_SIDE_SIZE-1, t[0]))
        },
        2: {
            FACE_LEFT: (5, FACE_RIGHT, lambda t: (0, CUBE_SIDE_SIZE-1-t[1])),
            FACE_UP: (6, FACE_RIGHT, lambda t: (0, t[0]))
        },
        3: {
            FACE_RIGHT: (1, FACE_UP, lambda t: (t[1], CUBE_SIDE_SIZE-1)),
            FACE_LEFT: (5, FACE_DOWN, lambda t: (t[1], 0))
        },
        4: {
            FACE_RIGHT: (1, FACE_LEFT, lambda t: (CUBE_SIDE_SIZE-1, CUBE_SIDE_SIZE-1-t[1])),
            FACE_DOWN: (6, FACE_LEFT, lambda t: (CUBE_SIDE_SIZE-1, t[0]))
        },
        5: {
            FACE_UP: (3, FACE_RIGHT, lambda t: (0, t[0])),
            FACE_LEFT: (2, FACE_RIGHT, lambda t: (0, CUBE_SIDE_SIZE-1-t[1]))
        },
        6: {
            FACE_DOWN: (1, FACE_DOWN, lambda t: (t[0], 0)),
            FACE_RIGHT: (4, FACE_UP, lambda t: (t[1], CUBE_SIDE_SIZE-1)),
            FACE_LEFT: (2, FACE_DOWN, lambda t: (t[1], 0))
        }
    }

    CHAR_OPEN  = '.'
    CHAR_WALL  = '#'
    CHAR_BLANK  = ' '
    CHAR_OB = None

    
    def __init__(self, board):
        self.tiles = dict()
        # The board does not have internal gaps, so we can represent the valid
        # range of coordinates on each axis as [min, max].
        self.x_range = dict()
        self.y_range = dict()

        lines = board.split("\n")
        for y in range(len(lines)):
            # Although the coordinates in this problem are 1-indexed, they are represented
            # as 0-indexed.
            self.tiles[y] = list()
            # Line is always pre-padded with spaces if they are present
            self.x_range[y] = (lines[y].count(self.CHAR_BLANK), len(lines[y])-1)
            for x in range(len(lines[y])):
                if lines[y][x] == self.CHAR_BLANK:
                    continue

                if x not in self.y_range:
                    self.y_range[x] = (y, y)
                
                self.y_range[x] = self.y_range[x][0], y

                self.tiles[y].append(lines[y][x])

    def _inbounds(self, x, y):
        # Determine if coordinates (x, y) are inbounds.
        if y in self.x_range:
            return self.x_range[y][0] <= x <= self.x_range[y][1]
        if x in self.y_range:
            return self.y_range[x][0] <= y <= self.y_range[x][1]
        
        # Coordinates are outside of the bounding rectangle
        return False

    def _get_character(self, x, y):
        # Get tile at (x, y)
        if not self._inbounds(x, y):
            return self.CHAR_OB
        list_len = len(self.tiles[y])
        x_ind = (x - self.x_range[y][0]) % list_len
        return self.tiles[y][x_ind]

    def _map_to_side(self, mx, my):
        # Get the (sx, sy) position within the cube side at the map
        # coordinates (mx, my). Note that side coordinates are still
        # in the orientation of the map view.
        return mx % CUBE_SIDE_SIZE, my % CUBE_SIDE_SIZE

    def _side_to_map(self, side, sx, sy):
        # Get the (mx, my) position on the map given the side and side
        # coordinates (sx, sy)
        if side == 1:
            return sx + 2*CUBE_SIDE_SIZE, sy
        if side == 2:
            return sx + CUBE_SIDE_SIZE, sy,
        if side == 3:
            return sx + CUBE_SIDE_SIZE, sy + CUBE_SIDE_SIZE
        if side == 4:
            return sx + CUBE_SIDE_SIZE, sy + 2*CUBE_SIDE_SIZE
        if side == 5:
            return sx, sy + 2*CUBE_SIDE_SIZE
        if side == 6:
            return sx, sy + 3*CUBE_SIDE_SIZE

    def _get_side(self, x, y):
        # Get the cube side corresponding to the map coordinates (x, y)
        z = y // CUBE_SIDE_SIZE
        if z == 0:
            return 1 if x > CUBE_SIDE_SIZE * 2 else 2
        elif z == 1:
            return 3
        elif z == 2:
            return 4 if x > CUBE_SIDE_SIZE else 5
        elif z == 3:
            return 6

    def _do_cube_wrap(self, x, y, facing):
        side = self._get_side(x, y)
        newside, newfacing, transform = self.CUBE_WRAP_RULES[side][facing]
        sx, sy = self._map_to_side(x, y)
        newsx, newsy = transform((sx, sy))
        newx, newy = self._side_to_map(newside, newsx, newsy)
        return newx, newy, newfacing

    def _do_step(self, x, y, facing):
        # Return resulting coordinates when moving forward from (x, y) 
        # in the given direction.
        dx, dy = self.STEPS[facing]
        newx, newy, newfacing = x + dx, y + dy, facing
        if not self._inbounds(newx, newy):
            print("Wrap on seam")
            newx, newy, newfacing = self._do_cube_wrap(x, y, facing)
        # only return the new coordinates if we don't hit a wall
        if not self._inbounds(newx, newy):
            print("cube wrapping produced OB coordinates")
        return (newx, newy, newfacing) if self._get_character(newx, newy) != self.CHAR_WALL else (x, y, facing)

    def _print_path_state(self, x, y, facing):
        print(
            "X: {}, Y: {}, Facing: {}, Cube side: {}".format(
                x, y, facing, self._get_side(x, y)
            )
        )

    def walk(self, path, debug=False):
        # Process sequence of commands in `path`
        # Initial coords is the leftmost tile in the top row
        y = min(self.x_range.keys())
        x = self.x_range[y][0]
        facing = self.FACE_RIGHT
        print("Initial state: ", x, y, facing)
        for command in path:
            if isinstance(command, int):
                if debug: 
                    print("-Walking {} steps with facing {}-".format(command, facing))
                for _ in range(command):
                    newx, newy, newfacing = self._do_step(x, y, facing)
                    if (newx, newy) == (x, y):
                        # no change in position
                        if debug: print("Hit a wall, stopping movement")
                        break
                    x, y, facing = newx, newy, newfacing
                    if debug:
                        self._print_path_state(x, y, facing)
            else:
                # mawarimasu
                facing = (facing + (1 if command == "R" else -1)) % 4
                if debug: 
                    print("-Turning to new facing {}-".format(command))
                    self._print_path_state(x, y, facing)
        
        return (x, y, facing)

    def __repr__(self):
        y_range_str = "Y ranges:\n" + "\n".join(
            "{}: {}".format(key, self.y_range[key]) for key in sorted(self.y_range.keys())
        )
        x_range_str = "X ranges:\n" + "\n".join(
            "{}: {}".format(key, self.x_range[key]) for key in sorted(self.x_range.keys())
        )
        return y_range_str + "\n" + x_range_str

def parse_path(path):
    # Parse the path string into a series of commands
    path_commands = []
    i = 0
    token = ""
    while i < len(path):
        if path[i].isdigit():
            # next character is a number, continue reading it
            token += path[i]
        elif token.isdigit() and not path[i].isspace():
            path_commands.append(int(token))
            token = ""
            path_commands.append(path[i])
        i += 1
    # Possibly add a token at the end of the path sequence
    if token.isdigit():
        path_commands.append(int(token))
    return path_commands

board, path = tuple(open("2022/d22_input.txt").read().split("\n\n"))
gb = GameBoard(board)
# print(gb)

commands = parse_path(path)

col, row, facing = gb.walk(commands, debug=True)
print("Final col: {}".format(col+1))
print("Final row: {}".format(row+1))
print("Facing: {}".format(facing))
print("Password: {}".format(1000*(row+1) + 4*(col+1) + facing))
