def snip(b, n):
    return int(bin(b).strip('0b')[(n-1):],base=2)

class EncryptDecrypt:
    @staticmethod
    def encrypt(data,h=169053490):
        out = ""
        for c in data:
            out+=str(-(snip(h,8))*(~ord(c))*(h>>8)).zfill(20)
        return out.rstrip("")
    def decrypt(data,h=169053490):
        out = ""
        for c in [data[i:i+20] for i in range(0, len(data), 20)]:
            out+=chr(int((~int(c))/(snip(h,8))/-(h>>8))-1)
        return out