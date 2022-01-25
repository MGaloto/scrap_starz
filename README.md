<p align="left">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/200px-Python-logo-notext.svg.png" alt="react" width="25" height="25" />
<img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Selenium_Logo.png" alt="react" width="25" height="25" />
</p>

# Web Scraping starz

El siguiente trabajo consistió en hacer Web Scraping en la pagina de [starz](https://www.starz.com/ar), capturar todas las películas, todas las series con sus temporadas y capítulos y guardar los datos mas relevantes de cada uno en formato <b><span style = "color:#e5f048">.json</span></b> .

Una vez terminado el Web Scraping se guardan los archivos <b><span style = "color:#e5f048">.json</span></b> , se hace un grafico de barras para las peliculas y series para visualizar los generos de cada una y por ultimo se ejecuta un comando para insertar los datos a <b><span style = "color:#58b54c">MongoDB</span></b> .


# Librerias Utilizadas

<ui>

<li>
{BeautifoulSoup}
</li>

<li>
{Selenium}
</li>

<li>
{Pandas}
</li>

<li>
{Plotly}
</li>

</ui>

# Graficos de barras:

Películas:

![.](Imagenes/grafico_barras_peliculas.png)

Series:

![.](Imagenes/grafico_barras_series.png)


# MongoDB:


Películas:

![.](Imagenes/mongo_peliculas.png)

Series:

![.](Imagenes/mongo_series.png)



