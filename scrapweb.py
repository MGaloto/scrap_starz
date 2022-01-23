# 1. Importar librerias

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from time import sleep
import requests
import csv
import json
from pprint import pprint
import re

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



#%%

diccionario = []

temporadas = []


count = 0
for i in range(len(links)):
    count += 1 
    url = links[i].article.div.a['href']
    url_final = 'https://www.starz.com' + url
    driver.get(url_final)
    sleep(4)
    html = driver.execute_script('return document.documentElement.outerHTML')
    dom = BS(html, 'html.parser')
    sleep(2)
    name = dom.find('div', attrs = {'class': "series-title d-flex flex-column justify-content-end"})
    #sleep(2)
    nombre = name.text
    datos = dom.find('ul', attrs = {'class': "meta-list text-uppercase"})
    #sleep(2)
    episodios = datos.find('li').find_next_sibling("li").find('span').get_text()
    tipo = datos.find('li').find_next_sibling("li").find_next_sibling("li").get_text()
    año = datos.find('li').find_next_sibling("li").find_next_sibling("li").find_next_sibling("li").get_text()
    sinopsis = dom.find('p', lines='3').text
    
    caracteristicas = {'Nombre': nombre, 'Año': año, 'Episodios':episodios, 'Tipo':tipo, 'Link':url_final, 'Sinopsis' : sinopsis}
    diccionario.append(caracteristicas) 
    
    ver_temporadas = dom.find('div', attrs = {'class': "season-selector d-flex"})
    
    ver_temporada = ver_temporadas.find('div', attrs = {'class': "season-number d-inline-block text-center active"}).text
        
    max_temporadas = len(ver_temporadas.text.strip('Temporada'))

    print('\nCargando los datos de la serie: ',nombre, '\n')
    len_temporadas = len(temporadas)

    
    for i in range(max_temporadas):
        url_temporadas = ver_temporadas.find_all('a')[i]['href']
        url_temporadas_final = 'https://www.starz.com' + url_temporadas
        driver.get(url_temporadas_final)
        sleep(4)
        html = driver.execute_script('return document.documentElement.outerHTML')
        dom = BS(html, 'html.parser')
        sleep(2)
        capitulos_div = dom.find_all('div', attrs = {'class': "col-12 col-sm-6 col-lg-9 align-self-center"})  
        for capitulo in capitulos_div:
            nombre_capitulo = capitulo.find('h6', attrs = {'class': "title"}).text
            temporada = re.search('season-(.+?)/', url_temporadas).group(1)
            temporada = re.search('season-(.+?)/', url_temporadas).group(1)
            minutos = capitulo.find('li').find_next_sibling("li").text
            descripcion = capitulo.find('p', lines='2').text
            capitulos = {'Numero': temporada, 'Capitulo': nombre_capitulo, 'Duracion' : minutos, 'Descripcion' : descripcion}
            temporadas.append(capitulos)
    len_temporadas_final = len(temporadas)
    diccionario[count - 1]['Temporadas'] = list(temporadas[len_temporadas:len_temporadas_final])

    
    print('\nLa serie: ',nombre, 'contiene: ',temporada, 'temporada/s.\n')        
    print('-------------\n')       
    print('\nOk los datos de la serie: ',nombre)
    print('-------------\n')
    print('\nRestan: ', len(links) - count, ' Series')

    
print('Fin del Scrap de Series')



    
      
    
#%%

# Guardar archivo Json

with open('series.json', 'w') as archivo_json_series:
    json.dump(diccionario, archivo_json_series, ensure_ascii=False, indent = 2)





#%%


# Prueba Series

import re

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome('chromedriver.exe', options = options)
url = 'https://www.starz.com/ar/es/series/little-birds/62168'
driver.get(url)

sleep(5)

html = driver.execute_script('return document.documentElement.outerHTML')

dom = BS(html, 'html.parser')



series_temporadas = []

ver_temporadas = dom.find('div', attrs = {'class': "season-selector d-flex"})
max_temporadas = len(ver_temporadas.text.strip('Temporada'))


for i in range(max_temporadas):
    sleep(1)
    url_temporadas = ver_temporadas.find_all('a')[i]['href']
    url_temporadas_final = 'https://www.starz.com' + url_temporadas
    print(url_temporadas_final)
    driver.get(url_temporadas_final)
    sleep(3)
    html = driver.execute_script('return document.documentElement.outerHTML')
    dom = BS(html, 'html.parser')
    sleep(6)
    temporada = re.search('season-(.+?)/', url_temporadas).group(1)
    capitulos_div = dom.find_all('div', attrs = {'class': "col-12 col-sm-6 col-lg-9 align-self-center"})  
    for capitulo in capitulos_div:
        nombre_capitulo = capitulo.find('h6', attrs = {'class': "title"}).text
        temporada = temporada
        minutos = capitulo.find('li').find_next_sibling("li").text
        descripcion = capitulo.find('p', lines='2').text
        caracteristicas_temporadas = {'Temporada': temporada, 'Nombre': nombre_capitulo, 'Duracion' : minutos, 'Descripcion' : descripcion}
        series_temporadas.append(caracteristicas_temporadas) 

            

            
pprint(series_temporadas)







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



diccionario[0]['Temporadas'] = list(temporadas[1:5])



temporads = []


len(temporads)





#%%









