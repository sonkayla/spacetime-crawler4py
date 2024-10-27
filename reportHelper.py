from typing import List
from urllib.parse import urlparse

def printUniquePagesAmt(pageList):
    with open("uniquePages.txt", "w") as f:
        f.write(f"Number of unique pages found: {len(pageList)}\n")
        # sort (netloc) alphabetically
        for url, count in sorted(pageList.items(), key=(lambda pageCount: urlparse(pageCount[0]).netloc.lower())):
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