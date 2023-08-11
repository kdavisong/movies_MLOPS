from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

app = FastAPI()

movies_dataset = pd.read_csv("movies_data.csv")
Paises = pd.read_csv("Production_countries.csv")

vectorizador = TfidfVectorizer(ngram_range =(1,2))
tfidf = vectorizador.fit_transform(movies_dataset["title"])

@app.get("/idiomas/{Idiomas}")
def obtener_Idiomas(Idiomas:str):
    try:
        cantidad = str(movies_dataset["original_language"].value_counts()[Idiomas])
        return {"Idioma": Idiomas, "Cantidad": cantidad}
    except:
        return("El Idioma ingresado no se encuentra en la base de datos")

    
@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula:str):
    try:
        pelicula = str.lower(pelicula)
        resultado = movies_dataset[movies_dataset["title"].str.lower() == pelicula]
        anio = resultado["release_year"][0]
        duracion = resultado["runtime"][0]
        return {'pelicula':pelicula.upper(), 'duracion':duracion, 'anio':anio}
    except:
        return("Película no registrada")
    
@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    pais = str.lower(pais)
    Paises["name"] = Paises["name"].str.lower()
    cantidad = str(Paises["name"].value_counts()[pais])
    return {'pais':pais.upper(), 'cantidad':cantidad}

@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
    Productoras = pd.read_csv("Productoras.csv")
    Productoras = Productoras["name"].str.replace(" ","_")
    productora = str.replace(" ","_")
    Productoras = pd.merge(Productoras, movies_dataset, on = "id_movie")
    mascara = Productoras["name"] == productora
    revenue = Productoras[mascara]["revenue"].sum()
    cantidad = str(Productoras["name"].value_counts()[productora])
    return {'productora':productora, 'revenue_total': revenue,'cantidad':cantidad}

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    Crew = pd.read_csv("Crew.csv")
    mask = (Crew["job"] == "Director") & (Crew["name"] == nombre_director)
    Crew = Crew[mask]
    Crew = pd.merge(Crew, movies_dataset, on = "id_movie")
    retorno_total = Crew["revenue"].sum()
    peliculas = Crew["title"].to_list()
    anio = Crew["release_year"].to_list()
    return_mov = Crew["return"].to_list()
    budget = Crew["budget"].to_list()
    revenue = Crew["revenue"].to_list()
    return {'director':nombre_director, 'retorno_total_director':retorno_total, 
    'peliculas':peliculas, 'anio':anio, 'retorno_pelicula':return_mov, 
    'budget_pelicula (USD)':budget, 'revenue_pelicula (USD)':revenue}

@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    Saga = pd.read_csv("Saga.csv")
    franquicia = str.lower(franquicia)
    resultado = Saga[Saga["name"].str.lower() == franquicia]
    cantidad = len(resultado)
    resultado = pd.merge(resultado, movies_dataset, on = "id_movie")
    ganancia_total = resultado["revenue"].sum()
    ganancia_promedio = ganancia_total / cantidad
    return {'franquicia':franquicia, 'cantidad':cantidad, 'ganancia_total':ganancia_total, 'ganancia_promedio':ganancia_promedio}

@app.get('/recomendacion/{titulo}')
def busqueda(titulo:str):
    titulo = str.lower(titulo)
    query_v = vectorizador.transform([titulo])
    simil = cosine_similarity(query_v, tfidf).flatten()
    indx = np.argpartition(simil, -3)[-3:]
    resultado = movies_dataset.iloc[indx][::-1]
    resultado = resultado[["original_language","title","release_year"]].values.tolist()
    return {'lista recomendada': resultado}
