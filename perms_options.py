def perms(s):
    ret = []
    # string of length 1 has one permutation
    if len(s) == 1:
        ret = [s]
    else:
        # iterate through each character in s
        for i in range(len(s)):
        # find the permutations of the string minus a character
            for p in perms(s[:i] + s[i+1:]):
                # add the character into every possible position
                ret += [s[i] + p]
    return set(ret)

def permss(s):
    ret = []
    # string of length 1 has one permutation
    if len(s) == 1:
        ret = [s]
    else:
        # iterate through each character in s
        for i in range(len(s)):
        # find the permutations of the string minus a character
            for p in permss(s[:i] + s[i+1:]):
                # add the character into every possible position
                ret += [s[i] + p]
    return ret


