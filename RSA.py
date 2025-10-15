from Crypto.Util import number
from random import randint
from os import urandom
from math import ceil, gcd

# Want variable length
randnum = randint(2,128)
p = number.getPrime(int(randnum))

randnum = randint(2,128)
q = number.getPrime(int(randnum))

n = p*q
e = 65537

thetaN = (p-1) * (q-1)
d = pow(e,-1,thetaN)

# Sanity check
# check = ((d*e) % thetaN)
# print("Result:",check)

pU = [e, n]
pR = [d, n]

M = randint(0, n)
print("Plaintext:",M)

ciphertext = pow(M, e, n)
print(f"Ciphertxt: {ciphertext}")

plaintext = pow(ciphertext,d,n)
print(f"Decrypted: {plaintext}")

print('')

while True:
    s = randint(2, n-1)
    if gcd(s, n) == 1:
        break

# Mallory modifies ciphertext
modified_c = (ciphertext * pow(s, e, n)) % n

# Alice takes modified ciphertext and decrypts accordingly
modified_m = pow(modified_c, d, n)

# Mallory recovers m by multiplying by s^-1
inversed = pow(s, -1, n)
mal_m = (modified_m * inversed) % n

print(f"Message Mallory decodes: {mal_m}")