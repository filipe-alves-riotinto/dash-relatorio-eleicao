import pandas as pd
import requests
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()
DATALAKE = os.getenv("DATALAKE")

def eleitorado(ano):
    response = requests.get(f'{DATALAKE}/{ano}/eleitorado{ano}.parquet', verify=False)  
    df_eleitorado = pd.read_parquet(BytesIO(response.content))
    
    #df_eleitorado = pd.read_parquet(f'dados/base/{ano}/eleitorado{ano}.parquet')
    
    df_eleitorado['Eleitorado'] = df_eleitorado['Eleitorado'].astype('Int64')
    #df_eleitorado['Eleitorado'] = df_eleitorado['Eleitorado'].fillna(0)
    return df_eleitorado
