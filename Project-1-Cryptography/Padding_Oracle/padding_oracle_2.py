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

    decrypted_text = ""

    for z in range(1,len(cipher_blocks)):
        if z == 1:
            cipher_blocks_dup = cipher_blocks
        else:
            cipher_blocks_dup = cipher_blocks[:-(z-1)]
        prev_block = cipher_blocks[-(z+1)]
        cipher_bytes = bytearray.fromhex(cipher_blocks[-(z+1)])
        decrypted_block = []
        plaintext_block = []

        i = 1
        while i < 17:
            for k in range(1,i):
                cipher_bytes[-k] = i ^ decrypted_block[-k]
            for j in range(0,256):    
                cipher_bytes[-i] = j
                print(cipher_bytes.hex())
        
                cipher_blocks_dup[-2] = cipher_bytes.hex()
                ciphertext = ""
                for ele in cipher_blocks_dup:
                    ciphertext += ele
                if verify_padding(ciphertext) == 1:
                    print(j)
                    break;

            decrypted_block.insert(0,(j ^ i))
            print("decrypted_block: ", decrypted_block)
            plaintext_block.insert(0,(decrypted_block[-i] ^ bytearray.fromhex(prev_block)[-i]))
            print("plaintext: ", plaintext_block)

            if i == 1 and z == 1:
                for l in range((i+1),(plaintext_block[-i]+1)):
                    decrypted_block.insert(0,(bytearray.fromhex(prev_block)[-l] ^ plaintext_block[-i]))
                    plaintext_block.insert(0,plaintext_block[-i])
                i = plaintext_block[-1] + 1
            else:
                i = i+1

        if z == 1:
            unpadded_block = unpad(bytes(plaintext_block))
        else:
            unpadded_block = bytes(plaintext_block)

        decrypted_text = unpadded_block.hex() + decrypted_text 
        print("Block",z,":",unpadded_block.hex())

    print(decrypted_text)
    actual_text = decrypted_text[:-64]
    actual_text_ascii = bytearray.fromhex(actual_text).decode()
    print(actual_text_ascii)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s ORACLE_URL CIPHERTEXT_HEX" % (sys.argv[0]), file=sys.stderr)
        sys.exit(-1)
    oracle_url = sys.argv[1]
    ciphertext = sys.argv[2]

    cipher_blocks = divide_ciphertext(ciphertext)

    decrypt_last_block(cipher_blocks)