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

#Sanity check
check = ((d*e) % thetaN)
print("Result:",check)

pU = [e, n]
pR = [d, n]

M = randint(0, n)
print("Plaintext:",p)

ciphertext = pow(M, e, n)
print(f"Ciphertext: {ciphertext}")

plaintext = pow(ciphertext,d,n)
print(f"Plaintext: {plaintext}")
