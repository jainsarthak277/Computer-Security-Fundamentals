#!/usr/bin/python3

import requests
import sys
from Crypto.Cipher import AES

oracle_url = ""

def unpad(message):
    n = message[-1]
    if n < 1 or n > AES.block_size or message[-n:] != bytes([n]*n):
        print('invalid_padding')
    return message[:-n]

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
    second_last = cipher_blocks[-2]
    cipher_bytes = bytearray.fromhex(cipher_blocks[-2])
    decrypted_block = []
    plaintext_block = []
    verify_plaintext = []

    i = 1
    while i < 17:
        for k in range(1,i):
            cipher_bytes[-k] = i ^ decrypted_block[-k]
        for j in range(1,256):    
            cipher_bytes[-i] = j
            print(cipher_bytes.hex())
            #cipher_hex = hex(int(cipher_bytes.hex(),16) ^ int(last_block,16))
            
            cipher_blocks_dup[-2] = cipher_bytes.hex()
            ciphertext = ""
            for ele in cipher_blocks_dup:
                ciphertext += ele
            if verify_padding(ciphertext) == 1:
                print(cipher_blocks_dup[-2])
                print(j)
                break;

        decrypted_block.insert(0,(j ^ i))
        print("decrypted_block: ", decrypted_block)
        plaintext_block.insert(0,(decrypted_block[-i] ^ bytearray.fromhex(second_last)[-i]))
        print("plaintext: ", plaintext_block)

        if i == 1:
            for l in range((i+1),(plaintext_block[-i]+1)):
                decrypted_block.insert(0,(bytearray.fromhex(second_last)[-l] ^ plaintext_block[-i]))
                plaintext_block.insert(0,plaintext_block[-i])
            i = plaintext_block[-1] + 1
        else:
            i = i+1

    #Verify if plaintext xor decrypted block is equal to previous cipher block
    for a,b in zip(bytes(plaintext_block),bytes(decrypted_block)):
        verify_plaintext.append(a^b)

    if verify_plaintext == list(bytearray.fromhex(second_last)):
        print("success")

    print(decrypted_block)
    #unpadded_block = unpad(bytes(plaintext_block).hex())
    print(bytes(plaintext_block).hex())
    #print(bytearray.fromhex(unpadded_block).decode())


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