import pandas as pd
import requests
from io import BytesIO
from dotenv import load_dotenv
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
DATALAKE = os.getenv("DATALAKE")

def votacao(ano, tipo = None):
    response = requests.get(f'{DATALAKE}/{ano}/votomunicipio{ano}.parquet', verify=False)  
    df_votacao = pd.read_parquet(BytesIO(response.content)).rename(columns={'sq_candidato': 'id_cand'})
    
    #df_votacao = pd.read_parquet(f'dados/base/{ano}/votos{ano}.parquet').rename(columns={'sq_candidato': 'id_cand'})
    df_votacao['qt_votos_nom_validos'] = df_votacao['qt_votos_nom_validos'].astype('Int64')
    if ano == '2022':
        if tipo == 'estadual':
            # Soma os votos por estado
            df_resultado = df_votacao.groupby(['co_uf', 'id_cand']).agg({
                'qt_votos_nom_validos': 'sum'
            }).reset_index().rename(columns={'co_uf': 'id_uf'}).astype('Int64')
            
        elif tipo == 'federal':
            # Soma os votos totais
            df_resultado = df_votacao.groupby(['id_cand']).agg({
                'qt_votos_nom_validos': 'sum'
            }).reset_index()

        else:
            # Votos por municipio.
            df_resultado = df_votacao[['co_uf','id','id_cand','qt_votos_nom_validos']].rename(columns={'co_uf': 'id_uf','id': 'id_municipio'})


    else:
        df_resultado = df_votacao[['sg_uf','id_cand','qt_votos_nom_validos']].rename(columns={'sg_uf': 'id_municipio'})
    
    return df_resultado

#print(votacao('2022', tipo='federal').dtypes)
#print(votacao('2022', tipo='federal'))
