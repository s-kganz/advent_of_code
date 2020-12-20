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
    for i in range(len(expr)):
        if type(expr[i]) == list:
            expr[i] = eval_expr(expr[i])
    new_expr = list()
    result = expr[0]
    i = 1
    while i < len(expr):
        if expr[i] == "+":
            result += expr[i+1]
            if i == len(expr) - 2:
                new_expr.append(result)
        else:
            new_expr.append(result)
            new_expr.append(expr[i])
            if i == len(expr)-2: new_expr.append(expr[i+1])
            else: result = expr[i+1]
        i += 2
    if len(new_expr) == 0: # no *'s in the expr
        return result
    result = new_expr[0]
    for i in range(2, len(new_expr), 2):
        result *= new_expr[i]
    return result



exprs = list()
for line in open("d18_input.txt"):
    line = line.strip()
    lis = list()
    expr = parse_expr(lis, 0, line)
    exprs.append(lis)

print(sum(map(eval_expr, exprs)))