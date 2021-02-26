from mechanics import attack, bomb, channeling
from vars import *

class Pommer:
    def __init__(self, user, hp = player_hp, ac = player_ac , damage = pommer_damage, attack = player_bab, total = 0, poms = "", staggered = 2):
        self.user = user
        self.hp = hp
        self.ac = ac
        self.damage = damage
        self.attack = attack
        self.total = total
        self.poms = poms
        self.staggered = staggered

    def __str__(self):
        ln = "USER: " + str(self.user)+ ", HP:" + str(self.hp) + ", AC: " +str(self.ac)+", DAMAGE: "+ str(self.damage)+", ATTACK: "+ str(self.attack)+ ", STAGGERED: "+str(self.staggered)
        return ln


    def shield(self, bonus):
        self.ac += bonus
        return[0, "defended!"]

    def sword(self, defence, additional):
        return attack(self.attack+additional, 6, self.damage, 2, defence)

    def axe(self, defence, additional):
        return attack(self.attack+additional, 8, self.damage, 3, defence)

    def fire(self, defence):
        return bomb(self.attack, defence)

    def heal (self, healed):
        print(self.user, " healed ", healed)
        self.hp = min(self.hp+healed, 100)
        if self.staggered == 0:
            self.staggered = 1
        return [healed,"healed!"]

    def suffer(self, amount):
        print("Amount", amount)
        print("self.hp.before", self.hp)
        res= max(self.hp - amount, 0)
        self.hp = res
        print("self.hp.after", self.hp)
        if res ==0:
            self.staggered = 0
            return [amount, "staggered!"]
        else:
            return [amount, "damaged!"]




    def action(self, name, target, additional=0):

        if name == "sword":
            return self.sword(target, additional)
        elif name == "axe":
            return self.axe(target, additional)
        elif name == "bomb":
            return self.fire(target)
        elif name == "defence":
            return self.shield(target)
        elif name == "heal":
            return self.heal(target)


