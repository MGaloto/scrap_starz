

# 1. Importar librerias

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json
from pprint import pprint
import re
from collections import Counter
import pandas as pd
import plotly.io as pio
import plotly.express as px
from datetime import date


# 2. Configuracion del driver y ejecutamos la URL

options = webdriver.ChromeOptions()
options.add_argument("--incognito") # Abrimos Chrome utilizando Incognito.
driver = webdriver.Chrome('chromedriver.exe', options = options)
url = 'https://www.starz.com/ar/es/view-all/blocks/1523514'
driver.get(url)
sleep(4) # Le doy tiempo a la pagina para luego capturar el html
html = driver.execute_script('return document.documentElement.outerHTML')
dom = BS(html, 'html.parser')

# Guardo en la variable links todo el html que contiene los url para recorrer en el for cada uno de los href

links = dom.find_all('starz-content-item')




#%%


# 3. Web Scraping de Series, temporadas y capitulos.

# Se crean dos listas, diccionario contiene los datos de las series y temporadas la metadata con detalles de cada capitulo

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
    
    sleep(4)
    
    """
    A continuacion se capturan todos los datos que van a guardarse en la lista diccionario creada antes del for.
    
    Nombre de la Serie, episodios, tipo, año, sinopsis, reparto, dirigida y escrita por.
    
    """
    
    nombre = dom.find('div', attrs = {'class': "series-title d-flex flex-column justify-content-end"}).text
    datos = dom.find('ul', attrs = {'class': "meta-list text-uppercase"})
    episodios = datos.find('li').find_next_sibling("li").find('span').get_text()
    tipo = datos.find('li').find_next_sibling("li").find_next_sibling("li").get_text()
    año = datos.find('li').find_next_sibling("li").find_next_sibling("li").find_next_sibling("li").get_text()
    sinopsis = dom.find('p', lines='3').text
    
    
    url_datos = 'https://www.starz.com/ar/es' + dom.find('a', attrs = {'class': "d-none d-sm-block episode-link"})['href']
    driver.get(url_datos)
    
    sleep(4)
    
    html = driver.execute_script('return document.documentElement.outerHTML')
    dom = BS(html, 'html.parser')
    
    sleep(4)
    
    
    """
    Se crean excepciones ya que no aparecen algunos textos dentro de las etiquetas html.
    
    """
    
    try:
        reparto = (' ,'.join(dom.find('div', attrs = {'class': "credit-group actors col-lg-8"}).stripped_strings)).strip('Reparto ,')
    except:
        reparto = 'None'

    try: 
        dirigida_por = (' ,'.join(dom.find('div', attrs = {'class': "credit-group directors"}).stripped_strings)).strip('Dirigida por ,')
    except:
        dirigida_por = 'None'
        
    
    try:
        escrita_por = (' ,'.join(dom.find('div', attrs = {'class': "credit-group writers"}).stripped_strings)).strip('Escrita por ,')
    except:
        escrita_por = 'None'
            

    caracteristicas = {'Nombre': nombre, 'Año': año, 'Episodios':episodios, 'Tipo':tipo, 'Link':url_final, 'Sinopsis' : sinopsis,
                       'Escrita' : escrita_por, 'Dirigida' : dirigida_por, 'Reparto' : reparto}
    diccionario.append(caracteristicas) 
    
    """
    A continuacion se ingresa a cada una de las series para capturar mas datos que hagan mas rico nuestro analisis.
    
    Hacemos el mismo ejercicio anterior, capturamos todos los href y ejecutamos la url de cada una de las series para capturar 
    datos de cada una de las temporadas y capitulos. En el primer for entramos en la temprada y en el que continua en cada uno de los capitulos.
    Cuando finaliza una temporada vuelve a iterar solo si max_temporadas es > 1.
    
    
    
    """
    
    
    ver_temporadas = dom.find('div', attrs = {'class': "season-selector d-flex"})
    
    ver_temporada = ver_temporadas.find('div', attrs = {'class': "season-number d-inline-block text-center active"}).text
        
    max_temporadas = len(ver_temporadas.text.strip('Temporada'))
    
    driver.execute_script("window.history.go(-1)")
    
    # len_temporadas nos sirve para que en cada iteracion podamos actualizar la longitud de la lista creada antes de iniciar el ciclo 
    
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
            
            # Con las expresiones regulares capturamos el numero de la temporada desde la url
            
            temporada = re.search('season-(.+?)/', url_temporadas).group(1)
            
            minutos = capitulo.find('li').find_next_sibling("li").text
            descripcion = capitulo.find('p', lines='2').text
            
            capitulos = {'Numero': temporada, 'Capitulo': nombre_capitulo, 'Duracion' : minutos, 'Descripcion' : descripcion}
            
            temporadas.append(capitulos)
            
    # len_temporadas_final nos sirve para que en cada iteracion podamos actualizar la longitud final de la lista creada antes de iniciar el ciclo 
        
    len_temporadas_final = len(temporadas)
    
    # Le agregamos a la lista diccionario las temporadas totales a cada una de las series
    
    diccionario[count - 1]['Temporadas'] = list(temporadas[len_temporadas:len_temporadas_final])

    

    print('\n------------------------------------------------------------')    
    print('La serie: ',nombre, 'contiene: ',temporada, 'temporada/s.')
    print('Ok los datos de la serie: ',nombre)
    print('\nRestan: ', len(links) - count, ' Series')        
    print('------------------------------------------------------------')   
    

    
print('Fin del Scrap de Series')


      
    
#%%

# Guardar archivo Json

with open('series.json', 'w') as archivo_json_series:
    json.dump(diccionario, archivo_json_series, ensure_ascii=False, indent = 2)




#%%

# Consulta de los generos de todas las series y grafico de barras:
    

series = json.load(open('series.json'))
 

generos = []
for i in range(len(series)):
    generos.append(series[i]['Tipo'])
    print(series[i]['Tipo'])
 

generos_result = dict(Counter(generos))


df = pd.DataFrame({'Genero':list(generos_result.keys()), 'Cantidad' : list(generos_result.values()) })

# Grafico de barras 

pio.renderers.default='svg'

bar_graph = px.bar(df, y='Cantidad', x='Genero', text='Cantidad', title = 'Cantidad de Series por Genero, datos del {}'.format(date.today()))
bar_graph.update_traces( textposition='outside')
bar_graph.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',barmode='stack', xaxis={'categoryorder':'total descending'})
bar_graph.show()




#%%

# Conexion a MongoDB

from pymongo import MongoClient

cliente = MongoClient('mongodb://localhost:27017')


bd = cliente['starz']
coleccion = bd['series']


#%%

# Insertar datos a MongoDB

coleccion.insert_many(diccionario)

print('datos subidos')



#%%

# Consultar serie The Great desde MongoDB

consulta = coleccion.find({'Nombre': 'The Great'})

for serie in consulta:
    pprint(serie)
    


#%%

# 4. Web Scraping de Peliculas.

# Utilizamos la apertura de toda la ventana completa para capturar todos los link_peliculas

options = Options()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome('chromedriver.exe', options = options)
url_peliculas = 'https://www.starz.com/ar/es/view-all/blocks/1523534'
driver.get(url_peliculas)

sleep(3)

html = driver.execute_script('return document.documentElement.outerHTML')
dom = BS(html, 'html.parser')

link_peliculas = dom.find_all('article', attrs = {'class': "content-link"})




#%%

# Se crea la lista peliculas para guardar cada una de las iteraciones

peliculas = []

count = 0

for i in range(len(link_peliculas)):
    link_pelicula = link_peliculas[i].find('a')['href']
    link_pelicula_final = 'https://www.starz.com' + link_pelicula
    driver.get(link_pelicula_final)
    sleep(3)
    html = driver.execute_script('return document.documentElement.outerHTML')
    dom = BS(html, 'html.parser')
    sleep(6)
    
    count += 1
    
    nombre = dom.find('h1', attrs = {'class': "movie-title"}).text.strip('Ver ')
    
    duracion = dom.find('ul', attrs = {'class': "meta-list text-uppercase"}).find("li").find_next_sibling("li").text
    
    tipo = dom.find('ul', attrs = {'class': "meta-list text-uppercase"}).find("li").find_next_sibling("li").find_next_sibling("li").text
    
    año = dom.find('ul', attrs = {'class': "meta-list text-uppercase"}).find("li").find_next_sibling("li").find_next_sibling("li").find_next_sibling("li").text
    
    descripcion = dom.find('p', attrs = {'lines': "3"}).text

    try:
        reparto = (' ,'.join(dom.find('div', attrs = {'class': "credit-group actors col-lg-8"}).stripped_strings)).strip('Reparto ,')
    except:
        reparto = 'None'

    try: 
        dirigida_por = (' ,'.join(dom.find('div', attrs = {'class': "credit-group directors"}).stripped_strings)).strip('Dirigida por ,')
    except:
        dirigida_por = 'None'
        
    try:
        escrita_por = (' ,'.join(dom.find('div', attrs = {'class': "credit-group writers"}).stripped_strings)).strip('Escrita por ,')
    except:
        escrita_por = 'None'
    
    caracteristicas_peliculas = {'Numero': count, 'Nombre': nombre, 'Duracion' : duracion, 
                                 'Tipo': tipo, 'Año': año, 'Descripcion' : descripcion, 'Link' : link_pelicula_final,
                                 'Reparto': reparto, 'Dirigida' : dirigida_por, 'Escrita' : escrita_por}
    peliculas.append(caracteristicas_peliculas) 
    
    print('\n------------------------------------------------------------')    
    print('La pelicula: ',nombre, ', Genero: ',tipo, ', Duracion:', duracion)
    print('Ok los datos de la pelicula: ',nombre)
    print('\nRestan: ', len(link_peliculas) - count, ' Peliculas')        
    print('------------------------------------------------------------') 
        



print('Fin del Scrap de Peliculas')


    
#%%

# Guardar archivo de las peliculas Json

with open('peliculas.json', 'w', encoding='utf-8') as archivo_json_peliculas:
    json.dump(peliculas, archivo_json_peliculas, ensure_ascii = False, indent = 2)



#%%

# Insertamos las peliculas en MongoDB

coleccion_peliculas = bd['peliculas']

coleccion_peliculas.insert_many(peliculas)

print('Datos subidos')


#%%


# Consulta de los generos de todas las peliculas y grafico de barras:
    

pelis = json.load(open('peliculas.json', encoding='utf-8'))
 

generos_pelis = []
for i in range(len(pelis)):
    generos_pelis.append(pelis[i]['Tipo'])
    print(pelis[i]['Tipo'])
 

generos_result_pelis = dict(Counter(generos_pelis))


df_pelis = pd.DataFrame({'Genero':list(generos_result_pelis.keys()), 'Cantidad' : list(generos_result_pelis.values()) })

# Grafico de barras 

pio.renderers.default='svg'

bar_graph = px.bar(df_pelis, y='Cantidad', x='Genero', text='Cantidad', title = 'Cantidad de Peliculas por Genero, datos del {}'.format(date.today()))
bar_graph.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',barmode='stack', xaxis={'categoryorder':'total descending'})
bar_graph.show()




#%%



















