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

    if obj['status'] == 'invalid_padding':
        return 0
    else:
        return 1

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s ORACLE_URL CIPHERTEXT_HEX" % (sys.argv[0]), file=sys.stderr)
        sys.exit(-1)
    oracle_url = sys.argv[1]
    ciphertext = sys.argv[2]

    divide_ciphertext(ciphertext)
    #dec_oracle_route()
    # Example check of ciphertext at the oracle URL:
    """
    r = requests.get("%s?message=%s" % (oracle_url, bytes.fromhex(ciphertext).hex()))
    r.raise_for_status()
    obj = r.json()
    print(AES.block_size)
    print(obj)
    """