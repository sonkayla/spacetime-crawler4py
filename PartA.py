import sys

# The tokenize function has a runtime complexity of O(n) where n is the character length of the text file. 
# This is because we are iterating through each character once, checking if it is alphanumeric and adding it to our string if it is.
# If it is not an alphanumeric character, we concatenate all the characters before that as a token, adding it to our tokens list.
def tokenize(text):

    lowercase_text = text.lower()

    tokens = [""]

    for i in lowercase_text:
        if ord('a') <= ord(i) <= ord('z') or ord('0') <= ord(i) <= ord('9'):
            tokens[-1] += i
        elif tokens[-1] != "":
            tokens.append('')
            
    return tokens

# The runtime complexity for computWordFrequnecies(tokens) function is O(n) where n is the number of tokens.
# This is because we are iterating through each token once, increasing the count if the token exists in the dictionary.
# Otherwise, we add the token to the dictionary with a value of 1.
def computeWordFrequencies(tokens):
    frequencies =  {}

    for t in tokens:
        if t in frequencies:
            frequencies[t] += 1
        else:
            frequencies[t] = 1
    
    return frequencies