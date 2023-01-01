nums = list(map(int, "0,13,16,17,1,10,6".split(",")))

previous_numbers = {nums[i]: i+1 for i in range(len(nums[:-1]))}

n = len(nums)
last_num = nums[-1]
# Part 1
# while n < 2020:
# Part 2
while n < 30000000:
    if last_num not in previous_numbers:
        previous_numbers[last_num] = n
        last_num = 0
    else:
        diff = n - previous_numbers[last_num]
        previous_numbers[last_num] = n
        last_num = diff
        
    n += 1

print(last_num)
