import pandas as pd
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()
DATALAKE = os.getenv("DATALAKE")

def fefc(ano):

    response = requests.get(f'{DATALAKE}/{ano}/prestacaocontas{ano}.parquet', verify=False)  
    df_fefc = pd.read_parquet(BytesIO(response.content))
    
    #df_fefc = pd.read_parquet(f'dados/base/{ano}/prestacaocontas{ano}.parquet')
    
    df_fefc = df_fefc[df_fefc['nm_doador'].str.startswith('Direção Nacional - ', na=False)]
    df_fefc['nm_doador'] = df_fefc['nm_doador'].str.replace('Direção Nacional - ', '', regex=False)
    df_fefc["vl_receita"] = df_fefc["vl_receita"].fillna(0)
    df_fefc = df_fefc[df_fefc['ds_origem'] == 'Fundo Especial']

    df_fefc = df_fefc.drop_duplicates(subset=['id_cand', 'ds_recibo_eleitoral', 'vl_receita'])
    df_fefc = df_fefc.groupby(['id_cand', 'nm_doador'])['vl_receita'].sum().reset_index()
    df_fefc = df_fefc[['id_cand', 'vl_receita', 'nm_doador']].rename(columns={'vl_receita' : 'FEFC'})
    df_fefc['id_cand'] = df_fefc['id_cand'].astype('Int64')    
    
    return df_fefc

