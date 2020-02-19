import random
import re
from pymd5 import md5

def get_password():
	""" Brute force raw md5 hash containing "'='" """

	max_num = (2**32)/2 - 1

	while(1):

		try_str = ""

		for i in range(0,3):
			try_str += str(random.randint(0,max_num))

		md5_str = md5(try_str).digest()
		str_found = re.search(b"'='", md5_str)

		if str_found:
			print("Password:",try_str,"; md5:",md5_str)
			break;

if __name__ == "__main__":
	
	get_password()