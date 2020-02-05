#!/usr/bin/python3

import requests
import sys
import json
from Crypto.Cipher import AES


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s ORACLE_URL CIPHERTEXT_HEX" % (sys.argv[0]), file=sys.stderr)
        sys.exit(-1)
    oracle_url = sys.argv[1]
    ciphertext = sys.argv[2]

    # Function returning list of strings, each 16 bytes in length
    ciphertext = "a0b9eaf756c37fef687278912dd9cc9676bf125be5a8baedd9a0c3129c1e2c0a4f5e81cad2ea7e88772880f05d148f8ee1435233616932c9f80b118f51c1ba274bac8e7d25b1afc579aed7e66d9ad3f13c160f957f252c5526bda70ea0684921"
    #ciphers = parse_cipher()
    c2 = "4bac8e7d25b1afc579aed7e66d9ad3f1"
    c3 = "3c160f957f252c5526bda70ea0684921"

    for x in range(256):
        c2 = c2[:-2]
        last_byte = "0x{:02x}".format(x)
        c2 += str(last_byte[2:])
        print(c2)

        ciphertext = ciphertext[:-64]
        ciphertext += c2 + c3

    # Example check of ciphertext at the oracle URL:
        r = requests.get("%s?message=%s" % (oracle_url, bytes.fromhex(ciphertext).hex()))
        r.raise_for_status()
        obj = r.json()
        if obj["status"] == "invalid_mac":
            print("Majjani Life")

