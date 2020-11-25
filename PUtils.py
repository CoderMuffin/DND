from os import system, name


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


#fix overfill and enemy
def useenemy(obj, atk, encounter):
    print(obj.name, "used", atk.name + "!")
    dmg = atk.inflict()
    if not atk.glo:
        import random
        if atk.beneficial:
            trgtobj = random.choice(encounter.enemies)
            print(obj.name, "healed", trgtobj.name, "by", abs(dmg))
        else:
            trgtobj = random.choice(encounter.players)
            print(obj.name, "dealt", dmg, "damage to", trgtobj.name)
        if not trgtobj.damage(dmg):
            print(trgtobj.name, "fainted.")
        if trgtobj.hp > trgtobj.base.maxhp:
            trgtobj.hp = trgtobj.base.maxhp
    else:
        if not atk.beneficial:
            for player in encounter.players:
                print(obj.name, "dealt", dmg, "damage to", player.name)
                if not player.damage(dmg):
                    print(player.name, "fainted.")
        else:
            for enemy in encounter.enemies:
                print(obj.name, "healed", enemy.name, "by", abs(dmg))
                if not enemy.damage(dmg):
                    print(player.name, "fainted.")
                if enemy.hp > enemy.base.maxhp:
                    enemy.hp = enemy.base.maxhp
    obj.damage(atk.recoil)


def useplayer(obj, ftargs, encounter):
    print(obj.name, "used", ftargs[0].name + "!")
    dmg = ftargs[0].inflict()
    #mp=a[1]
    #dmg=a[0]
    obj.mp -= ftargs[0].mp
    if ftargs[1] == "ALL":
        for thing in encounter.players if ftargs[
                0].beneficial else encounter.enemies:
            if ftargs[0].beneficial:
                print(obj.name, "healed", thing.name, "by", abs(dmg))
            else:
                print(obj.name, "dealt", dmg, "damage to", thing.name)
            if not thing.damage(dmg):
                print(thing.name, "fainted.")
            if thing.hp > thing.base.maxhp:
                thing.hp = thing.base.maxhp
            dmg = ftargs[0].inflict()
    else:
        trgtobj = ftargs[1]
        if ftargs[0].beneficial:
            print(obj.name, "healed", trgtobj.name, "by", abs(dmg))
        else:
            print(obj.name, "dealt", dmg, "damage to", trgtobj.name)
        if not trgtobj.damage(dmg):
            print(trgtobj.name, "fainted.")
        if trgtobj.hp > trgtobj.base.maxhp:
            trgtobj.hp = trgtobj.base.maxhp
    obj.damage(ftargs[0].recoil)


def pathrand(x, y, r, l):
    from random import randint
    dict1 = {}
    dict1[(x, y)] = [0, 0, 3, 0, False, -1]
    cx = x + 1
    cy = y
    marx = x + r
    mary = y + r
    mirx = x - r
    miry = y - r
    for i in range(l):
        dict1[(cx, cy)] = [0, 0, 0, 0, False, -1]
        attempts = 0
        while attempts < 100:
            attempts += 1
            pcx = cx
            pcy = cy
            dir1 = randint(1, 3)
            if dir1 == 1:
                cx += 1
            elif dir1 == 2:
                cy -= 1
            else:
                cy += 1
            try:
                dict1[(cx, cy)]
                fail = False
            except:
                fail = True
            if marx > cx > mirx and mary > cy > miry and fail:
                break
            else:
                cx = pcx
                cy = pcy
        if attempts >= 100:
            print("Generation warning on iteration", i, "east")
    dict1[(cx, cy)] = [0, 0, 0, 0, False, 0]
    cx = x
    cy = y - 1
    for i in range(l):
        dict1[(cx, cy)] = [0, 0, 0, 0, False, -1]
        attempts = 0
        while attempts < 100:
            attempts += 1
            pcx = cx
            pcy = cy
            dir1 = randint(1, 3)
            if dir1 == 1:
                cx += 1
            elif dir1 == 2:
                cx -= 1
            else:
                cy -= 1
            try:
                dict1[(cx, cy)]
                fail = False
            except:
                fail = True
            if marx > cx > mirx and mary > cy > miry and fail:
                break
            else:
                cx = pcx
                cy = pcy
        if attempts >= 100:
            print("Generation warning on iteration", i, "north")
    dict1[(cx, cy)] = [0, 0, 0, 0, False, 0]
    cx = x - 1
    cy = y
    for i in range(l):
        dict1[(cx, cy)] = [0, 0, 0, 0, False, -1]
        attempts = 0
        while attempts < 100:
            attempts += 1
            pcx = cx
            pcy = cy
            dir1 = randint(1, 3)
            if dir1 == 1:
                cx -= 1
            elif dir1 == 2:
                cy += 1
            else:
                cy -= 1
            try:
                dict1[(cx, cy)]
                fail = False
            except:
                fail = True
            if marx > cx > mirx and mary > cy > miry and fail:
                break
            else:
                cx = pcx
                cy = pcy
        if attempts >= 100:
            print("Generation warning on iteration", i, "west")
    dict1[(cx, cy)] = [0, 0, 0, 0, False, 0]
    dict1[(x, y + 1)] = [3, 0, 0, 0, True, -1]
    return dict1


def flash():
    from time import sleep
    for i in range(5):
        clear()
        print(
            "\033[1;31m################\n################\n################\n################\n################\n################\n################\n\033[1;33m"
        )
        sleep(0.1)
        clear()
        sleep(0.1)
