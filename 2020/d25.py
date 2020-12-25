key1 = 5099500
key2 = 7648211

def do_transform(val, subj, divisor):
    val *= subj
    val %= divisor
    return val

def get_loop_size(subj, target):
    val = 1
    n = 0
    while val != target:
        val = do_transform(val, subj, 20201227)
        n += 1
    return n

loop1 = get_loop_size(7, key1)
loop2 = get_loop_size(7, key2)

enc_key = 1
for _ in range(loop2):
    enc_key = do_transform(enc_key, key1, 20201227)

enc_key2 = 1
for _ in range(loop1):
    enc_key2 = do_transform(enc_key2, key2, 20201227)

print(enc_key)
print(enc_key2)