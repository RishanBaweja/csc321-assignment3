from Crypto.Util import number
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from random import randint
from os import urandom
from math import ceil, gcd
from operator import xor

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
print("bob_s_value_:",M)

ciphertext = pow(M, e, n)
print(f"public_key_s: {ciphertext}")

plaintext = pow(ciphertext,d,n)
print(f"Decrypted_s_: {plaintext}")

print('')

nd_modn = pow(n, d, n)

print(f"Message Mallory modifies: {nd_modn}")

# k = SHA256.new(M).digest()[:16]
k = SHA256.new(nd_modn).digest()[:16]
iv = urandom(16)
mes = b'Hi Bob!'

enc = bytes(map(xor, mes, iv))

new_cipher = AES.new(k, AES.MODE_CBC, iv)
padded = new_cipher.encrypt(pad(enc, 16))

new_cipher = AES.new(k, AES.MODE_CBC, iv)

decrypted = unpad(new_cipher.decrypt(padded), 16)
plain = bytes(map(xor, decrypted, iv))

print(f"Received decrypted text: {plain}")
