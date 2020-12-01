from PUtils import *
from encounter import *
from items import *
from random import randint
from time import sleep


class DoorEnum:
    UNLOCKED = 0
    LOCKED = 1
    WALL = 2
    BOSS = 3


class WallEnum:
    DOOR = ""
    LOCKEDDOOR = "O"
    BOSSDOOR = "#"
    XWALL = "-"
    YWALL = "|"


class Room:
    def __init__(self, x, y, doorStates, enc=None, boss=False, itemid=-1, stairs=False):
        self.north = doorStates[0]
        self.east = doorStates[1]
        self.south = doorStates[2]
        self.west = doorStates[3]
        self.stairs = stairs
        self.encounter = enc
        self.x = x
        self.y = y
        self.boss = boss
        self.itemid = itemid

    def calcDoorCostume(self, cstm, XOrY):
        if cstm == 0:
            return WallEnum.DOOR
        elif cstm == 1:
            return WallEnum.LOCKEDDOOR
        elif cstm == 2:
            return (WallEnum.XWALL if XOrY == "X" else WallEnum.YWALL)
        elif cstm == 3:
            return WallEnum.BOSSDOOR

    def load(self):
        print((WallEnum.XWALL * 10) + self.calcDoorCostume(self.north, "X") +
              (WallEnum.XWALL * 10))
        for i in range(7):
            if i != 3:
                print(WallEnum.YWALL + (" " * 19) + WallEnum.YWALL)
            else:
                print((self.calcDoorCostume(self.west, "Y") + (
                    (" " * 19) if self.itemid == -1 else (
                    (" " * 9) + ItemEnum2.l[self.itemid] + (" " * 9)))) + self.calcDoorCostume(self.east, "Y"))
        print((WallEnum.XWALL * 10) + self.calcDoorCostume(self.south, "X") +
              (WallEnum.XWALL * 10))
        if self.encounter != None:
            if not self.encounter.fire():
                raise Exception("YOU LOSE")
            self.encounter = None

    def checkroom(self, dir1):
        return getattr(self, dir1) != 2

    def merge(self, room):
        for i in range(4):
            if room.doorStates[i] < self.doorStates[i]:
                self.doorstates[i] = room.doorStates[i]


def flipdir(x):
    if x == "north":
        return "south"
    elif x == "south":
        return "north"
    elif x == "west":
        return "east"
    elif x == "east":
        return "west"
    else:
        return "no u"  # uno reverse card activate!


def checkvalid(rm, dir1, plr, mapdict1):
    if dir1 in ["north", "east", "south", "west"]:
        doorno = getattr(rm, dir1)
    elif dir1 == "pickup" and mapdict1[rm.x, rm.y].itemid != -1:
        return True
    elif dir1 == "help":
        return True
    else:
        return False
    if doorno == 0:
        return True
    elif doorno == 1 and plr.keys > 0:
        plr.keys -= 1
        setattr(rm, dir1, 0)
        xc = 0
        yc = 0
        if dir1 == "north":
            yc = -1
        elif dir1 == "east":
            xc = 1
        elif dir1 == "south":
            yc = 1
        elif dir1 == "west":
            xc = -1
        #error catch
        setattr(mapdict1[(rm.x + xc, rm.y + yc)], flipdir(dir1), 0)
        return True
    elif doorno == 3 and plr.bosskeys > 0:
        plr.bosskeys -= 1
        setattr(rm, dir1, 0)
        xc = 0
        yc = 0
        if dir1 == "north":
            yc = -1
        elif dir1 == "east":
            xc = 1
        elif dir1 == "south":
            yc = 1
        elif dir1 == "west":
            xc = -1
        #error catch
        setattr(mapdict1[(rm.x + xc, rm.y + yc)], flipdir(dir1), 0)
        return True
    return False


def assigndoors(mapdict1):
    for xy, doors in mapdict1.items():
        x = xy[0]
        y = xy[1]
        try:
            mapdict1[(x, y - 1)]
        except:
            mapdict1[x, y][0] = 2
        try:
            if mapdict1[(x + 1, y)][4]:
                raise
        except:
            mapdict1[x, y][1] = 2
        try:
            mapdict1[(x, y + 1)]
        except:
            mapdict1[x, y][2] = 2
        try:
            if mapdict1[(x - 1, y)][4]:
                raise
        except:
            mapdict1[x, y][3] = 2


class Dungeon:
    def __init__(self, rooms, plrs):
        self.mapdict = {-1:{},0:{},1:{}}
        self.maplayer = 0
        for rm in rooms:
            self.mapdict[self.maplayer][(rm.x, rm.y)] = rm
        self.loc = [3, 3]
        self.plr = plrs[0]
        self.plrs = plrs
        self.load()

    def prompt(self):
        dir1 = input(">").lower()
        valid = checkvalid((self.mapdict[self.maplayer][self.loc[0], self.loc[1]]), dir1, self.plr, self.mapdict[self.maplayer])
        while not ((dir1 in ["north","east","south","west","pickup","help"]) and valid):
            dir1 = input("Invalid. >").lower()
            valid = checkvalid((self.mapdict[self.maplayer][self.loc[0], self.loc[1]]), dir1, self.plr, self.mapdict[self.maplayer])
        if dir1 == "north" and self.loc[1] > 0:
            self.loc[1] = self.loc[1] - 1
        if dir1 == "east":
            self.loc[0] = self.loc[0] + 1
        if dir1 == "south":
            self.loc[1] = self.loc[1] + 1
        if dir1 == "west" and self.loc[0] > 0:
            self.loc[0] = self.loc[0] - 1
        if dir1 == "pickup":
            itemno = (self.mapdict[self.maplayer][self.loc[0], self.loc[1]]).itemid
            if itemno == 0:
                self.plr.keys += 1
            elif itemno == 1:
                self.plr.bosskeys += 1
            elif 1 < itemno < 6:
                self.plr.items.append(Item(itemno - 2))
            self.mapdict[self.maplayer][self.loc[0], self.loc[1]].itemid = -1
        if dir1 == "help":
            self.help()
        self.load()

    #def write(self):
    #   with open("save/dungeon.dmap", "w") as save:
    #        for k, v in self.mapdict.items():
    #            doorstates = [
    #                str(v.north),
    #                str(v.east),
    #                str(v.south),
    #                str(v.west)
    #            ]
    #            save.write(",".join([str(i) for i in k]) + ":" +
    #                      ",".join(doorstates) + ";" + str(v.itemid))
    #           save.write("\n")

    #def read(self):
    #    with open("save/dungeon.dmap", "r") as save:
    #        self.mapdict = {}
    #        for x in save:
    #            k, v = x.split(":")
    #            self.mapdict[tuple([int(i) for i in k.split(",")])] = Room(
    #                int(k.split(",")[0]),
    #                int(k.split(",")[1]),
    #                [int(i) for i in v.split(";")[0].split(",")],
    #                itemid=int(v.split(";")[1]))
    #    for k, v in self.mapdict.items():
    #        v.encounter = create_encounter(self.plrs)

    def load(self):
        clear()
        print("Keys:", self.plr.keys)
        print("Boss keys:", self.plr.bosskeys)
        print("Type help if stuck")
        self.mapdict[self.maplayer][self.loc[0], self.loc[1]].load()
        render_minimap(self.loc, self.mapdict[self.maplayer], 10, 10)

    @staticmethod
    def assortenc():
        pass

    @staticmethod
    def help():
        clear()
        with open("helpdocument.txt") as f:
            print("".join(f.readlines()))
        input()
        pass


def render_minimap(loc, mapdict, rx, ry):
    #import collections
    #ordermapdict=collections.OrderedDict(sorted(d.items()))
    for y in range(ry):
        for x in range(rx):
            try:
                mapdict[x, y]
                if loc == [x, y]:
                    print("O", end=" ")
                elif mapdict[x, y].boss:
                    print("#", end=" ")
                else:
                    print("+", end=" ")
            except:
                print(" ", end=" ")
        print()


def create_encounter(plrs):
    return ((Encounter(plrs, [Enemy(randint(0, 1)),
                              Enemy(randint(0, 1))][:randint(1, 2)]))
            if randint(0, 5) == 0 else None)


def genrooms(dict1, plrs):
    assigndoors(dict1)
    ret = []
    for i in dict1.keys():
        r_itemid = -1
        if randint(0, 4) == 0: # for testing  
            r_itemid = randint(2,5)
        ret.append(
            Room(i[0], i[1], dict1[(i[0], i[1])][:4], create_encounter(plrs),
                 dict1[(i[0], i[1])][4], r_itemid))
    return ret
