import dpkt
import sys


def main():
    if len(sys.argv) != 2:
    	print("Few/extra arguments specified")
    	sys.exit()

    ParsePcap(sys.argv[1])

if __name__ == '__main__':
    main()