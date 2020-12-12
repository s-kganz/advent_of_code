from copy import deepcopy

lines = list(map(lambda x: list(x.strip().replace("L", "#")), open("d11_input.txt")))

def print_board(board):
    print("\n".join(map(str, board)))
    print()

while True:
    did_change = False
    new_board = list()
    for i in range(len(lines)):
        new_line = lines[i].copy()
        for j in range(len(lines[i])):
            if lines[i][j] == ".": continue
            seat_count = 0
            for drow in range(-1, 2):
                for dcol in range(-1, 2):
                    if drow == dcol == 0: continue
                    # Check if valid coordinates
                    if 0 <= i + drow < len(lines) and 0 <= j + dcol < len(lines[i]):
                        seat_count += (lines[i+drow][j+dcol] == "#")
            if seat_count == 0 and lines[i][j] == "L":
                new_line[j] = "#"
            elif seat_count >= 4 and lines[i][j] == "#":
                new_line[j] = "L"
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

