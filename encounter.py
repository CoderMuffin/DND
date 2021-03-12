from PUtils import *
from items_v2 import *


class EnemyEnum:
    UNDEAD = 0
    SKELETON = 1
    BOSS = 2


class Attack:
    def __init__(self, name, damage, rand, chance, beneficial=False, glo=False, mp=0, recoil=0):
        self.beneficial = beneficial
        self.name = name
        self.damage = damage
        self.rand = rand
        self.chance = chance
        self.mp = mp
        self.glo = glo
        self.recoil = recoil

    def inflict(self):
        import random
        return self.damage + int(random.randint(-self.rand, self.rand))


class Enemy:
    def __init__(self, idn):
        self.base = EnemyType(idn)
        self.name = self.base.typename
        self.hp = self.base.maxhp
        self.xp = self.base.xpr

    def fight(self, encounter):
        import random
        chances = []
        index = 0
        for i in self.base.attacks:
            for i in range(i.chance):
                chances.append(index)
            index += 1
        cid = self.base.attacks[random.choice(chances)]
        return cid

    def damage(self, d):
        self.hp -= d
        if self.hp <= 0:
            return False
        else:
            return True

class Boss(Enemy):
    def __init__(self, idn, skin):
        self.skin = skin
        super().__init__(idn)

class EnemyType:
    def __init__(self, idn):
        types = ["UNDEAD", "SKELETON", "BOSS"]
        hps = [10, 15, 40]
        xps = [4, 8, 25]
        self.attacks = self._attacks(idn).copy()
        self.typename = types[idn]
        self.maxhp = hps[idn]
        self.xpr = xps[idn]

    def _attacks(self, idn):
        if idn == 0:
            return [Attack("Flail", 2, 1, 5), Attack("Kick", 5, 1, 1)]
        elif idn == 1:
            return [Attack("Flail", 2, 1, 2), Attack("Bowshot", 3, 0, 3)]
        elif idn == 2:
            return [Attack("Smash", 5, 2, 3),Attack("Roar", 6, 3, 1), Attack("Fire Breath", 7, 1, 2), Attack("Rage", 8, 1, 1), Attack("Heal", 3, 1, 1, beneficial=True)]
    
class Encounter:
    def __init__(self, players, enemies):
        self.enemies = enemies
        self.players = players

    def trigger(self):
        flash()
        for p in self.players:
            p.mp = p.base.maxmp
        while True:
            clear()

            print()
            for enemy in self.enemies:
                
                if isinstance(enemy,Boss):
                    import os
                    os.system("cat "+enemy.skin)
                    print()
                useenemy(enemy, enemy.fight(self), self)
                print()
            for enemy in self.enemies:
                printEnemyHp(enemy)
            for player in self.players:
                printPlayerHp(player)
            for player in self.players:
                if player.hp <= 0:
                    self.players.remove(player)
            if self.players == []:
                print("You lost")
                return False
            for player in self.players:
                for buff in player.buffs:
                    buff.duration -= 1
                    if buff.duration < 0:
                        player.buffs.remove(buff)
                        if buff.idn == 1:
                            player.base = PlayerBase(
                                getattr(PlayerEnum,
                                        player.cls))  #reset attack dmg
                        if buff.idn == 2:
                            player.shielded = False
                print(player.name + ":",
                      "HP: " + str(player.hp) + ", MP Left: " + str(player.mp))
            print()
            for player in self.players:
                t = player.turn(self)
                if t[0] == "F":
                    useplayer(player, t[1], self)
                elif t[0] == "R":
                    if t[1]:
                        self.enemies=[]
                else:
                    #item
                    pass
                print()
            for enemy in self.enemies:
                if enemy.hp <= 0:
                    for p in self.players:
                        print("Awarded", p.name, enemy.xp, "XP")
                        p.xp += enemy.xp
                    self.enemies.remove(enemy)
            if self.enemies == []:
                print("You won!")
                input()
                clear()
                return True
            input()
            clear()


class Player:
    def __init__(self, signature):
        #maxhp=base.maxhp+lvl*4?
        self.hp = 0
        self.cls = 0
        self.name = ""
        self.lvl = 0
        self.xp = 0
        self.mp = 0
        self.buffs = []
        self.items = []
        self.signature = signature
        self.shielded = False
        self.load(signature)
        
    def info(self):
        itemslist=[]
        for i in self.items:
            itemslist.append(i.name)
        print("\n"+self.name+"\n"+"-"*len(self.name)+"\nHP:",self.hp,"/",str(self.base.maxhp)+"\nMP:",self.mp,"/",str(self.base.maxmp)+"\nItems:\n\t"+"\n\t".join(itemslist)+"\nXP: "+str(self.xp))

    @property
    def bosskeys(self): #for backwards compatibility
        return sum(i.idn==1 for i in self.items)
    @property
    def keys(self): #for backwards compatibility
        return sum(i.idn==0 for i in self.items)

    def load(self, ln):
        with open("save/savedata.csv") as f:
            lineno = 0
            for line in f:
                if ln == lineno:
                    self.parsedata(line.rstrip("\n"))
                    return
                lineno += 1
        self.base = PlayerBase(int(input("class: ")))
        self.parsedata(self.base.cls + "," + str(self.base.maxhp) + ",3," +
                       input("name: ") + ",0,0,0")

    def parsedata(self, dat):
        spldat = dat.split(",")
        self.cls = spldat[0]
        self.hp = int(spldat[1])
        self.lvl = int(spldat[2])
        self.name = spldat[3]
        self.xp = int(spldat[4])
        self.items = spldat[7].split(":")
        index = 0
        for i in self.items:
            self.items[index] = Item(int(i))
            index += 1
        self.base = PlayerBase(getattr(PlayerEnum, self.cls))
        self.mp = self.base.maxmp

    def save(self):
        w = True
        with open("save/savedata.csv", "r+") as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                if i.split(",")[3].rstrip("\n") != self.name:
                    f.write(i)
                else:
                    w = False
                    tmpitems = []
                    for i in self.items:
                        tmpitems.append(str(i.idn))
                    f.write(self.cls + "," + str(self.hp) + "," +
                            str(self.lvl) + "," + self.name + "," +
                            str(self.xp) + "," + str(self.keys) + "," +
                            str(self.bosskeys) + "," + ":".join(tmpitems) +
                            "\n")
            f.truncate()
            if w:
                f.write(self.cls + "," + str(self.hp) + "," + str(self.lvl) +
                        "," + self.name + "," + str(self.xp) + "," +
                        str(self.keys) + "," + str(self.bosskeys) + "\n")

    def turn(self, encounter):
        t = input("Fight, Item or Run? (f,i,r)").lower()
        #run
        if t == "r":
            import random
            if sum([isinstance(a,Boss) for a in encounter.enemies]):#contains boss?
                print("You can't run from a boss!")
                return self.turn(encounter)
            if random.randint(1,4) == 1:
                print("You successfully escaped the encounter!")
                return ["R",True]
            else:
                print("You tried to run, but it failed!")
                return ["R",False]

        if t == "no u":
            print("\033[1;33muno reverse card activate!\033[0m")
            return self.turn(encounter)
        if t == "uwu":
            print("\033[1;33mowo\033[0m")
            return self.turn(encounter)
        if t == "f":
            return self.fight(encounter)
        elif t == "i":
            return self.itemslist(encounter)
        else:
            print("Invalid")
            return self.turn(encounter)

    def fight(self, encounter):
        print(self.name + ", choose an attack:")
        for i in range(self.lvl):
            try:
                print("  " + str(i + 1) + ".) ", self.base.attacks[i].name,"- uses",
                      str(self.base.attacks[i].mp)+"mp")
            except:
                pass
        in1 = 999999999
        while in1 >= self.lvl:
            try:
                todo = input("do: ")
                if todo=="back":
                    return self.turn(encounter)
                else:
                    in1 = int(todo) - 1
                    if self.base.attacks[in1].mp > self.mp:
                        print("Not enough mp")
                        in1=999999999
            except (ValueError, IndexError):
                in1 = 999999999
        in2 = in1
        if not self.base.attacks[in2].glo:
            print("Choose a target:")
            if self.base.attacks[in2].beneficial:
                for i in range(len(encounter.players)):
                    print(
                        "  " + str(i + 1) + ".) " + encounter.players[i].name,
                        encounter.players[i].hp)
                in1 = 99999
                while not in1 < len(encounter.players):
                    try:
                        in1 = int(input("do: ")) - 1
                    except:
                        in1 = 99999
                return ["F",[self.base.attacks[in2], encounter.players[in1]]]
            else:
                for i in range(len(encounter.enemies)):
                    print(
                        "  " + str(i + 1) + ".) " + encounter.enemies[i].name,
                        encounter.enemies[i].hp)
                in1 = 99999
                while not in1 < len(encounter.enemies):
                    try:
                        in1 = int(input("do: ")) - 1
                    except:
                        in1 = 99999
                return ["F",[self.base.attacks[in2], encounter.enemies[in1]]]
        else:
            return ["F",[self.base.attacks[in2], "ALL"]]

    def itemslist(self, enc):
        if self.items == []:
            print("No items")
            x = self.turn(enc)
            return x
        else:
            for i, item in enumerate(self.items):
                print("  " + str(i + 1) + ".)", str(item))
            while True:
                todo = input("do:")
                if todo=="back":
                    return self.turn(enc)
                try:
                    #self.buffs.append(self.items[int(todo) - 1].effect)
                    if self.items[int(todo)-1].action(self):

                        for buff in self.buffs:
                            buff.inflict(self)
                        if self.hp > self.base.maxhp:
                            self.hp = self.base.maxhp
                        print(self.items[int(todo)-1].actionmessage)
                        break
                except:
                    print("Invalid")
            del self.items[int(todo) - 1]
        return ["I"]

    def damage(self, d):
        from random import randint
        if self.shielded and randint(0, 3) == 0:
            print(self.name, "shielded!")
            print("No damage was dealt!\n")
            return True
        else:
            self.hp -= d
        if self.hp <= 0:
            return False
        else:
            return True


class PlayerEnum:
    Warrior = 0
    Cleric = 1
    Mage = 2
    Barbarian = 3


class PlayerBase:
    def __init__(self, idn):
        types = ["Warrior", "Cleric", "Mage", "Barbarian"]
        hps = [30, 26, 28, 24]
        mps = [8, 12, 20, 8]
        self.attacks = self._attacks(idn)
        self.maxhp = hps[idn]
        self.cls = types[idn]
        self.maxmp = mps[idn]

    def _attacks(self, idn):
        if idn == 0:
            return [
                Attack("Swing", 5, 0, 0),
                Attack("Slice", 6, 3, 0, recoil=3),
                Attack("Burn cut", 8, 2, 0, mp=5),
                Attack("Mega burn", 10, 4, 0, mp=7)
            ]
        elif idn == 1:
            return [
                Attack("Hit", 6, 2, 0),
                Attack("Burn", 4, 2, 0, glo=True),
                Attack("Heal", -10, 2, 0, True, mp=5),
                Attack("Mega heal", -12, 2, 0, True, True, mp=15)
            ]
        elif idn == 2:
            return [
                Attack("Hit", 4, 0, 0),
                Attack("Shock", 7, 1, 0, mp=4),
                Attack(
                    "Life force",
                    -7,
                    1,
                    0,
                    beneficial=True,
                    glo=True,
                    mp=6,
                    recoil=3),
                Attack("Blast burn", 9, 2, 0, glo=True, mp=8)
            ]
        elif idn == 3:
            return [
                Attack("Hit", 6, 0, 0),
                Attack("Slash", 7, 2, 0),
                Attack("Double edged sword", 9, 3, 0, mp=3, recoil=3),
                Attack("Long swipe", 9, 0, 0, glo=True)
            ]
