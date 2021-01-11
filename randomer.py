import random

def coin():
    res =["Yes", "No"]
    n = random.randrange(2)
    return res[n]

def rannum(number, amount = 1):
    numbers = list(range(1,number+1))
    resp = ""
    for i in range(amount):
        n = random.randrange(len(numbers))
        resp += str(numbers.pop(n))+", "
    return resp[:-2]

