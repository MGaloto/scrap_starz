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


links = dom.find_all('starz-content-item')


# Creamos una tabla con las variables

tabla_series = [['Nombre','Año', 'Episodios', 'Tipo', 'Link', 'Sinopsis']]


#%%

diccionario = []

series_temporadas = []


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
    print(count, '----',nombre,  '--', sinopsis)
    caracteristicas = {'Nombre': nombre, 'Año': año, 'Episodios':episodios, 'Tipo':tipo, 'Link':url_final, 'Sinopsis':sinopsis}
    diccionario.append(caracteristicas) 
    break
    
    
            
    

    

#%%


# Prueba Series

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome('chromedriver.exe', options = options)
url = 'https://www.starz.com/ar/es/series/the-borgias/61183'
driver.get(url)

sleep(5)

html = driver.execute_script('return document.documentElement.outerHTML')

dom = BS(html, 'html.parser')




ver_temporadas = dom.find('div', attrs = {'class': "season-selector d-flex"})
ver_temporada = ver_temporadas.find('div', attrs = {'class': "season-number d-inline-block text-center active"}).text



series_temporadas = []

if ver_temporada == '1':
    for i in range(len(ver_temporadas)):
        sleep(1)
        url_temporadas = ver_temporadas.find_all('a')[i]['href']
        url_temporadas_final = 'https://www.starz.com' + url_temporadas
        print(url_temporadas_final)
        driver.get(url_temporadas_final)
        sleep(3)
        html = driver.execute_script('return document.documentElement.outerHTML')
        dom = BS(html, 'html.parser')
        sleep(6)
        temporada = i + 1
        capitulos_div = dom.find_all('div', attrs = {'class': "col-12 col-sm-6 col-lg-9 align-self-center"})  
        for capitulo in capitulos_div:
            nombre_capitulo = capitulo.find('h6', attrs = {'class': "title"}).text
            temporada = temporada
            minutos = capitulo.find('li').find_next_sibling("li").text
            descripcion = capitulo.find('p', lines='2').text
            caracteristicas_temporadas = {'Temporada': temporada, 'Nombre': nombre_capitulo, 'Duracion' : minutos, 'Descripcion' : descripcion}
            series_temporadas.append(caracteristicas_temporadas) 
            

            




#%%

# Conexion a MongoDB

from pymongo import MongoClient

cliente = MongoClient('mongodb://localhost:27017')


bd = cliente['starz']
coleccion = bd['series']


#%%


# Insertar datos

coleccion.insert_many(diccionario)
print('datos subidos')



#%%



















