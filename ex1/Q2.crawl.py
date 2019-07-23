import heapq
import math
import lxml.html
import requests
import urllib.robotparser

URL = "https://en.wikipedia.org/wiki/Elizabeth_II"
maxPages = 50


def crawl(url, xpaths):
    # methods to read, parse and answer questions about the robots.txt
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url("https://en.wikipedia.org/robots.txt")
    rp.read()
    # key words to define if url is in top priority
    top_priority = ["King", "Queen", "I", "I", "II", "III", "V", "IV", "VI", "VII", "VIII"]
    urls = []
    crawledUrls=PrioritySet()
    close_list = []
    next_url = url
    iteration = 1
    crawledUrls.map[next_url] = 1
    while iteration <= maxPages:
        close_list.append(next_url)
        # Sends a GET request
        res = requests.get(next_url)
        # Parse the html
        doc = lxml.html.fromstring(res.content)
        # extract url's of the given url using the xpath list
        for expression in xpaths:
            for t in doc.xpath(expression):
                current_url = t
                # check if wikipidia disallow the url
                if not rp.can_fetch("*", current_url):
                    continue
                if "https://en.wikipedia.org" in current_url or current_url.startswith('/wiki'):
                    if current_url.startswith('/wiki'):
                        current_url = "https://en.wikipedia.org" + current_url
                    #give the highest priority to kings and queens
                    if any(n in current_url for n in top_priority):
                        crawledUrls.add(current_url, 1)
                        #adding 1 to the priority it came from
                    else:
                        pririty=crawledUrls.getPriority(next_url)
                        crawledUrls.add(current_url,pririty+1)
        for current in crawledUrls.set:
            urls.append([next_url, current])
            #check if it's not in the close list
        while True:
            next_url = crawledUrls.pop()
            if not next_url in close_list:
                break
       # print(next_url, crawledUrls.getPriority(next_url))
        iteration += 1
    return urls

class PrioritySet(object):
    def __init__(self):
        self.heap = []
        self.set = set()
        self.map = {}
    #add to the priority with the right order
    def add(self, d, pri):
        #if the URL is new insert it to all the collections
        if not d in self.set:
            heapq.heappush(self.heap, (pri, d))
            self.set.add(d)
            self.map[d] =pri
            # else check if the current priority is bigger than the new one
        else:
            pri2 = self.map[d]
            if pri < pri2:
                self.heap.remove((pri2,d))
                heapq.heappush(self.heap, (pri, d))
                self.map[d]=pri

    #pop from the top of the list
    def pop(self):
        pri, d = heapq.heappop(self.heap)
        self.set.remove(d)
        return d
    # get the priority of the URL
    def getPriority(self,d):
        if len(self.map) == 0:
            return 1
        pri = self.map[d]
        return pri

