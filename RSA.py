from Crypto.Util import number
from random import randint
from os import urandom

#Want variable length
randnum = randint(2,128)
p = number.getPrime(int(randnum))


randnum = randint(2,128)
q = number.getPrime(int(randnum))

n = p*q
e = 65537

print(f"\n\n{p}\n\n")
print(q)