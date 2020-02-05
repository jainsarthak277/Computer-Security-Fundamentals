#!/usr/bin/python3

import requests
import sys
from Crypto.Cipher import AES

oracle_url = ""

def divide_ciphertext(ciphertext):
    """ Divides ciphertext into blocks of 16 bytes """
    if len(ciphertext) % AES.block_size:
        print("Invalid length")
    else:
        cipher_blocks = []

        for i in range(0,len(ciphertext),AES.block_size*2):
            cipher_blocks.append(ciphertext[i:i+(AES.block_size*2)])

        #print(cipher_blocks)
        return cipher_blocks

def verify_padding(ciphertext):
    """ Verify whether padding is correct """
    r = requests.get("%s?message=%s" % (oracle_url, bytes.fromhex(ciphertext).hex()))
    r.raise_for_status()
    obj = r.json()
    #print(obj)

    if obj['status'] == 'invalid_mac':
        return 1
    else:
        return 0

def decrypt_last_block(cipher_blocks):

    cipher_blocks_dup = cipher_blocks
    last_block = cipher_blocks[-1]
    print(last_block)
    cipher_bytes = bytearray.fromhex(cipher_blocks[-2])
    decrypted_block = []
    plaintext_block = []
    verify_plaintext = []

    for i in range(1,17):
        for k in range(1,i):
            cipher_bytes[-k] = i ^ decrypted_block[-k]
        for j in range(0,256):    
            cipher_bytes[-i] = j
            #print(cipher_bytes.hex())
            #cipher_hex = hex(int(cipher_bytes.hex(),16) ^ int(last_block,16))
            
            cipher_blocks_dup[-2] = cipher_bytes.hex()
            ciphertext = ""
            #print(cipher_blocks_dup)
            for ele in cipher_blocks_dup:
                ciphertext += ele
            #ciphertext.join(cipher_blocks_dup)
            #print(ciphertext)
            if verify_padding(ciphertext) == 1:
                #print(cipher_hex)
                #print(last_block)
                #print(ciphertext)
                print(j)
                break;

        decrypted_block.insert(0,(j ^ i))
        plaintext_block.insert(0,(decrypted_block[-i] ^ bytearray.fromhex(cipher_blocks[-2])[-i]))
        print(plaintext_block)

    #Verify if plaintext xor decrypted block is equal to previous cipher block
    for a,b in zip(bytes(plaintext_block),bytes(decrypted_block)):
        verify_plaintext.append(a^b)

    if verify_plaintext == list(bytearray.fromhex(cipher_blocks[-2])):
        print("success")

    print(decrypted_block)
    print(bytes(plaintext_block).hex())

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s ORACLE_URL CIPHERTEXT_HEX" % (sys.argv[0]), file=sys.stderr)
        sys.exit(-1)
    oracle_url = sys.argv[1]
    ciphertext = sys.argv[2]

    cipher_blocks = divide_ciphertext(ciphertext)

    decrypt_last_block(cipher_blocks)
    #dec_oracle_route()
    # Example check of ciphertext at the oracle URL:
    """
    r = requests.get("%s?message=%s" % (oracle_url, bytes.fromhex(ciphertext).hex()))
    r.raise_for_status()
    obj = r.json()
    print(AES.block_size)
    print(obj)
    """