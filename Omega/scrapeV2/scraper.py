import re, time, sys
from urllib.request import urlopen

from bs4 import BeautifulSoup
import OMEGA
from threading import Thread
from colorama import Fore, Style

startTime = time.time()
operatingTime = 0

def main(param=None):
    if param:
        if param.lower() == "all":
            threadFunc()
        else:
            prefix = str(param[:1])
            OMEGA.crawlNBATable('http://www.basketball-reference.com/players/' + prefix + '/' + param + '/gamelog/2023/#pgl_basic')
    else:
        print(Fore.WHITE+"["+Fore.MAGENTA+"*"+Fore.WHITE+"]"+Style.RESET_ALL+" To scrape all player data, type `ALL`. Otherwise, specify a player ID, ie `knighna01`\n")
        choice = input(" > ")

        if (choice.lower() == "all"):
            threadFunc()
        else:
            prefix = str(choice[:1])
            OMEGA.crawlNBATable('http://www.basketball-reference.com/players/' + prefix + '/' + choice + '/gamelog/2023/#pgl_basic')

def parsePlayers():
    html = urlopen("https://zerscrpt.cfd/omega/nbaPlayerLinks.txt")
    soup = BeautifulSoup(html, 'html.parser')

    rawData = str(soup.getText)
    data = rawData.split()
    del data[:5]   # removing header data from the table
    data[-1] = (data[-1])[-1]    # removing html junk on last element
    del data[-1]  # see previous comment

    rawList1,rawList2 = OMEGA.splitList(data)

    preList1,preList2 = OMEGA.splitList(rawList1)
    preList3,preList4 = OMEGA.splitList(rawList2)

    list1,list2 = OMEGA.splitList(preList1)
    list3,list4 = OMEGA.splitList(preList2)
    list5,list6 = OMEGA.splitList(preList3)
    list7,list8 = OMEGA.splitList(preList4)

    returnList = [list1,list2,list3,list4,list5,list6,list7,list8]
    return returnList

def parseID(url):
    pattern = r"/./(\w+)/gamelog"
    matches = re.findall(pattern, url)

    if len(matches) > 0:
        return matches[0]
    else:
        return "unknownID"

def target(list):
    for i in list: OMEGA.crawlNBATable(i,str(parseID(i)))

def threadFunc():
    global operatingTime
    print(Fore.WHITE+"["+Fore.MAGENTA+"*"+Fore.WHITE+"]"+Style.RESET_ALL+' Starting threads...')

    threadLists = parsePlayers()
    
    activeThreads = []
    for i in range(8):
        activeThreads.append(Thread(target=target(threadLists[i])))

    for i in range(8):
        activeThreads[i].start()

    for i in range(8):
        activeThreads[i].join()

    operatingTime = (time.time() - startTime) / 60

    print(f'Done || Operating Time: {str(round(operatingTime,2))} minutes')

    unparsed = ''

    for i in OMEGA.didNotPull:
        unparsed += i + '\n'

    OMEGA.sendWebhook('Scraping Completed','A scraping job has just completed',0x6327a3,'File Count',OMEGA.counter,'Unparsed URL\'s',unparsed)


if (len(sys.argv) <= 1):
    main()
else:
    main(sys.argv[1])

OMEGA.csvToTXT('output','txt')
OMEGA.ftpUpload('txt','omega/nbaData')
OMEGA.sendWebhook('Player Data Update','Player data was just updated on zerScrpt',0xf2244e,'Files Pushed',OMEGA.counter,'Upload Directory',OMEGA.webDir)