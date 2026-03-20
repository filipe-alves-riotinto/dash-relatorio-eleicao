import pandas as pd
import requests
from io import BytesIO
from dotenv import load_dotenv
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
DATALAKE = os.getenv("DATALAKE")

def votacao(ano):
    response = requests.get(f'{DATALAKE}/eleicao{ano}/votacao{ano}.parquet', verify=False)  
    df_votacao = pd.read_parquet(BytesIO(response.content)).rename(
        columns={
            'SQ_CANDIDATO': 'id_cand', 
            'SG_UE': 'co_uf',
            'CD_MUNICIPIO': 'id_municipio',
            'QT_VOTOS_NOMINAIS_VALIDOS' : 'qt_votos_nom_validos'})
    
    #df_votacao = pd.read_parquet(f'dados/baseDash/{ano}/votos{ano}.parquet').rename(columns={'sq_candidato': 'id_cand'})
    df_votacao['qt_votos_nom_validos'] = df_votacao['qt_votos_nom_validos'].astype('Int64')
    
    df_votacao = df_votacao[df_votacao['NR_TURNO'] == 1].copy()
    
    # Verificar se a coluna CD_MUNICIPIO existe
    if 'id_municipio' in df_votacao.columns:
        # Agrupar com id_municipio
        df_resultado = df_votacao.groupby(['id_cand', 'co_uf', 'id_municipio'])['qt_votos_nom_validos'].sum().reset_index()
    else:
        # Agrupar sem id_municipio
        df_resultado = df_votacao.groupby(['id_cand'])['qt_votos_nom_validos'].sum().reset_index()
    
    return df_resultado

#print(votacao('2022', tipo='federal').dtypes)
#print(votacao(2022))
