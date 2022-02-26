import requests
from bs4 import BeautifulSoup
import re
import time

from dublinBusTweeter import tweeter


class busStops:
    def __init__(self, q):
        self.busStops = q
        self.header = makeHeader(q)

    def getBusStops(self):
        return self.busStops

    def getHeader(self):
        return self.header

    def getBusInformation(self):
        return getInformation(self.busStops)

    def getTweets(self):
        return tweeter.splitIntoTweet(self.getHeader(), self.getBusInformation())

    def printTweets(self):
        for tweet in self.getTweets():
            print(tweet)

    def tweet(self):
        for tweet in self.getTweets():
            tweeter.tweet(tweet)


# Removes tags from text
def remove_tags(text):
    # SOURCE https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
    # SOURCE https://stackoverflow.com/questions/1546226/is-there-a-simple-way-to-remove-multiple-spaces-in-a-string
    TAG_RE = re.compile(r'<[^>]+>')
    text = TAG_RE.sub('', str(text))
    text = re.sub('\s+', ' ', text)
    return text.strip(" ")


# Check if Stop exits and has data
def checkStop(stopNumber):
    url = "https://dublinbus.ie/RTPI/Sources-of-Real-Time-Information/?searchtype=view&searchquery=" + stopNumber
    page = requests.get(url)
    html = page.text
    if "Sorry, this stop is not available" in html:
        return False
    else:
        return True


# Gets list of stops from query string
def exactStops(string):
    stops = set()
    for delim in [",", ":", ";", "+", "add", "plus", "and", "&"]:
        string = string.replace(delim, "-")
        string = string.replace(" ", "")
    for stop in string.split("-"):
        stops.add(stop)
    return stops


# Gets Real Time info from Dublin Bus
def getRealTimeInformationResults(stopNumber):
    url = "https://dublinbus.ie/RTPI/Sources-of-Real-Time-Information/?searchtype=view&searchquery=" + stopNumber
    page = requests.get(url)
    html = page.text
    if "Sorry, this stop is not available" in html:
        raise ValueError("Invalid Bus Stop Number")
    soup = BeautifulSoup(html, 'html.parser')
    html = soup.prettify()
    return html


# Gets the table from the page of times
def getTable(html):
    soup = BeautifulSoup(html, "html.parser")
    html = soup.find(id="rtpi-results").prettify()
    return (html)


# Processes Tables to a clearer format
def processTable(html, q):
    # q = Route, Destination, Expected Time
    rows = html.split("</tr>")
    Results = []
    for row in rows:
        html = row + "</tr>"
        soup = BeautifulSoup(html, "html.parser")
        n = 0
        for column in soup.find_all("td"):
            if n == q:
                Results.append(remove_tags(column))
            n += 1
    return Results


# Puts results into sentences
def makeSentences(table):
    routes = processTable(table, 0)
    destinations = processTable(table, 1)
    expectedTimes = processTable(table, 2)
    N = len(routes)
    lines = []
    for n in range(N):
        line = "No. " + routes[n] + " (" + destinations[n] + ") at " + expectedTimes[n]
        line = line.replace("at Due", "now")
        lines.append(line)
    return lines


# Orders sentences so soonest bus is first
def orderSentences(senetences):
    H = int(time.strftime("%H"))
    M = int(time.strftime("%M"))
    times = ["now"]
    sentences = []
    for h in range(24):
        for m in range(60):
            if M + m == 60:
                h += 1
            t = str((H + h) % 24) + ":" + str((M + m) % 60)
            if (M + m) % 60 <= 9:
                t = t.replace(":", ":0")
            times.append(t)
    for t in times:
        for sentence in senetences:
            if " " + t in sentence:
                sentences.append(sentence)
    return (sentences)


# Gets aggregate information from many stops
def getInformation(query):
    stops = exactStops(query)
    combinedTable = ""
    for stop in stops:
        if checkStop(stop):
            html = getRealTimeInformationResults(stop)
        else:
            return (["Not a valid stop number"])
        table = getTable(html)
        combinedTable += table
    sentences = makeSentences(combinedTable)
    sentences = orderSentences(sentences)
    return (sentences)


# Makes header text
def makeHeader(query):
    stops = exactStops(query)
    header = "Stops "
    for stop in stops:
        header += str(stop) + " "
    header = header.strip(" ")
    header = header
    return (str(header))
