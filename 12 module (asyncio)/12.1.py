import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def get_currencies(url, id, currencies, lock):
    response = requests.get(url)
    if response.status_code == 200:
        secret_code()
        soup = BeautifulSoup(response.text, 'html.parser')
        currency = str(soup.find_all('valute')[id])
        with lock:
            if currency not in currencies:
                currencies.append(currency)

if __name__ == '__main__':
    currencies = []
    lock = threading.Lock()
    id = int(input())
    max_threads = 5

    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(get_currencies, url, id, currencies, lock) for url in urls]

    currencies_string = ''.join(currencies)
    print(currencies_string)