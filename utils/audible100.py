import pandas as pd
import numpy as np

url= "../data/Audible_Top_100_Final.csv"
df = pd.DataFrame()
def clean_dataset(url):
    df = pd.read_csv(url, encoding='windows-1252')
    # para eliminar filas sin titulo si las hubiera. OJO, la columna de los títulos puede tener diferente nombre según el dataset
    df.drop(df[df["Title"].isnull()].index, inplace=True)
    # para eliminar columna unnamed si la hubiera
    #df.drop(columns=['Unnamed: 0'], inplace=True)
    # eliminación de columnas en las que todos los valores son nulos
    df = df.dropna(how="all", axis= 1)
    # para convertir las columnas de tipo object en string y limpiar posibles espacios por delante y por detrás
    for column in df.columns:
        print("Va por: ", column)
        if df[column].dtype == object:
            print("tipo columna: ", df[column].dtype)
            df[column] = df[column].astype(str)
            df[column] = df[column].str.strip()
    df = df.iloc[:,:-9].copy()
    df = df.iloc[:,0:13].copy()
    return df

df = clean_dataset(url)

# para quedarme con las columnas que me interesan
df = df.iloc[:,:-9].copy()
df = df.iloc[:,0:13].copy()

# creación de un ranking según el número de reviews por categoría.
categories = df["Categories"].unique()
df_ranking = df.copy()
for categorie in categories:
    print(categorie)
    df_categorie = df[df["Categories"] == categorie].copy()
    df_categorie = df_categorie.sort_values(by= ["Ratings"], ascending= False)
    df_categorie["ranking_" + str(categorie)] = range(1, len(df_categorie) + 1)
    df_ranking = pd.merge(df_ranking,df_categorie, how="left")

df_ranking.to_csv("../data/a_audible100.csv")
