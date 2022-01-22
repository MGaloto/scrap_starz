# 1. Importar librerias

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from time import sleep
import requests
import csv
import json
from pprint import pprint

# 2. Ejecutar URL

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome('chromedriver.exe', options = options)
url = 'https://www.starz.com/ar/es/view-all/blocks/1523514'
driver.get(url)


"""
Obtener todas las películas y series
Obtener la metadata de cada contenido: título, año, sinopsis, link, duración (solo para movies)
Guardar la información obtenida en una base de datos, en archivo .json o .csv automáticamente
PLUS: Episodios de cada serie
PLUS: Metadata de los episodios
PLUS: Si es posible obtener mas información/metadata por cada contenido
PLUS: Identificar modelo de negocio
"""


#%%

html = driver.execute_script('return document.documentElement.outerHTML')
dom = BS(html, 'html.parser')

# series = dom.find_all('h3', class_='title text-center on-hover')

# nombre_serie = []

links = dom.find_all('starz-content-item')


# Creamos una tabla con las variables

tabla_series = [['Nombre','Año', 'Episodios', 'Tipo', 'Link', 'Sinopsis']]


#%%



count = 0
for i in range(len(links)):
    count += 1 
    url = links[i].article.div.a['href']
    url_final = 'https://www.starz.com' + url
    driver.get(url_final)
    sleep(3)
    html = driver.execute_script('return document.documentElement.outerHTML')
    dom = BS(html, 'html.parser')
    sleep(6)
    name = dom.find('div', attrs = {'class': "series-title d-flex flex-column justify-content-end"})
    sleep(1)
    nombre = name.text
    datos = dom.find('ul', attrs = {'class': "meta-list text-uppercase"})
    sleep(3)
    episodios = datos.find('li').find_next_sibling("li").find('span').get_text()
    tipo = datos.find('li').find_next_sibling("li").find_next_sibling("li").get_text()
    año = datos.find('li').find_next_sibling("li").find_next_sibling("li").find_next_sibling("li").get_text()
    sinopsis = dom.find('p', lines='3').text
    variables = [nombre, año, episodios, tipo, url_final, sinopsis]
    tabla_series.append(variables)
    print(count, '----',nombre,  '--', sinopsis)
    break
    
    
    
    
#%%
    

with open('series.csv', 'w', newline = '') as series:
     salida = csv.writer(series)
     salida.writerows(tabla_series)




#%%
    
# Prueba

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome('chromedriver.exe', options = options)
url = 'https://www.starz.com/ar/es/series/express/63120'
driver.get(url)

html = driver.execute_script('return document.documentElement.outerHTML')

dom = BS(html, 'html.parser')



#%%

# Conexion a MongoDB

from pymongo import MongoClient

cliente = MongoClient('mongodb://localhost:27017')


bd = cliente['starz']
coleccion = bd['series']


#%%








#%%

# Insertar datos

coleccion.insert_many('poner la lista que contiene el diccionario')
print('datos subidos')


#%%






















