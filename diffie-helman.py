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

#q, alpha = 37, 5

q_hex = """
        B10B8F96 A080E01D DE92DE5E AE5D54EC 52C99FBC FB06A3C6
        9A6A9DCA 52D23B61 6073E286 75A23D18 9838EF1E 2EE652C0
        13ECB4AE A9061123 24975C3C D49B83BF ACCBDD7D 90C4BD70
        98488E9C 219A7372 4EFFD6FA E5644738 FAA31A4F F55BCCC0
        A151AF5F 0DC8B4BD 45BF37DF 365C1A65 E68CFDA7 6D4DA708
        DF1FB2BC 2E4A4371
        """.replace("\n","").replace(" ","")

q = int(q_hex, 16)

alpha_hex = """
A4D1CBD5 C3FD3412 6765A442 EFB99905 F8104DD2 58AC507F
D6406CFF 14266D31 266FEA1E 5C41564B 777E690F 5504F213
160217B4 B01B886A 5E91547F 9E2749F4 D7FBD7D3 B9A92EE1
909D0D22 63F80A76 A6A24C08 7A091F53 1DBF0A01 69B6A28A
D662A4D1 8E73AFA3 2D779D59 18D08BC8 858F4DCE F97C2A24
855E6EEB 22B3B2E5
""".replace("\n","").replace(" ","")

alpha = int(alpha_hex, 16)

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