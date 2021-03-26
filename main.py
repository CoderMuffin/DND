class PrintEnum:
    STDSTREAM=0
    DISCORDSTREAM=1

PRINTSTREAM = PrintEnum.DISCORDSTREAM

def __print_override(*abcd):
    import builtins
    if PRINTSTREAM==0:
        builtins.print(*abcd)
    else:
        pass

#print = __print_override




from encounter import *
from save_encrypt import EncryptDecrypt
'''a = EncryptDecrypt.encrypt("BEAN")
print(a)
print(EncryptDecrypt.decrypt(a))
exit()'''
from maps import *
from time import sleep
from PUtils import *
import keep_alive
e1 = Enemy(EnemyEnum.UNDEAD)
e2 = Enemy(EnemyEnum.UNDEAD)
p1 = Player(0)
#p2=Player(1)
p1.save()
#p2.save()
#enc=Encounter([p1],[e1,e2])
#enc.fire()
keep_alive.keep_alive()
try:
    x = Dungeon(genrooms(generate_random_path(3, 3, 4, 5), [p1]), [p1])
except Exception as e:
    print(
        "An unexpected error occurred. Please rerun the program. We are sorry for any inconvieniences this error message may have caused you.\nError:",
        e)
    raise e

x.mapdict[0][(3, 3)].north = 1
x.mapdict[0][(3, 3)].itemid = 1
x.mapdict[0][(2, 3)].itemid = 4
x.mapdict[0][(4, 3)].itemid = 5
x.mapdict[0][(3, 2)].south = 1
#x.read()
x.mapdict[0][(3, 4)] = Room(
    3, 4, [3, 2, 2, 2], boss=True, enc=Encounter([p1], [Boss(2,"dragonascii.txt")]))
x.load()  # force load the new doors
lost = False
while True:
    print("\n")
    try:
        x.prompt()
    except Exception as e:  #for now
        if "YOU LOSE" in str(e):
            with open("GameOver.txt") as f:
                print("\033[1;31m"+"".join(f.readlines()))
            print()
            lost = True
            break
        else:
            print(
                "An unexpected error occurred. Please rerun the program. We are sorry for any inconvieniences this error message may have caused you.",e)
            raise e

if lost:
    print("Game Over. Your final score was: {0}".format(p1.xp))