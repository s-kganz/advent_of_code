def getScore(s, b, a, h):
    cap = 2*s
    dur = b*5 - a
    fla = h*5 - 2*s - 3*b
    tex = 5*a - h
    return max(cap, 0) * max(dur, 0) * max(fla, 0) * max(tex, 0)

def getCals(s, b, a, h):
    return 3*s + 3*b + 8*a + 8*h

maxscore = 0
for i in range(100):
    for j in range(100):
        if i+j > 100: break
        for k in range(100):
            if i+j+k > 100: break
            for l in range(100):
                s = i+j+k+l
                cals = getCals(i,j,k,l)
                if s > 100 or cals > 500:
                    break
                if i+j+k+l == 100 and cals == 500:
                    maxscore = max(maxscore, getScore(i, j, k, l))
print(maxscore)
