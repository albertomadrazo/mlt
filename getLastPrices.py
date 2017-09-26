import urllib.request
from bs4 import BeautifulSoup

# quote_page = 'https://www.bloomberg.com/quote/SPX:IND'

# page = urllib.request.urlopen(quote_page)

# soup = BeautifulSoup(page, 'html.parser')

# # print(soup)

# name_box = soup.find('div', attrs={'class':'price'})

# name = name_box.text

# print(name)


pagina_resultados = 'http://www.pronosticos.gob.mx/Paginas/Melate/historico-melate'
pagina = urllib.request.urlopen(pagina_resultados)
soup = BeautifulSoup(pagina, 'html.parser')

tabla_resultados = soup.find('table', attrs={'id':'MainContent_gvwHistoricosMelate'})

rowan = tabla_resultados.findAll('tr')

sorteos = []

for r in rowan:
    tede = r.findAll('td')
    sorteo = []
    for i, val in enumerate(tede):
        # print(i, val.text)
        sorteo.append(val.text)

    sorteos.append(sorteo)


print(sorteos)
