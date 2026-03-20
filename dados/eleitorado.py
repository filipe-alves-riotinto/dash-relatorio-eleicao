import pandas as pd
import requests
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()
DATALAKE = os.getenv("DATALAKE")

def eleitorado(ano):
    response = requests.get(f'{DATALAKE}/eleicao{ano}/eleitorado{ano}.parquet', verify=False)  
    df_eleitorado = pd.read_parquet(BytesIO(response.content))
    
    #df_eleitorado = pd.read_parquet(f'dados/baseDash/{ano}/eleitorado{ano}.parquet')
    
    df_eleitorado['QT_ELEITORES_PERFIL'] = df_eleitorado['QT_ELEITORES_PERFIL'].astype('Int64')
    
    return df_eleitorado
