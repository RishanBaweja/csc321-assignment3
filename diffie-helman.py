from random import randint
from Crypto.Hash import SHA256
from operator import xor
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from os import urandom


def calculation(q, alpha):
    x = randint(0,q-1)
    y = pow(alpha,x,q)
    return (x,y)

def Alice(q, xA, yB):
    s = pow(yB,xA,q)
    #convert s to bytes
    s_bytes = s.to_bytes((s.bit_length() + 7) // 8, byteorder='big')
    #perform the SHA256 on it. After that digest it into bytes
    k = SHA256.new(s_bytes).digest() 
    # return the first 16 bytes
    return k[:16]

def Bob(q, xB, yA):
    s = pow(yA,xB,q)
    s_bytes = s.to_bytes((s.bit_length() + 7) // 8, byteorder='big')
    #perform the SHA256 on it. After that digest it into bytes
    k = SHA256.new(s_bytes).digest() 
    # return the first 16 bytes
    return k[:16]

q, alpha = 37, 5
a = calculation(q, alpha) #(xA, xB)
b = calculation(q, alpha) #(yA, yB)

aK = Alice(q, a[0], b[1])
bK = Bob(q, b[0], a[1])
#aK = bK

iv = urandom(16)

aMessage = b"Hi Bob"
bMessage = b"Hi Alice"

# XOR data with random bits before going through the cipher
a_data = bytes(map(xor, aMessage, iv))
b_data= bytes(map(xor, bMessage, iv))

# Cipher used with code in instructions
aK_cipher = AES.new(aK, AES.MODE_ECB)
bK_cipher = AES.new(bK, AES.MODE_ECB)

# Encrypt the data and then return it
alice_encrypted_data = aK_cipher.encrypt(pad(a_data,16))
bob_encrypted_data = bK_cipher.encrypt(pad(b_data,16))

alice_decrypted = unpad(aK_cipher.decrypt(bob_encrypted_data), 16)
bob_decrypted = unpad(bK_cipher.decrypt(alice_encrypted_data), 16)

alice_plain = bytes(map(xor, alice_decrypted, iv))
bob_plain = bytes(map(xor, bob_decrypted, iv))

print(f"The message that Alice received from Bob: {alice_plain}")
print(f"The message that Bob received from Alice: {bob_plain}")