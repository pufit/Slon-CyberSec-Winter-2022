

def check(num):
    s = str(num)
    if len(s) > 8:
        raise OverflowError()
    if (len(s) == 4) or (len(s) % 2):
        return False
    if sum(map(int, list(s[:len(s)//2]))) == sum(map(int, list(s[len(s)//2:]))) == 4:
        return True
    return False
