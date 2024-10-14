"""Con este archivo abrimos y hacemos la principal limpieza del dataset de los 100 libros más vendidos de amazon durante los años
2009 a 2021"""

import pandas as pd
import numpy as np

url= "../data/kindle_data-v2.csv"
df = pd.DataFrame()
def clean_dataset(url):
    df = pd.read_csv(url)
    df.drop(df[df["title"].isnull()].index, inplace=True)
    #df.drop(columns=['Unnamed: 0'], inplace=True)
    df = df.dropna(how="all", axis= 1)
    for column in df.columns:
        print("Va por: ", column)
        if df[column].dtype == object:
            print("tipo columna: ", df[column].dtype)
            df[column] = df[column].astype(str)
            df[column] = df[column].str.strip()
    return df

df = clean_dataset(url)

# Inclusión de columna ranking que indica la posición actual de cada libro.
ranking = list(range(1,len(df)+1))
df["Ranking"] = ranking

# creación de un ranking según el número de reviews por categoría.
categories = df["category_name"].unique()
df_ranking = df.copy()
for categorie in categories:
    print(categorie)
    df_categorie = df[df["category_name"] == categorie].copy()
    df_categorie = df_categorie.sort_values(by= ["reviews"], ascending= False)
    df_categorie["ranking_" + str(categorie)] = range(1, len(df_categorie) + 1)
    df_ranking = pd.merge(df_ranking,df_categorie, how="left")

# para eliminar todos los libros que no estén en el ranking 100 de su categoría
for categorie in categories:
    df_ranking.drop(df_ranking[df_ranking["ranking_" + str(categorie)] > 100].index, inplace=True)

df_ranking.to_csv("../data/a_kindle100cat.csv")
