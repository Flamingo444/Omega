### Library for all OMEGA projects, using module-based structure for readability and adds room for further improvement

import requests, http, json, ftplib, os, csv
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
from urllib.error import HTTPError
from colorama import Fore, Back, Style

didNotPull = []
dnpReason = []
counter = 0
webDir = ''


def crawlNBATable(url, playerID):
    global didNotPull, dnpReason, counter

    os.makedirs('output', exist_ok=True)

    try:
        response = requests.get(
            url,
            proxies={
                "http": "http://1c06b7f733094af89fc31306284ca446:@proxy.crawlera.com:8011/",
                "https": "http://1c06b7f733094af89fc31306284ca446:@proxy.crawlera.com:8011/",
            },
            verify='zyte-proxy-ca.crt'
        )
        html = response.text
        soup = BeautifulSoup(html, features='lxml')
        headers = [th.getText() for th in soup.findAll('tr')[0].findAll('th')]

        rows = soup.findAll('tr', class_=lambda table_rows: table_rows != 'thead')
        player_stats = [[td.getText() for td in rows[i].findAll('td')]
                        for i in range(len(rows))]
        player_stats = player_stats[31:]

        headers = ['rk', 'date', 'age', 'tm', 'home/away', 'opp', 'w/l', 'gs', 'mp', 'fg', 'fga', 'fg%', '3p', '3pa',
                   '3p%', 'ft', 'fta', 'ft%', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'gmsc',
                   '+/-']
        df = pd.DataFrame(player_stats, columns=headers)

        file_path = 'output/' + str(playerID) + '.csv'

        df.to_csv(file_path, index=False)
        counter = counter + 1
        if ((counter % 25) == 0):
            print(Fore.WHITE + "[" + Fore.MAGENTA + "*" + Fore.WHITE + "]" + Style.RESET_ALL + ' ' + str(
                counter) + ' links parsed')

    except (IndexError):
        print(Fore.WHITE + "[" + Fore.RED + "!" + Fore.WHITE + "]" + Style.RESET_ALL + ' Error Parsing Link: ' + url)
        didNotPull.append(url)
        dnpReason.append('IndexError')

    except HTTPError:
        print(
            Fore.WHITE + "[" + Fore.RED + "!" + Fore.WHITE + "]" + Style.RESET_ALL + ' HTTP Error 429: Too many requests -- Stopping operation')
        print(
            Fore.WHITE + "[" + Fore.MAGENTA + "*" + Fore.WHITE + "]" + Style.RESET_ALL + ' If error persists, change proxies')
        exit(0)

    except PermissionError:
        print(
            Fore.WHITE + "[" + Fore.RED + "!" + Fore.WHITE + "]" + Style.RESET_ALL + ' Permission Error: Skipping ' + playerID + '.csv')
        didNotPull.append(str(playerID) + '.csv')
        dnpReason.append('PermissionError')

    except http.client.IncompleteRead:
        print(
            Fore.WHITE + "[" + Fore.RED + "!" + Fore.WHITE + "]" + Style.RESET_ALL + ' Incomplete Read: Skipping ' + url)
        didNotPull.append(url)
        dnpReason.append('IncompleteRead')

    except http.client.RemoteDisconnected:
        print(
            Fore.WHITE + "[" + Fore.RED + "!" + Fore.WHITE + "]" + Style.RESET_ALL + ' Client Disconnected: Skipping ' + url)
        didNotPull.append(url)
        dnpReason.append('RemoteDisconnect')
    except ValueError:
        print(Fore.WHITE + "[" + Fore.RED + "!" + Fore.WHITE + "]" + Style.RESET_ALL + ' Value Error: Skipping ' + url)
        didNotPull.append(url)
        dnpReason.append('ValueError')


def splitList(inputList):
    x = 0
    for i in inputList:
        x = x + 1
    n = x // 2
    firstHalf = inputList[:n]
    secondHalf = inputList[n:]

    return firstHalf, secondHalf


def sendWebhook(title, description, color, field1, value1, field2, value2):
    webhook = 'https://discord.com/api/webhooks/1088214057192017931/n_ab-k5EHxniyqtxus9uNd9Jav9uqfogrJ-Fj9BHVU50kOMholn6wSc25U4obxFtlvGZ'
    payload = {
        'embeds': [{
            'title': str(title),
            'description': str(description),
            'color': color,
            'fields': [
                {'name': str(field1), 'value': str(value1), 'inline': True},
                {'name': str(field2), 'value': str(value2), 'inline': True},
            ],
            'footer': {'text': str(date.today())}
        }]
    }

    requests.post(webhook, data=json.dumps(payload), headers={'Content-Type': 'application/json'})


def ftpUpload(source, destination):
    global webDir

    counter = 0

    FTP_HOST = 'ftp.zerscrpt.cfd'
    FTP_USER = 'omega@zerscrpt.cfd'
    FTP_PASS = 'h8H6$Wk3pdC3'

    localFolder = source
    remoteFolder = destination

    webDir = 'public_html/omega' + remoteFolder

    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)

    ftp.cwd('public_html')
    ftp.cwd(remoteFolder)

    fileCount = 0

    for file in os.scandir(localFolder):
        if file.is_file(): fileCount += 1

    for fileName in os.listdir(localFolder):
        if counter % 25 == 0: print(f'{counter}/{str(fileCount)}')
        localFilePath = os.path.join(localFolder, fileName)
        with open(localFilePath, 'rb') as f:
            ftp.storbinary(f'STOR {fileName}', f)
        counter += 1

    ftp.quit()

    print('Files uploaded successfully')


def csvToTXT(source, output):
    sourceDIR = source
    outputDIR = output
    os.makedirs(outputDIR, exist_ok=True)

    for filename in os.listdir(sourceDIR):
        if filename.endswith('.csv'):
            inputPath = os.path.join(sourceDIR, filename)
            outputPath = os.path.join(outputDIR, os.path.splitext(filename)[0] + '.txt')

            with open(inputPath, 'r') as csvFile:
                reader = csv.reader(csvFile)
                with open(outputPath, 'w') as txtFile:
                    writer = csv.writer(txtFile, delimiter=',')
                    for row in reader:
                        writer.writerow(row)

    print('Files converted')


def compareCSV(csv1, csv2):
    # filename = 'changes.csv'
    with open(csv1, 'r', encoding='utf-8') as file1, open(csv2, 'r', encoding='utf-8') as file2:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)
        # changes = []

        file2_rows = list(reader2)

        diff = False
        for row1 in reader1:
            if row1 not in file2_rows:
                print(f'New projection added: {row1}\n')
                #print(type(row1))
                #print(row1[0])
                # changes += str(row1)
                diff = True
        if not diff:
            print("\n\nNo changes have occurred.\n")


"""
        if os.path.isfile(filename):
            os.remove(filename)
            df_changes = pd.DataFrame(changes)
            df_changes.to_csv(changes, index=False)
        else:
            df_changes = pd.DataFrame(changes)
            df_changes.to_csv(changes, index=False)
"""


# WORK IN PROGRESS
def compareBumps(csv1, csv2):

    with open(csv1, 'r', encoding='utf-8') as file1, open(csv2, 'r', encoding='utf-8') as file2:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)

        file2_rows = list(reader2)

        diff = False
        for row1 in reader1:
            if row1 not in file2_rows:
                diff = True
                for row2 in file2_rows:
                    if row2[0] == row1[0] and row2[2] == row1[2]:
                        print(f"Change detected for {row1[0]}:\n    Stat: {row1[2]}\n    Change: {row2[1]} -> {row1[1]}\n")
        if not diff:
            print("No changes have occurred.\n")


