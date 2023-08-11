# MOVIES DATASET MLOPS

A partir de la base de datos de películas en el presente proyecto se realizaron los siguientes pasos:

### ETL: 
transformación de los datos para que estos sean mas entendibles, digeriblers y fáciles de procesar con mira a realizar un modelo que sea escalable, por ello se generan tablas relacionales de salida.

### Desarollo API: 
Empleando el framework [Fast API](https://fastapi.tiangolo.com/) con la finalidad de tener un sistema de consultas básicas como:
            * Obtener el número de películas en determinado idioma
            * Ingresando una película saber la duración de la misma y el año de lanzamiento
            * Consultar el número de películas producidas en un país que sea ingresado
            * Mirar las ganancias que han tenido las productoras
            * Ingresando el nombre de un director obtener el listado de películas registradas que hayan sido dirigidas por él, con su fecha de lanzamiento, retorno, costo y ganancia.

### EDA (Exploratory Data Analysis):
Realizando un análsis mas a fondo de los datos de salida del EDA explorando algunas relaciones y estadísticas que nos puede arrojar los mismos.

##Archivos de Entrada
Los archivos de entrada del ETL se encuentran en el siguiente enlace: https://drive.google.com/drive/folders/15Bez2dXXsTL9dG8u31B10vcpqMEimKV5

En el presente repositorio asimismo se encuentran dos archivos.

1. PI.ipynb: el cual contiene el ETL y el EDA
2. Main.py: archivo vinculado al deploy donde encontramos las consultas configuradas

## Enlace para acceder al sistema de consulta:
https://consulta-database-de-peliculas.onrender.com/docs
