class ItemEnum:
    KEY = "🔑"
    BOSSKEY = "@"
    POTION = "ᵿ"


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
