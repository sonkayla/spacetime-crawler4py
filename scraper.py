import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from PartA import tokenize, computeWordFrequencies
from collections import defaultdict
from simhash import simhash, similarity

from MaxWordCount import MaxWordCount as mwc
from reportHelper import printSubdomains, printUniquePagesAmt, printMaxWordCount

uniquePages = defaultdict(int)
uciSubdomains = defaultdict(int)

simhashList = []

def scraper(url, resp):
    links = extract_next_links(url, resp)

    printUniquePagesAmt(uniquePages)
    printSubdomains(uciSubdomains)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    # ***** IMPLEMENTATION *****
    # case that status is not 200; don't extract
    if resp.status != 200:
        return []
    
    hyperlinks = [] # init hyperlinks to return

    # checking if there's a response and content to parse
    if resp.raw_response and resp.raw_response.content:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        
        parsedText = soup.get_text()
        tokens = tokenize(parsedText) 

        # comparing and tracking max word count of the url that was read
        totalTokens = len(tokens) # counting total tokens which are words
        # print("current maxwordcount:", mwc.MaxWordCount[1])
        # print("total tokens read in this link:", totalTokens)
        if totalTokens > mwc.MaxWordCount[1]:
            mwc.MaxWordCount[0] = url
            mwc.MaxWordCount[1] = totalTokens
            printMaxWordCount(mwc.MaxWordCount[0], mwc.MaxWordCount[1])
        
        # retireving all .uci.edu subdomains (QUESTION 4)
        if ".uci.edu" in urlparse(resp.raw_response.url).netloc:
            uciSubdomains[urlparse(resp.raw_response.url).scheme +
                                "://" + urlparse(resp.raw_response.url).netloc] += 1
            
        # avoid URLs with no text
        if len(parsedText) == 0:
            return hyperlinks

        # exact and near webpage similarity detection using simhash
        simhashVal = simhash(computeWordFrequencies(tokens))
        for i in simhashList:
            if similarity(simhashVal, i) >= 0.82:
                return hyperlinks
        simhashList.append(simhashVal)
        
        # finding all the '<a>' and extracting those as links
        for aTag in soup.find_all('a', href = True):
            href = aTag.get('href')

            # making sure to defragment the URLs, i.e. remove the fragment part.
            if href:
                fullUrl = urljoin(resp.raw_response.url, href)
                defragmentedUrl = fullUrl.split('#')[0]
                uniquePages[defragmentedUrl] += 1 # adding unique page, not including after fragment (QUESTION 1)
                hyperlinks.append(defragmentedUrl)
    
    return hyperlinks

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        # making sure to return only URLs that are within the domains and paths mentioned
        validDomains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu", 
                   ".stat.uci.edu", "today.uci.edu/department/information_computer_sciences"]
        
        if not any(domain in parsed.netloc for domain in validDomains):
            return False
        
        query_params = parse_qs(parsed.query)
        excluded_params = {"C", "do", "tab_files", "tab_details", "image"}

        if any(param in query_params for param in excluded_params):
            return False
    
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|apk|cc|cpp|h|dsp"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()) 

    except TypeError:
        print ("TypeError for ", parsed)
        raise
