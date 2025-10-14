from Crypto.Util import number
from random import randint
from os import urandom
from math import ceil

#Want variable length
randnum = randint(2,128)
p = number.getPrime(int(randnum))


randnum = randint(2,128)
q = number.getPrime(int(randnum))

n = p*q
e = 65537

thetaN = (p-1) * (q-1)
d = pow(e,-1,thetaN)

res = ((d*e) % thetaN)
print(f"theta N:{thetaN}\n\n")
print(e)
print(d)
print(f"Result: {res}\n\n")