small_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

dirstack = list()
sizes = dict()

for command in map(str.strip, open("2022/d7_input.txt").readlines()):
#for command in small_input.split("\n"):
    #print(command)
    args = command.strip().split(" ")
    if args[0].isdigit():
        # this is a file
        filesize = int(args[0])
        # add size to every directory in the stack
        for i in range(len(dirstack)):
            path = "/".join(dirstack[:i+1])
            sizes[path] += filesize
    elif args[0] == "$":
        if args[1] == "ls":
            continue
        elif args[1] == "cd":
            if args[2] == "..":
                dirstack.pop()
            else:
                dirstack.append(args[2])
                if "/".join(dirstack) not in sizes: sizes["/".join(dirstack)] = 0

# Part 1
small_dir_sum = 0
for key in sizes:
    if sizes[key] <= 100000:
        small_dir_sum += sizes[key]

print(small_dir_sum)

# Part 2
space_available   = 70000000
min_unused_space  = 30000000
space_used        = sizes["/"]
curr_unused_space = space_available - space_used
space_to_delete   = min_unused_space - curr_unused_space

# Find size of smallest directory that is at least space_to_delete in size
print(min(filter(lambda x: x >= space_to_delete, sizes.values())))