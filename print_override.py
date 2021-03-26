class PrintEnum:
    STDSTREAM=0
    DISCORDSTREAM=1

PRINTSTREAM = PrintEnum.DISCORDSTREAM

def __print_override(s):
    import builtins
    if PRINTSTREAM==0:
        builtins.print(s)
    else:
        pass

print = __print_override