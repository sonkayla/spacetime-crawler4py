from typing import List
from urllib.parse import urlparse
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from itertools import islice

def printUniquePagesAmt(uniqueList, pages):
    with open("uniquePages.txt", "w") as f:
        f.write(f"Number of pages found: {pages}\n")
        f.write(f"Number of unique pages found: {len(uniqueList)}\n")
        # sort (netloc) alphabetically
        for url, count in sorted(uniqueList.items(), key=(lambda pageCount: urlparse(pageCount[0]).netloc.lower())):
            f.write(f"{url}, {count}\n")

def printSubdomains(pageList):
    with open("subDomains.txt", "w") as f:
        f.write(f"Number of subdomains for .uci.edu pages = {len(pageList)}\n")
        # sort (netloc) alphabetically
        for subdomain, count in sorted(pageList.items(), key=(lambda pageCount: urlparse(pageCount[0]).netloc.lower())):
            f.write(f"{subdomain}, {count}\n")

def printMaxWordCount(url, tokenCount):
    with open("MaxWordCount.txt", "w") as f:
        f.write(f"{url} = {tokenCount}\n")

def printFrequencies(freq):
    sortedFreq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))
    N = 100
    sortedFreq50 = dict(islice(sortedFreq.items(), N))

    with open("tokenFreq.txt", "w") as f:
        f.write("Token List:\n")
        for key, value in sortedFreq50.items():
            f.write(f"{key}, {str(value)}\n")