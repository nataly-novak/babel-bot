from mechanics import attack, bomb, channeling

class Pommer:
    def __init__(self, user, hp = 100, ac = 15 , damage = 3, attack = 10, total = 0, poms = ""):
        self.user = user
        self.hp = hp
        self.ac = ac
        self.damage = damage
        self.attack = attack
        self.total = total
        self.poms = poms

    def __str__(self):
        ln = "USER: " + str(self.user)+ ", HP:" + str(self.hp) + ", AC: " +str(self.ac)+", DAMAGE: "+ str(self.damage)+", ATTACK: "+ str(self.attack)
        return ln


    def shield(self, bonus):
        self.ac += bonus
        return[0, "Defended!"]

    def sword(self, defence):
        return attack(self.attack, 6, self.damage, 2, defence)

    def axe(self, defence):
        return attack(self.attack, 8, self.damage, 3, defence)

    def fire(self, defence):
        return bomb(self.attack, defence)

    def heal (self):
        healed = channeling()
        self.hp = min(self.hp+healed, 100)
        return [healed,"Healed!"]




    def action(self, name, target):

        if name == "sword":
            return self.sword(target)
        elif name == "axe":
            return self.axe(target)
        elif name == "fire":
            return self.fire(target)
        elif name == "defence":
            return self.shield(target)
        elif name == "heal":
            return self.heal()


