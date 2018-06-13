from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


# Sumary : get a table with all data
#
#
#
def get_html_table():
    req = Request('https://pokemondb.net/pokedex/all',
                  headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    table = soup.table
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        print(row)
