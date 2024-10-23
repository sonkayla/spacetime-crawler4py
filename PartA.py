import sys

# The tokenize function has a runtime complexity of O(n) where n is the character length of the text file. 
# This is because we are iterating through each character once, checking if it is alphanumeric and adding it to our string if it is.
# If it is not an alphanumeric character, we concatenate all the characters before that as a token, adding it to our tokens list.
def tokenize(TextFilePath):
    try:
        file = open(TextFilePath, "r", encoding='utf-8')

        tokens = []
        currToken = ""

        while True:
            char = file.read(1)
            if not char:
                break

            lowercase_char = char.lower()
            if ord('a') <= ord(lowercase_char) <= ord('z') or ord('0') <= ord(lowercase_char) <= ord('9'):
                currToken += lowercase_char
            else:
                if currToken:
                    tokens.append(currToken)
                    currToken = ""
        
        if currToken:
            tokens.append(currToken)

        file.close()
        
        return tokens
    except Exception as error:
        print(f"Error: {str(error)}")

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

# The runtime complexity for printFrequencies(frequencies) is O(nlogn) where n is the amount of different tokens.
# This is because we use the sorted function to sort the tokens by frequent appearance which has a runtime of O(nlogn).
# We also loop though each token once which is O(n) but O(nlogn) + O(n) is still overall O(nlogn).

# Sorted function usage: First parameter we are iterating through the dictionary, the key is to sort by frequency of tokens,
# and we reverse the order since we want to output most frequent to least frequent.
def printFrequencies(frequencies):
    sortedFreq = sorted(frequencies.items(), key = lambda item: item[1], reverse = True)
    
    for token, freq in sortedFreq:
        print(f"{token}\t{freq}")

# The runtime complexity for the main function is O(nlogn).
# This is because we call all our previous functions: O(n) + O(n) + O(nlogn) = O(nlogn).
if __name__ == "__main__":
    try:
        file = sys.argv[1]

        tokens = tokenize(file)
        frequencies = computeWordFrequencies(tokens)
        printFrequencies(frequencies)
    
    except Exception as error:
        print(f"Error: {str(error)}")