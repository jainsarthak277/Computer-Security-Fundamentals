from pymd5 import md5, padding
from urllib.parse import urlparse, urlsplit, quote
import sys

hack_msg = "&command=UnlockSafes"

#url = sys.argv[1]      

url = "https://project1.ecen4133.org/saja3209/lengthextension/api?token=7eabf9e83890b3bc459cc4aba39c1dfc&command=SprinklersPowerOn"
#url = "https://project1.ecen4133.org/saja3209/lengthextension/api?token=2410cd71208e1c17eeff7afe8b86ae04&command=ClockPowerOff&command=NoOp&command=ClockPowerOn"
#print(url)

#Parse String
parsed = urlparse(url)
query = parsed.query.split('&')
token = query[0].split('=')

#Calculate length of original message (+8 for length of secret key)
len_og_msg = 0
count_of_extra = 0
query.pop(0)
for n in query:
    len_og_msg += len(n)
    count_of_extra += 1
len_og_msg += 8 + count_of_extra - 1

#Concatenate all queries for single command
command = ""
for n in query:
    command += n + "&"
command = command[:-1]
print(command)

pad = quote(padding(len_og_msg*8))

#Calculate hash with count bits of new message
bits = (len_og_msg + len(padding(len_og_msg * 8))) * 8
h = md5(state=bytes.fromhex(token[1]), count=bits)
h.update(hack_msg)

#Re-Combine URL
newUrl = '{scheme}://{netloc}{path}?token={token}&{command}{pad}{suffix}'.format(
        scheme = parsed.scheme,
        netloc = parsed.netloc,
        path = parsed.path, 
        token = h.hexdigest(),
        command = command,
        pad = pad, 
        suffix = hack_msg)

parsedUrl = urlparse(newUrl)
print(newUrl)

sys.exit()
