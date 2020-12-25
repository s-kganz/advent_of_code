import time

class Node():
    def __init__(self, prev, nxt, val, in_cycle):
        self.prev = prev
        self.next = nxt
        self.val = val
        self.in_cycle = in_cycle
    
    def print(self):
        ptr = self
        while ptr.next is not None and ptr.next != self:
            print("{}".format(ptr.val), end="")
            ptr = ptr.next
        print("{}".format(ptr.val))

# build a linked list with a map of values to nodes
inp = "962713854"
nodemap = dict()
head = Node(None, None, int(inp[0]), True)
nodemap[head.val] = head
maxval = head.val
lead_node = head
for char in inp[1:]:
    val = int(char)
    new_node = Node(lead_node, None, val, True)
    nodemap[val] = new_node
    maxval = max(maxval, val)
    lead_node.next = new_node
    lead_node = new_node
for i in range(10, 1000000+1):
    val = i
    new_node = Node(lead_node, None, val, True)
    nodemap[val] = new_node
    maxval = max(maxval, val)
    lead_node.next = new_node
    lead_node = new_node

lead_node.next = head
head.prev = lead_node

def do_move(cup):
    ptr = cup.next
    outhead = ptr
    for _ in range(3):
        ptr.in_cycle = False
        ptr = ptr.next
    cup.next = ptr
    outtail = ptr.prev
    ptr.prev = cup

    dstn = cup.val-1
    while dstn == 0 or not nodemap[dstn].in_cycle:
        dstn -= 1
        if dstn <= 0: dstn = maxval
    
    dstn_node = nodemap[dstn]
    outtail.next = dstn_node.next
    dstn_node.next.prev = outtail
    dstn_node.next = outhead
    outhead.prev = dstn_node

    outhead.in_cycle = True
    outhead.next.in_cycle = True
    outtail.in_cycle = True

    return cup.next

t1 = time.time()
for _ in range(10000000):
    head = do_move(head)
delta = time.time() - t1

print(nodemap[1].next.val * nodemap[1].next.next.val)
print("Elapsed time: {:.2f} seconds".format(delta))