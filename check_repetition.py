a = '123'

def repetition(stringg):
    substringg = ''
    for character in stringg:
        substringg += character
        if len(stringg) % len(substringg) == 0:
            if (len(stringg) // len(substringg)) * substringg == stringg:
                return substringg