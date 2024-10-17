import pandas as pd
import numpy as np
import os
import shutil

# para abrir excel y pasarlo a csv eliminando columna unnamed si la hubiera
df = pd.DataFrame(pd.read_excel("../data/Amazon_top100.xlsx"))
df.drop(columns=['Unnamed: 0'], inplace=True)
df.to_csv("../data/amazon100.csv")

# para abrir un csv y eliminar columna unnamed si la hubiera
df = pd.read_csv("../data/bestsellers_with_categories_2022_03_27.csv")
df.drop(columns=['Unnamed: 0'], inplace=True)

# eliminación de columnas en las que todos los valores son nulos
df = df.dropna(how="all", axis= 1)

# para eliminar todas las filas que cumplan una condicion
df.drop(df[df["reviews"] <= 20].index, inplace=True)

url= "../data/kindle_data-v2.csv"
df = pd.DataFrame()
def clean_dataset(url):
    df = pd.read_csv(url)
    # para eliminar filas sin titulo si las hubiera. OJO, la columna de los títulos puede tener diferente nombre según el dataset
    df.drop(df[df["title"].isnull()].index, inplace=True)
    # para eliminar columna unnamed si la hubiera
    df.drop(columns=['Unnamed: 0'], inplace=True)
    # eliminación de columnas en las que todos los valores son nulos
    df = df.dropna(how="all", axis= 1)
    # para convertir las columnas de tipo object en string y limpiar posibles espacios por delante y por detrás
    for column in df.columns:
        print("Va por: ", column)
        if df[column].dtype == object:
            print("tipo columna: ", df[column].dtype)
            df[column] = df[column].astype(str)
            df[column] = df[column].str.strip()
            df[column] = df[column].str.lower()
    return df

df = clean_dataset(url)

# para añadir un ranking en una nueva columna basándose en otra columna del dataframe (ejemplo)
years = df["Year"].unique()
df = df.copy()
for year in years:
    print(year)
    df_year = df[df["Year"] == year].copy()
    df_year["top_50_" + str(year)] = range(1, len(df_year) + 1)
    df_amazon_ranking = pd.merge(df_amazon_ranking,df_year, how="left")

# creación de un ranking según el número de reviews por categoría.
categories = df["category_name"].unique()
df_kindle_ranking = df.copy()
for categorie in categories:
    print(categorie)
    df_categorie = df[df["category_name"] == categorie].copy()
    df_categorie = df_categorie.sort_values(by= ["reviews"], ascending= False)
    df_categorie["ranking_" + str(categorie)] = range(1, len(df_categorie) + 1)
    df_kindle_ranking = pd.merge(df_kindle_ranking,df_categorie, how="left")

