def parse_expr(lis, start_i, s):
    i = start_i
    while i < len(s):
        if s[i] == ")":
            return i
        elif s[i] == "(":
            paren_expr = list()
            i = parse_expr(paren_expr, i+1, s)
            lis.append(paren_expr)
        elif s[i].isdigit():
            lis.append(int(s[i]))
        elif s[i] != " ":
            lis.append(s[i])
        i+=1
    return i

def eval_expr(expr):
    if type(expr) == int:
        return expr
    elif type(expr[0]) == list:
        result = eval_expr(expr[0])
    else:
        result = expr[0]
    for i in range(1, len(expr), 2):
        rhs = expr[i+1]
        if type(rhs) == list:
            rhs = eval_expr(rhs)
        if expr[i] == "+":
            result += rhs
        else:
            result *= rhs
        
    return result

exprs = list()
for line in open("d18_input.txt"):
    line = line.strip()
    lis = list()
    expr = parse_expr(lis, 0, line)
    exprs.append(lis)

print(sum(map(eval_expr, exprs)))