"""Con este archivo abrimos y hacemos la principal limpieza del dataset de los 100 libros más vendidos de amazon durante los años
2009 a 2021"""

import pandas as pd
import numpy as np

url= "../data/Amazon_top100.xlsx"

def clean_dataset(url):
    df = pd.read_excel(url)
    df.drop(df[df["title"].isnull()].index, inplace=True)
    df.drop(columns=['Unnamed: 0'], inplace=True)
    df = df.dropna(how="all", axis= 1)
    df["title"] = df["title"].astype(str)
    df['title'] = df['title'].str.strip()
    df['author'] = df['author'].str.strip()
    df['cover_type'] = df['cover_type'].str.strip()
    df['genre'] = df['genre'].str.strip()

    df.to_csv("../data/amazon100a.csv")

clean_dataset(url)