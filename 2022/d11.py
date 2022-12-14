import operator

op_dict = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}

DIVISOR_LCM = 1

class Monkey():
    def __init__(self, input_str, monkey_list):
        self.monkey_list = monkey_list
        self.inspection_total = 0

        input_lines = list(map(str.strip, input_str.split("\n")))
        op_tokens = input_lines[2].split(" ")

        # Parse the starting item list
        print(input_lines[1])
        colon_index = input_lines[1].index(":")
        self.items = list(map(int, input_lines[1][colon_index+2:].split(", ")))
        # Parse other members from the input
        self.monkey_id = int(input_lines[0].split(" ")[1][:-1])
        self.op_param1 = op_tokens[3]
        self.op_param2 = op_tokens[5]
        self.op_operator = op_dict[op_tokens[4]]
        self.test_divisor = int(input_lines[3].split(" ")[3])
        self.throw_dest_true = int(input_lines[4].split(" ")[5])
        self.throw_dest_false = int(input_lines[5].split(" ")[5])

        # cast op parameters as int if possible
        if self.op_param1.isdigit(): self.op_param1 = int(self.op_param1)
        if self.op_param2.isdigit(): self.op_param2 = int(self.op_param2)

        # All the divisors are primes, so we can get their lcm by multiplying
        # them together.
        global DIVISOR_LCM
        DIVISOR_LCM *= self.test_divisor

    def do_op(self, old):
        p1 = self.op_param1 if type(self.op_param1) == int else old
        p2 = self.op_param2 if type(self.op_param2) == int else old

        return self.op_operator(p1, p2)

    def do_test(self, item):
        return item % self.test_divisor == 0

    def throw(self, item, dest):
        self.monkey_list[dest].items.append(item)

    def do_turn(self):
        global DIVISOR_LCM
        # add to inspection total
        self.inspection_total += len(self.items)
        for item in self.items:
            # inspect the item
            item = self.do_op(item) % DIVISOR_LCM
            # decide where to throw it
            if self.do_test(item):
                dest = self.throw_dest_true
            else:
                dest = self.throw_dest_false
            # throw the item
            self.throw(item, dest)
        # all items thrown, clear the list
        self.items.clear()

    def print_status(self):
        print("Monkey {}:".format(self.monkey_id))
        print("\tItems: {}".format(", ".join(map(str, self.items))))
        print("\tOperation: {} {} {}".format(self.op_param1, self.op_operator, self.op_param2))
        print("\tTest: divisible by {}".format(self.test_divisor))
        print("\t\tif true: throw to monkey {}".format(self.throw_dest_true))
        print("\t\tif false: throw to monkey {}".format(self.throw_dest_false))

# Parse all the input
monkeys = list()
for monkey_str in open("2022/d11_input.txt").read().split("\n\n"):
    monkeys.append(Monkey(monkey_str, monkeys))

for m in monkeys:
    m.print_status()

n_rounds = 10000
for i in range(n_rounds):
    if i % 100 == 0: print(i)
    for m in monkeys:
        m.do_turn()

counts = [m.inspection_total for m in monkeys]
counts.sort()
print("Monkey business: ", counts[-1] * counts[-2])