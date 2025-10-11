from random import randint
from Crypto.Hash import SHA256

def calculation(q, alpha):
    x = randint(0,q-1)
    y = pow(alpha,x,q)
    return (x,y)

def Alice(q, xA, yB):
    s = pow(yB,xA,q)
    k = SHA256.new(s.to_bytes((s.bit_length() + 7) // 8, byteorder='big'))
    return k.digest().hex()

def Bob(q, xB, yA):
    s = pow(yA,xB,q)
    k = SHA256.new(s.to_bytes((s.bit_length() + 7) // 8, byteorder='big'))
    return k.digest().hex()

q, alpha = 37, 5
a = calculation(q, alpha) #(xA, xB)
b = calculation(q, alpha) #(yA, yB)


print(f"{Alice(q, a[0], b[1])}\n\n\n")
print(Bob(q, b[0], a[1]))
