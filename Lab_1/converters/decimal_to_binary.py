from constants import BIT_LENGTH

def trans_into_straight(given_number : int )-> list[int]:
    sign = given_number>=0
    given_number = abs(given_number)
    bits = [0] * BIT_LENGTH
    index = BIT_LENGTH - 1
    while given_number>0 and index>=0:
        bits[index] =  given_number%2
        given_number //=2
        index -=1
    if not sign:
        bits[0] = 1
    return bits

def trans_into_reverse(given_number: int)->list[int]:
    
    bits = trans_into_straight(given_number)
    if given_number >= 0: 
        return bits
    for i in range(1,BIT_LENGTH):
        if bits[i] == 1: bits[i] = 0
        else: bits[i] = 1
    return bits

def trans_into_additional(given_number: int) -> list[int]:
    if given_number >= 0:
        return trans_into_straight(given_number)

    bits = trans_into_reverse(given_number)

    carry = 1
    for i in range(BIT_LENGTH - 1, -1, -1):
        temp = bits[i] + carry
        bits[i] = temp % 2
        carry = temp // 2

    return bits