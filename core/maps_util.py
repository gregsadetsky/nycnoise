import requests
import json
from bs4 import BeautifulSoup

def main():
    tv_eye = "https://maps.app.goo.gl/4UtdECEnYra6kJwa8"
    print(f"I love tv eye: {tv_eye}")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    respone = requests.get(tv_eye, headers=headers)
    print(respone.headers)
    print(respone.status_code)
    data = respone.text
    # print(data)
    soup = BeautifulSoup(data, features="lxml")
    print(soup.prettify())

if __name__ == '__main__':
    main()
