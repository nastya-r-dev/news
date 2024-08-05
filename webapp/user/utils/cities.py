import requests
from bs4 import BeautifulSoup
from pprint import pp

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except (requests.RequestException, ValueError):
        print('error!')
        return False


def get_russian_cities():
    html = get_html('https://ru.wikipedia.org/wiki/Список_городов_России')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find('tbody').find_all('tr')
        rows.pop(0)
        cities = []
        for row in rows:
            cities.append(row.find_all('a')[1].text)
    return cities


if __name__ == '__main__':
    get_russian_cities()
