from http.client import NETWORK_AUTHENTICATION_REQUIRED


data = open("2022/d6_input.txt").read().strip()

#data = "nppdvjthqldpwncqszvftbrmjlhg"

# Part 1
'''
for i in range(4, len(data)):
    if len(set(data[i-3:i+1])) == 4:
        print(i+1)
        break
'''
# Part 2
'''
for i in range(14, len(data)):
    if len(set(data[i-13:i+1])) == 14:
        print(i+1)
        break
'''