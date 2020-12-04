class ItemEnum:
    KEY=0
    BOSSKEY=1
    RPOTION=2
    BPOTION=3
    YPOTION=4

def assert_item_name(idn):
    return ["Key", "Boss Key", "Red Potion", "Blue Potion", "Yellow Potion"][idn]

class Item:
    def __init__(self,idn):
        self.battle_usable = idn in [2,3,4]
        self.idn=idn
        self.name=assert_item_name(idn)

    def action(self,plr):
        if not self.battle_usable:
            print("You can't use this item here.")
            return False
        if self.idn==ItemEnum.RPOTION:
            plr.buffs.append(Effect(0,1))
        if self.idn==ItemEnum.BPOTION:
            plr.buffs.append(Effect(1,1))
        if self.idn==ItemEnum.YPOTION:
            plr.buffs.append(Effect(2,2))

        return True
            
    def draw(self):
        return ["o¬¬","@=@","\033[91m ᵿ \033[0m","\033[96m ᵿ \033[0m","\033[93m ᵿ \033[0m"][self.idn]

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
