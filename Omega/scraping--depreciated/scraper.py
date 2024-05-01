import http, time, re, requests, json
import pandas as pd
from urllib.error import HTTPError
from datetime import date
from urllib.request import urlopen, ProxyHandler, build_opener, install_opener
from bs4 import BeautifulSoup
from threading import Thread
from colorama import Fore, Back, Style

# Initialization variables/processes
startTime = time.time()
operatingTime = 0
totalDataLines = 359
didNotPull = []
dnpReason = []
counter = 0
webhook = 'https://discord.com/api/webhooks/1088214057192017931/n_ab-k5EHxniyqtxus9uNd9Jav9uqfogrJ-Fj9BHVU50kOMholn6wSc25U4obxFtlvGZ'


def main():
    startUI()

def crawlTable(url):
    global didNotPull, dnpReason, counter

    try:
        response = requests.get(
            url,
            proxies = {
                "http": "http://1c06b7f733094af89fc31306284ca446:@proxy.crawlera.com:8011/",
                "https": "http://1c06b7f733094af89fc31306284ca446:@proxy.crawlera.com:8011/",
            },
            verify = 'zyte-proxy-ca.crt'
        )
        html = response.text
        soup = BeautifulSoup(html, features='lxml')
        headers = [th.getText() for th in soup.findAll('tr')[0].findAll('th')]

        rows = soup.findAll('tr', class_ = lambda table_rows: table_rows != 'thead')
        player_stats = [[td.getText() for td in rows[i].findAll('td')]
                        for i in range(len(rows))]
        player_stats = player_stats[31:]

        headers = ['rk', 'date', 'age', 'tm', 'home/away', 'opp', 'w/l', 'gs', 'mp', 'fg', 'fga', 'fg%', '3p', '3pa', '3p%', 'ft', 'fta', 'ft%', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'gmsc', '+/-']
        df = pd.DataFrame(player_stats, columns=headers)

        playerID = parseID(url)

        file_path = 'output/' + str(playerID)+'.csv'  
        
        df.to_csv(file_path, index=False)
        counter = counter+1
        if ((counter % 25) == 0):
            print(Fore.WHITE+"["+Fore.MAGENTA+"*"+Fore.WHITE+"]"+Style.RESET_ALL+' ' + str(counter) + '/' + str(totalDataLines))

    except (IndexError):
        print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' Error Parsing Link: ' + url)
        didNotPull.append(url)
        dnpReason.append('IndexError')

    except HTTPError:
        print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' HTTP Error 429: Too many requests -- Stopping operation')
        print(Fore.WHITE+"["+Fore.MAGENTA+"*"+Fore.WHITE+"]"+Style.RESET_ALL+' If error persists, change proxies')
        exit(0)

    except PermissionError:
        print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' Permission Error: Skipping ' + playerID + '.csv')
        didNotPull.append(str(playerID) + '.csv')
        dnpReason.append('PermissionError')

    except http.client.IncompleteRead:
        print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' Incomplete Read: Skipping ' + url)
        didNotPull.append(url)
        dnpReason.append('IncompleteRead')

    except http.client.RemoteDisconnected:
        print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' Client Disconnected: Skipping ' + url)
        didNotPull.append(url)
        dnpReason.append('RemoteDisconnect')
    except ValueError:
        print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' Value Error: Skipping ' + url)
        didNotPull.append(url)
        dnpReason.append('ValueError')

def initProxies():
    proxyDict = ProxyHandler({'http': '1c06b7f733094af89fc31306284ca446:@proxy.crawlera.com:8011','https': '1c06b7f733094af89fc31306284ca446:@proxy.crawlera.com:8011'})
    opener = build_opener(proxyDict)
    install_opener(opener)

def parseID(url):
    pattern = r"/./(\w+)/gamelog"
    matches = re.findall(pattern, url)

    if len(matches) > 0:
        return matches[0]
    else:
        return "unknownID"

def splitList(input):
    x = 0
    for i in input:
        x = x+1
    n = x//2
    firstHalf = input[:n]
    secondHalf = input[n:]

    return firstHalf,secondHalf

def parsePlayers():
    html = urlopen("https://zerscrpt.cfd/sc/NBA_PLAYER_LINKS.txt")
    soup = BeautifulSoup(html, 'html.parser')

    rawData = str(soup.getText)
    data = rawData.split()
    del data[:5]   # removing header data from the table
    data[-1] = (data[-1])[-1]    # removing html junk on last element
    del data[-1]  # see previous comment

    rawList1,rawList2 = splitList(data)

    preList1,preList2 = splitList(rawList1)
    preList3,preList4 = splitList(rawList2)

    list1,list2 = splitList(preList1)
    list3,list4 = splitList(preList2)
    list5,list6 = splitList(preList3)
    list7,list8 = splitList(preList4)

    returnList = [list1,list2,list3,list4,list5,list6,list7,list8]
    return returnList

def target(list):
    for i in list: crawlTable(i)

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

    endUI()


def startUI():
    print()
    print(Fore.WHITE+"["+Fore.MAGENTA+"*"+Fore.WHITE+"]"+Style.RESET_ALL+" To scrape all player data, type `ALL`. Otherwise, specify a player ID, ie `knighna01`\n")
    choice = input(" > ")

    if (choice.lower() == "all"):
        threadFunc()
    else:
        prefix = str(choice[:1])
        crawlTable('http://www.basketball-reference.com/players/' + prefix + '/' + choice + '/gamelog/2023/#pgl_basic')


def endUI():
    global operatingTime, webhook, counter, didNotPull, dnpReason

    counter = counter - len(dnpReason)
    unparsed = ''

    for i in didNotPull:
        unparsed += i + '\n'

    payload = {
    'embeds': [{
        'title': 'Scraping Complete!',
        'description': 'A scraping job was just completed',
        'color': 0x6327a3,
        'fields': [
            {'name': 'Operating Time', 'value': str(round(operatingTime,2)) + ' minutes', 'inline': True},
            {'name': 'Total Count', 'value': str(counter), 'inline': True},
            {'name': 'Unparsed URLs', 'value': unparsed, 'inline': False}
        ],
        'footer': {'text': str(date.today())}
        }]
    }

    requests.post(webhook, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

    print(Fore.WHITE+Back.YELLOW+'~~~~~~~~~~~~~~~~~~~~~~~~~~'+Style.RESET_ALL)
    print('\n'+Fore.WHITE+"["+Fore.GREEN+"+"+Fore.WHITE+"]"+Style.RESET_ALL+' Finished >> Operating Time: ' + str(round(operatingTime,2)) + 'm\n')
    print(Fore.WHITE+Back.YELLOW+'~~~~~~~~~~~~~~~~~~~~~~~~~~'+Style.RESET_ALL)
    print('\n'+str(len(didNotPull)) + ' item(s) did not parse correctly\n')
    
    for i in didNotPull:
        print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' ['+ Fore.YELLOW + dnpReason[didNotPull.index(i)] + Style.RESET_ALL + '] ―― ' + i +'\n')
    
    print(Fore.WHITE+Back.YELLOW+'~~~~~~~~~~~~~~~~~~~~~~~~~~'+Style.RESET_ALL)

if __name__ == '__main__':
    main()