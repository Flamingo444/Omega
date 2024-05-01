import csv,os,time,ftplib,requests,json
from datetime import date

webDir = ''

def sendWebhook(numFiles):
    webhook = 'https://discord.com/api/webhooks/1088214057192017931/n_ab-k5EHxniyqtxus9uNd9Jav9uqfogrJ-Fj9BHVU50kOMholn6wSc25U4obxFtlvGZ'
    payload = {
    'embeds': [{
        'title': 'Bulk Data Update',
        'description': 'A bulk player data update was just made',
        'color': 0x402fd6,
        'fields': [
            {'name': 'Files Pushed', 'value': str(numFiles), 'inline': True},
            {'name': 'Upload Directory', 'value': str(webDir), 'inline': True},
        ],
        'footer': {'text': str(date.today())}
        }]
    }

    requests.post(webhook, data=json.dumps(payload), headers={'Content-Type': 'application/json'})


def ftpUpload():
    global webDir

    counter = 0

    FTP_HOST = 'ftp.zerscrpt.cfd'
    FTP_USER = 'omega@zerscrpt.cfd'
    FTP_PASS = 'h8H6$Wk3pdC3'

    localFolder = 'converted'
    remoteFolder = '11csv'

    webDir = 'public_html/' + remoteFolder

    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)

    ftp.cwd('public_html')
    ftp.cwd(remoteFolder)

    for fileName in os.listdir(localFolder):
        localFilePath = os.path.join(localFolder, fileName)
        with open(localFilePath, 'rb') as f:
            ftp.storbinary(f'STOR {fileName}', f)
        print(f'uploaded {fileName}')
        counter += 1

    ftp.quit()

    sendWebhook(counter)
    print('Files uploaded successfully')


startTime = time.time()
originalCSV = 'output'
newDestination = 'converted'
os.makedirs(newDestination, exist_ok=True)

for filename in os.listdir(originalCSV):
    if filename.endswith('.csv'):
        inputPath = os.path.join(originalCSV, filename)
        outputPath = os.path.join(newDestination, os.path.splitext(filename)[0] + '.txt')

        with open(inputPath, 'r') as csv_file:
            reader = csv.reader(csv_file)
            with open(outputPath, 'w') as txt_file:
                writer = csv.writer(txt_file, delimiter=',')
                for row in reader:
                    writer.writerow(row)

print(f'\n\ndone :: operating time - {str(round(time.time()-startTime,2))}s')

continuePrompt = str(input('\n\n Push new files to zerScrpt? [Y/n]: ') or 'y')
continuePrompt.lower()

if continuePrompt == 'y':
    ftpUpload()
else:
    exit(0)