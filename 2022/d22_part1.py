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

    CHAR_OPEN  = '.'
    CHAR_WALL  = '#'
    CHAR_BLANK  = ' '
    CHAR_OB = None

    CUBE_TILE_SIZE = 50
    
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

    def _do_map_step(self, x, y, facing):
        # Return resulting coordinates when moving forward from (x, y) 
        # in the given direction.
        dx, dy = self.STEPS[facing]
        newx, newy = x + dx, y + dy
        if not self._inbounds(newx, newy):
            if facing == self.FACE_UP:
                # walked off the edge upward, get the max valid y in this column
                newx, newy = newx, self.y_range[x][1]
            if facing == self.FACE_DOWN:
                # walked off the edge downward, get the min valid y in this column
                newx, newy = newx, self.y_range[x][0]
            if facing == self.FACE_LEFT:
                # walked off the edge leftward, get the max valid x in this row
                newx, newy = self.x_range[y][1], newy
            if facing == self.FACE_RIGHT:
                # walked off the edge rightward, get the min valid x in this row
                newx, newy = self.x_range[y][0], newy
        # only return the new coordinates if we don't hit a wall
        return (newx, newy) if self._get_character(newx, newy) != self.CHAR_WALL else (x, y)

    def _print_path_state(self, x, y, facing):
        print("X: {}, Y: {}, Facing: {}".format(x, y, facing))

    def walk(self, path):
        # Process sequence of commands in `path`
        # Initial coords is the leftmost tile in the top row
        y = min(self.x_range.keys())
        x = self.x_range[y][0]
        facing = self.FACE_RIGHT
        print("Initial state: ", x, y, facing)
        for command in path:
            if isinstance(command, int):
                # print("-Walking {} steps with facing {}-".format(command, facing))
                for _ in range(command):
                    newx, newy = self._do_map_step(x, y, facing)
                    if (newx, newy) == (x, y):
                        # no change in position
                        # print("Hit a wall, stopping movement")
                        break
                    x, y = self._do_map_step(x, y, facing)
                    # self._print_path_state(x, y, facing)
            else:
                # mawarimasu
                # print("-Turning to new facing {}-".format(command))
                facing = (facing + (1 if command == "R" else -1)) % 4
                # self._print_path_state(x, y, facing)
        
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

col, row, facing = gb.walk(commands)
print("Final col: {}".format(col+1))
print("Final row: {}".format(row+1))
print("Facing: {}".format(facing))
print("Password: {}".format(1000*(row+1) + 4*(col+1) + facing))
