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

print('procesando...')

for r in rowan:
    tede = r.findAll('td')
    sorteo = []
    for i, val in enumerate(tede):
        # print(i, val.text)
        sorteo.append(val.text)

    sorteos.append(sorteo)


for s in sorteos:
    if len(s) > 0:
        print('Sorteo {}\tFecha: {}\tNúmeros: {}'.format(*s))
        s[2] = s[2].replace('-', ' ').split(' ')
        for i, num in enumerate(s[2]):
            if num[0] == '0':
                print('$$$$$$$$', num)
                s[2][i] = num[1:]
                print('----->', num)

        print(s[2])
