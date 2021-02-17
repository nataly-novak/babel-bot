import random
from vars import *

def roll(die, amnt = 1):
    res = 0
    for i in range(amnt):
        res += random.randrange(1, die+1)
    return res

def attack(BAB, weapon_die, weapon_damage, multiplier, AC):
    crit = False
    hit = False
    roller = roll(20)
    print(roller)
    if roller ==20:
        hit = True
        if roll(20)+BAB >= AC:
            crit = True
    elif roller == 1:
        hit = False
    elif roller + BAB >= AC:
        hit = True
    else:
        hit = False
    if hit:
        if crit:
            rolls =0
            for i in range(multiplier):
                rolls += roll(weapon_die)
            return [rolls+multiplier*weapon_damage, "Critical Hit!"]
        else:
            return [roll(weapon_die)+weapon_damage, "Hit"]
    else:
        return [0, "Miss"]

def bomb(BAB, AC, amnt = 3, damage = 4):
    crit = False
    hit = False
    roller = roll(20)
    print(roller)
    if roller == 20:
        hit = True
        if roll(20) + BAB >= AC-10:
            crit = True
    elif roller == 1:
        hit = False
    elif roller + BAB >= AC-10:
        hit = True
    else:
        hit = False
    if hit:
        if crit:
            return [roll(6,amnt+1)+2*damage, "Critical Hit!"]
        else:
            return [roll(6, amnt)+damage, "Hit"]
    else:
        return [0, "Miss"]

def channeling():
    return roll(6, channel_dies)


def ranpop(number, length):
    nms = []
    lst = list(range(length))
    for i in range(number):
        ln = len(lst)
        j = random.randrange(0,ln)
        nms.append(lst.pop(j))
    return nms

