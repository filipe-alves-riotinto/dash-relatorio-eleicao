import pandas as pd
import requests
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()
DATALAKE = os.getenv("DATALAKE")

def municipio():
    response = requests.get(f'{DATALAKE}/municipio.parquet', verify=False)  
    df_municipio = pd.read_parquet(BytesIO(response.content))
    
    #df_municipio = pd.read_parquet('dados/base/municipio.parquet')
    
    df_municipio = df_municipio[['id','uf', 'nome', 'capital', 'no_regiao_brasil', 'co_uf', 'co_ibge', 'co_regiao_brasil', 'nu_pop']].rename(columns={'uf': 'uf_cand','nome' : 'nm_municipio', 'id': 'id_municipio','co_uf': 'id_uf'})
    df_municipio = df_municipio[~df_municipio['uf_cand'].str.startswith('ZZ')] # Remove linhas com UF ZZ
    df_municipio['id_uf'] = df_municipio['id_uf'].astype(float).astype('Int64')
    df_municipio['nu_pop'] = df_municipio['nu_pop'].astype('Int64')
    df_municipio['co_ibge'] = df_municipio['co_ibge'].astype(str)
    df_municipio['co_regiao_brasil'] = df_municipio['co_regiao_brasil'].astype(float).astype(int).astype(str)
    #df_municipio['nu_pop'] = df_municipio['nu_pop'].astype(str)
    return df_municipio

# print(municipio().dtypes)
# print(municipio())