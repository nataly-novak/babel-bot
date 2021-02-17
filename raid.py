from mechanics import attack, roll
from vars import *

class Raid:
    def __init__(self, stamp, amnt, mmbr, acts = "",trg = trigger_start, attacks = "", bhp = dragon_hp, vhp= village_hp, bab = dragon_bab, ac = dragon_ac, save = 5 , damage = dragon_damage):
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

    def __str__(self):
        ln = self.stamp +"; "+self.mmbr+ "; TRiggered: "+str(self.trg)+ ", HP: "+ str(self.bhp)+ ", VHP: "+str(self.vhp)
        return ln

    def physical(self, defence):
        return attack(self.bab, 6, self.damage, 2, defence)

    def burn(self):
        damage = roll(bomb_dies,6)
        self.vhp = max(0, self.vhp-damage)
        return [damage, "Village is burning!"]



