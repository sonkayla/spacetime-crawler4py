# link references:
# https://www.geeksforgeeks.org/sha-in-python/
# https://docs.python.org/3/library/string.html#formatstrings
# https://stackoverflow.com/questions/77359516/simhash-function-details#:~:text=The%20SimHash%20algorithm%20allows%20the,not%20limited%20to%20text%20documents.

import hashlib

# converting each token into a binary hash representation with SHA-256
def hash(token):
    hex = hashlib.sha256(token.encode()).hexdigest() # hashing token
    binary = bin(int(hex, 16))[2:] # convert hex --> binary
    return "{:0>256}".format(binary) # ensuring 256 bits with padding

# creating 256-bit fingerprint for entire document with weighted summing based on token frequencies
def simhash(freqDict):

    vectorSum = 256 * [0]

    # adding freq if bit is 1 and subtracting if bit is 0
    for i in range(len(vectorSum)):
        for token, freq in freqDict.items():
            
            binary = hash(token)
            
            if binary[i] == "1":
                vectorSum[i] += freq
            elif binary[i] == "0":
                vectorSum[i] -= freq

    # creating the fingerprint by checking sign of each element in vectorSum
    fingerprint = []
    
    for bit in vectorSum:
        if bit > 0:
            fingerprint.append(1)
        else:
            fingerprint.append(0)
    
    return fingerprint

# calculating the similarity between two SimHash fingerprints by computing the proportion of matching bits
def similarity(simhash1, simhash2):
    same = 0
    
    # counting matching bits and calc similarity
    for i in range(len(simhash1)):
        if simhash1[i] == simhash2[i]:
            same += 1
    
    return same / len(simhash1)