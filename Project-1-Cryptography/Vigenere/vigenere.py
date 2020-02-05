#!/usr/bin/python3

import sys
from collections import Counter
from string import ascii_uppercase

#taken from Wikipedia
letter_freqs = {
    'A': 0.08167,
    'B': 0.01492,
    'C': 0.02782,
    'D': 0.04253,
    'E': 0.12702,
    'F': 0.02228,
    'G': 0.02015,
    'H': 0.06094,
    'I': 0.06966,
    'J': 0.00153,
    'K': 0.00772,
    'L': 0.04025,
    'M': 0.02406,
    'N': 0.06749,
    'O': 0.07507,
    'P': 0.01929,
    'Q': 0.00095,
    'R': 0.05987,
    'S': 0.06327,
    'T': 0.09056,
    'U': 0.02758,
    'V': 0.00978,
    'W': 0.02361,
    'X': 0.00150,
    'Y': 0.01974,
    'Z': 0.00074
}

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def pop_var(s):
    """Calculate the population variance of letter frequencies in given string."""
    freqs = Counter(s)
    mean = sum(float(v)/len(s) for v in freqs.values())/len(freqs)  
    return sum((float(freqs[c])/len(s)-mean)**2 for c in freqs)/len(freqs)
    
def keyLength(s):
    """ Using IoC method to determine key lenth - highest IoC value will be the key lenth.
        Input - s - ciphertext """

    mean = {}
    
    """ Loop through all possible key lengths from 2 to 13 """
    for i in range(2,14):
        coset_var = 0;
        
        """ Divide ciphertext into i cosets and determine IoC for each coset """
        for j in range(0,i):
            coset = s[j::i]
            freqs = Counter(coset)
            coset_var += sum(v*(v-1) for v in freqs.values())/(len(coset)*(len(coset)-1))

        """ For each key length, take the mean of IoC for all cosets """
        mean[i] = (coset_var/i)
        #print("Mean assuming length ",i,": ",(coset_var/i))

    key_length = max(mean, key=mean.get) #Determine max IoC
    #print("Estimated key length:",key_length)

    return key_length

def key_detector(length, s):
    """ Determine the key using chi-square method 
        input - length - length of key
                s - ciphertext """

    """ Numbering of alphabets from 1 to 26 and vice versa"""            
    LETTERS = {letter: index for index, letter in enumerate(ascii_uppercase, start=0)}
    NUMBERS = {index: letter for index, letter in enumerate(ascii_uppercase, start=0)}

    key = ""

    for i in range(0,length):
        sum_list = []
        coset = s[i::length] #Divide ciphertext into length number of cosets

        """ Shift each letter of the coset left by one over 26 iterations and determine the chi-square for each  """
        for shift in range(0,26):
            sum = 0
            shifted_coset = ""

            for char in range(0,len(coset)):
                shifted_coset += NUMBERS[(LETTERS[coset[char]] - shift)%26]
            
            freqs = Counter(shifted_coset)

            for j in freqs:
                cipher_letter_freq = float(freqs[j])/len(coset)
                sum += ((cipher_letter_freq - letter_freqs[j])**2)/letter_freqs[j]

            sum_list.append(sum)

        """ Determining the index of min chi-square value. Alphabet corresponding to the index is one of the letters of key """
        min_sum_index = sum_list.index(min(sum_list))
        key += NUMBERS[min_sum_index]
        #print("Key:",key)

    return key

def decrypt(cipher, key):

    LETTERS = {letter: index for index, letter in enumerate(ascii_uppercase, start=0)}
    NUMBERS = {index: letter for index, letter in enumerate(ascii_uppercase, start=0)}
    
    plainText = ""
    for i in range(0,len(cipher)):
        plainText += NUMBERS[(LETTERS[cipher[i]] - LETTERS[key[i%len(key)]])%26]

    print("Decrypted Text:",plainText)
    
        
if __name__ == "__main__":
    # Read ciphertext from stdin
    # Ignore line breaks and spaces, convert to all upper case
    cipher = sys.stdin.read().replace("\n", "").replace(" ", "").upper()

    key = key_detector(keyLength(cipher), cipher)
    print(key)
    #################################################################
    # Your code to determine the key and decrypt the ciphertext here
