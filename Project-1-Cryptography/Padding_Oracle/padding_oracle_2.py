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

        return cipher_blocks

def verify_padding(ciphertext):
    """ Verify whether padding is correct """
    r = requests.get("%s?message=%s" % (oracle_url, bytes.fromhex(ciphertext).hex()))
    r.raise_for_status()
    obj = r.json()

    if obj['status'] == 'invalid_mac':
        return 1
    else:
        return 0

def decrypt_block(cipher_blocks):
    """ Decrypt using padding oracle attack
        input - cipher_blocks - Ciphertext divided into a list with each element 16 bytes   """
    
    decrypted_text = ""

    """ Iterate over all blocks """
    z = 1
    while z < len(cipher_blocks):
        if z == 1:
            cipher_blocks_dup = cipher_blocks
        else:
            cipher_blocks_dup = cipher_blocks[:-(z-1)] #Strip blocks
        prev_block = cipher_blocks[-(z+1)]
        cipher_bytes = bytearray.fromhex(cipher_blocks[-(z+1)])
        decrypted_block = []
        plaintext_block = []

        """ Iterate over all bytes of a block """
        i = 1
        while i < 17:
            for k in range(1,i):
                cipher_bytes[-k] = i ^ decrypted_block[-k] 
            for j in range(0,256): #Iterate over all possibilities for a byte 
                cipher_bytes[-i] = j
        
                cipher_blocks_dup[-2] = cipher_bytes.hex()
                ciphertext = ""
                for ele in cipher_blocks_dup:
                    ciphertext += ele
                if verify_padding(ciphertext) == 1:
                    break;

            decrypted_block.insert(0,(j ^ i))
            plaintext_block.insert(0,(decrypted_block[-i] ^ bytearray.fromhex(prev_block)[-i]))

            """ Once last byte of last block is determined, strip last 2 blocks and dcrypt from 3rd last block """
            if i == 1 and z == 1:
                padding_len = plaintext_block[-1]
                break;
            else:
                i = i+1

        if z == 1:
            z = 3
        else:
            if z == 3: #if decrypting 3rd last block, removing mac bits from resulting plaintext
                plaintext_block = plaintext_block[:-padding_len]

            unpadded_block = bytes(plaintext_block)
            decrypted_text = unpadded_block.hex() + decrypted_text 
            z = z + 1

    actual_text_ascii = bytearray.fromhex(decrypted_text).decode()
    print(actual_text_ascii)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s ORACLE_URL CIPHERTEXT_HEX" % (sys.argv[0]), file=sys.stderr)
        sys.exit(-1)
    oracle_url = sys.argv[1]
    ciphertext = sys.argv[2]

    cipher_blocks = divide_ciphertext(ciphertext)

    decrypt_block(cipher_blocks)