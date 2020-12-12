slope = list(map(lambda x: x.strip(), list(open("d3_input.txt"))))

def test_slope(drow, dcol):
    pos = [0, 0] # row, col
    tree_ct = 0
    line_len = len(slope[0])
    while pos[0] < len(slope):
        if slope[pos[0]][pos[1]] == '#':
            tree_ct += 1
        
        pos[0] += drow
        pos[1] += dcol
        pos[1] %= line_len
    
    return tree_ct

treeprod = test_slope(1, 1) * test_slope(1, 3) * test_slope(1, 5) * test_slope(1, 7) * test_slope(2, 1)
print(treeprod)