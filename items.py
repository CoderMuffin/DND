class ItemEnum:
    KEY = "o¬¬"
    BOSSKEY = "@=@"
    POTION = " ᵿ "

class ItemEnum2:
    l = [
        ItemEnum.KEY, ItemEnum.BOSSKEY, ItemEnum.POTION, ItemEnum.POTION,
        ItemEnum.POTION, ItemEnum.POTION
    ]


class PotionEnum:
    RED = 0
    BLUE = 1
    YELLOW = 2
    PURPLE = 3


def item_name_to_color(name):
    if name=="Red Potion":
        return "\033[1;31m"
    elif name=="Blue Potion":
        return "\033[1;35m"
    elif name=="Yellow Potion":
        return "\033[1;33m"
    elif name=="Purple Potion":
        return "\033[1;34m"
    else:
        return "no color"

class Item:
    def __init__(self, idn):
        self.idn = idn
        if idn == 0:
            self.name = "Red Potion"
            self.effect = Effect(0, 1)
        elif idn == 1:
            self.name = "Blue Potion"
            self.effect = Effect(1, 1)
        elif idn == 2:
            self.name = "Yellow Potion"
            self.effect = Effect(2, 3)
        elif idn == 3:
            self.name = "debug"

    def __str__(self):
        return self.name


class Effect:
    def __init__(self, idn, duration):
        self.idn = idn
        self.duration = duration
        self.maxduration = duration

    def inflict(self, plr):
        if self.idn == 0:
            plr.hp = plr.base.maxhp
        elif self.idn == 1:
            for attack in plr.base.attacks:
                attack.damage += 2
        elif self.idn == 2:
            plr.shielded = True
