from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

df = pd.read_csv("movies_data.csv", index_col = [0])
Crew = pd.read_csv("Crew.csv", index_col = [0])
genres = pd.read_csv("genres.csv", index_col = [0])
paises = pd.read_csv("Production_countries.csv")


app = FastAPI()


'''Por defecto dentro de nuestras recomendaciones no vamos a recomendar películas "malas"
por lo que vamos a tomar solo las películas que están por encima de la media en calificación'''
df_recomendado = df.loc[lambda df:(df["vote_average"] > 6)]
df_recomendado.loc[:, "release_year"] = df_recomendado["release_year"].astype(str)
df_recomendado.loc[:, "overview"] = df_recomendado["overview"].str.lower()
df_recomendado = df_recomendado[["id_movie","overview","title","vote_average","vote_count","release_year","genres"]]
df_r = df_recomendado["genres"] + df_recomendado["overview"]

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df_recomendado[df_r])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

@app.get("/idiomas/{Idiomas}")
def obtener_Idiomas(Idiomas:str):
    try:
        cantidad = str(df["original_language"].value_counts()[Idiomas])
        return {"Idioma": Idiomas, "Cantidad": cantidad}
    except:
        return("El Idioma ingresado no se encuentra en la base de datos")

    
@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula:str):
    try:
        pelicula = str.lower(pelicula)
        resultado = df[df["title"].str.lower() == pelicula]
        anio = int(resultado["release_year"].values[0])
        duracion = int(resultado["runtime"].values[0])
        return {'pelicula':pelicula.upper(), 'duracion':duracion, 'anio':anio}
    except:
        return("Película no registrada")
    
@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    pais = str.lower(pais)
    paises["name"] = paises["name"].str.lower()
    cantidad = str(paises["name"].value_counts()[pais])
    return {'pais':pais.upper(), 'cantidad':cantidad}

@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
    Productoras = pd.read_csv("Productoras.csv")
    Productoras = pd.merge(Productoras, df, on = "id_movie")
    mascara = Productoras["name"] == productora
    revenue = Productoras[mascara]["revenue"].sum()
    cantidad = str(Productoras["name"].value_counts()[productora])
    return {'productora':productora, 'revenue_total': revenue,'cantidad':cantidad}

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    Crew = pd.merge(Crew, df, on = "id_movie")
    mask = (Crew["name"] == nombre_director)
    Crew_n = Crew[mask]
    retorno_total = Crew_n["revenue"].sum()
    peliculas = Crew_n["title"].to_list()
    anio = Crew_n["release_year"].to_list()
    return_mov = Crew_n["return"].to_list()
    budget = Crew_n["budget"].to_list()
    revenue = Crew_n["revenue"].to_list()
    return {'director':nombre_director, 'retorno_total_director':retorno_total, 
    'peliculas':peliculas, 'anio':anio, 'retorno_pelicula':return_mov, 
    'budget_pelicula (USD)':budget, 'revenue_pelicula (USD)':revenue}

@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    Saga = pd.read_csv("Saga.csv")
    franquicia = str.lower(franquicia)
    resultado = Saga[Saga["name"].str.lower() == franquicia]
    cantidad = len(resultado)
    resultado = pd.merge(resultado, df, on = "id_movie")
    ganancia_total = resultado["revenue"].sum()
    ganancia_promedio = ganancia_total / cantidad
    return {'franquicia':franquicia, 'cantidad':cantidad, 'ganancia_total':ganancia_total, 'ganancia_promedio':ganancia_promedio}

@app.get('/recomendacion/{titulo}')
def busqueda(titulo:str):
    titulo = str.lower(titulo)
    idx = df_recomendado[df_recomendado["title"].str.lower() == titulo].index.to_list()[0]
    puntaje_coseno = enumerate(cosine_sim[idx])
    puntaje_coseno = sorted(puntaje_coseno, key = lambda x: x[1], reverse = True)    
    puntaje_coseno = puntaje_coseno[1:5]
    cos_indices = [i[0] for i in puntaje_coseno]
    resultado = df_recomendado["title"].iloc[cos_indices]
    return {'lista recomendada': resultado}
