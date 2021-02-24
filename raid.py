from mechanics import attack, roll
from vars import *

class Raid:
    def __init__(self, stamp, amnt, mmbr, acts = "",trg = trigger_start, attacks = "", bhp = dragon_hp, vhp= village_hp, bab = dragon_bab, ac = dragon_ac, save = 5 , damage = dragon_damage, effect = ""):
        self.stamp = stamp
        self.amnt = amnt
        self.mmbr = mmbr
        self.acts = acts
        self.trg = trg
        self.attacks = attacks
        self.bhp = bhp
        self.vhp = vhp
        self.bab = bab
        self.ac = ac
        self.save = save
        self.damage = damage
        self.effect = effect

    def __str__(self):
        ln = self.stamp +"; "+self.mmbr+ "; TRiggered: "+str(self.trg)+ ", HP: "+ str(self.bhp)+ ", VHP: "+str(self.vhp) + " CURRENT EFFECT: "+ str(self.effect)
        return ln

    def physical(self, defence):
        return attack(self.bab, 6, self.damage, 2, defence)

    def burn(self):
        damage = roll(bomb_dies,6)
        self.vhp = max(0, self.vhp-damage)
        return [damage, "Village is burning!"]

    def mystery(self):
        probabilities = {"ac":range(50), "damage": range(50,75), "attack": range(75,88), "trigger": range(88,94), "hp": range(94, 97), "vulnerable": (97, 99), "stagger":(99, 100)}
        r = roll(100)
        for probs in probabilities:
            if r in probabilities[probs]:
                self.effect = probs
        if self.effect == "ac":
            self.ac -= 5
            message = "Dragon's defence for that round was lowered\n"
        elif self.effect == "damage":
            self.damage -= 3
            message = "Dragon's damage for that round was lowered\n"
        elif self.effect == "attack":
            self.bab -= 5
            message = "Dragon's attack for that round was lowered\n"
        elif self.effect == "trigger":
            self.trg = trigger_start + breath_cooldown
            message = "Dragon's next breath attack is delayed\n"
        elif self.effect == "hp":
            self.hp -= 50
            message = "Dragon lost 50 hp\n"
        elif self.effect == "vulnerable":
            message = "Dragon is more vulnerable for this round\n"
        elif self.effect == "stagger":
            message = "Dragon is unable to act for this round\n"
        return message








