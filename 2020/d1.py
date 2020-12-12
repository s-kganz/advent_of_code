lines = list(map(lambda x: int(x.strip()), list(open("d1_input.txt"))))

for a in lines:
    for b in lines:
        if a+b > 2020: continue
        for c in lines:
            if a+b+c == 2020:
                print(a*b*c)