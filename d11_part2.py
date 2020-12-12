from copy import deepcopy

lines = list(map(lambda x: list(x.strip().replace("L", "#")), open("d11_input.txt")))

def print_board(board):
    print("\n".join(map(lambda x: "".join(x), board)))
    print()

def look_dirxn(drow, dcol, row, col, board):
    # return the first non-floor character seen, or none if edge hit
    row += drow
    col += dcol
    while 0 <= row < len(board) and 0 <= col < len(board[row]):
        if board[row][col] != ".":
            return board[row][col] == "#"
        row += drow
        col += dcol
    return 0

while True:
    new_board = list()
    did_change = False
    for i in range(len(lines)):
        new_line = lines[i].copy()
        for j in range(len(lines[i])):
            if lines[i][j] == ".": continue
            seat_count = 0
            for drow in range(-1, 2):
                for dcol in range(-1, 2):
                    if drow == dcol == 0: continue
                    seat_count += look_dirxn(drow, dcol, i, j, lines)
            if seat_count >= 5 and lines[i][j] == "#":
                new_line[j] = "L"
            elif seat_count == 0 and lines[i][j] == "L":
                new_line[j] = "#"
        if new_line != lines[i]:
            did_change = True
        new_board.append(new_line)
    lines = deepcopy(new_board)
    if not did_change: break
    

# sum the occupied seats
tot_seats = 0
for row in lines:
    tot_seats += sum(map(lambda x: x == "#", row))

print(tot_seats)