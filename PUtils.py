from os import system, name

def iter_drop_n(data, condition, drop):
    dropped = 0

    for item in data:
        if dropped >= drop:
            yield item
            continue

        if condition(item):
            dropped += 1
            continue

        yield item
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




def flash():
    from time import sleep
    for i in range(5):
        clear()
        print(
            "\033[1;31m################\n################\n################\n###\033[0mono\033[1;31m#\033[0mcombat\033[1;31m###\n################\n################\n################\n\033[0m"
        )
        sleep(0.2)
        clear()
        sleep(0.2)
