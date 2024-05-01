import requests
from lxml import html
import time
from colorama import Fore, Style
import http.client



url_file = "https://zerscrpt.cfd/sc/NBA_PLAYER_LINKS.txt"
response = requests.get(url_file)
if response.status_code != 200:
    print(f"Error: {response.status_code} - Could not retrieve URL file")
    exit()

urls = response.content.decode().splitlines()

with open("playerIDS.txt", "w", encoding="utf-8") as f:
    counter = 0
    didNotPull = []
    dnpReason = []
    for url in urls:
        counter += 1
        try:
            response = requests.get(url)
            if response.status_code == 429:
                print(Fore.RED + "Error: 429 - Rate limit exceeded." + Style.RESET_ALL)
                input("Change VPN location and press any key to continue...")
                response = requests.get(url)
                if response.status_code != 200:
                    print(f"Error: {response.status_code} - Could not retrieve {url}")
                    continue
            elif response.status_code != 200:
                print(f"Error: {response.status_code} - Could not retrieve {url}")
                continue
            tree = html.fromstring(response.content)

            player_id = url.split('/')[-3]
            target_data_list = tree.xpath('//*[@id="meta"]/div[2]/h1/span/text()')
            if len(target_data_list) > 0:
                target_data = target_data_list[0]
                if '2022-23 Game Log' in target_data:
                    output = f"{player_id}: {target_data.replace('2022-23 Game Log', '')}\n"
                else:
                    output = f"{player_id}: {target_data}\n"
                f.write(output)
                print(output.strip())
            else:
                print(f"Error: Could not find target data for {url}")

        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.NewConnectionError):
                print("Error: VPN Connection Failed - Retrying in 10 seconds...")
                time.sleep(10)
                continue
            print(f"Error: {e}")
            continue

        except IndexError:
            print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' Error Parsing Link: ' + url)
            didNotPull.append(url)
            dnpReason.append('IndexError')

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' HTTP Error 429: Too many requests -- Stopping operation')
                print(Fore.WHITE+"["+Fore.MAGENTA+"*"+Fore.WHITE+"]"+Style.RESET_ALL+' If error persists, change proxies')
                exit(0)
            else:
                print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' HTTP Error: ' + str(e.response.status_code))
                didNotPull.append(url)
                dnpReason.append('HTTPError')

        except PermissionError:
            print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' Permission Error: Skipping ' + player_id + '.csv')
            didNotPull.append(str(player_id) + '.csv')
            dnpReason.append('PermissionError')

        except http.client.IncompleteRead:
            print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' Incomplete Read: Skipping ' + url)
            didNotPull.append(url)
            dnpReason.append('IncompleteRead')

        except http.client.RemoteDisconnected:
            print(Fore.WHITE+"["+Fore.RED+"!"+Fore.WHITE+"]"+Style.RESET_ALL+' Remote Disconnected: Skipping ' + url)
           
