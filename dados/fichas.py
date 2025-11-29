import pandas as pd
import requests
from io import BytesIO
from dotenv import load_dotenv
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
DATALAKE = os.getenv("DATALAKE")
#https://datalake.psdb.org.br/
#https://datalake.psdb.org.br/eleicao2022/fichas2022.parquet

def fichas(ano):
    response = requests.get(f'{DATALAKE}/{ano}/fichas{ano}.parquet', verify=False)  
    df_fichas = pd.read_parquet(BytesIO(response.content))
    
    #df_fichas = pd.read_parquet(f'dados/base/{ano}/fichas{ano}.parquet')
        
    df_fichas = df_fichas[df_fichas['ds_sit_urna'] == 'Consta da urna']
    df_fichas = df_fichas[df_fichas['sit_partido'].isin (['Deferido', 'Deferido com recurso'])]
    df_fichas = df_fichas[df_fichas['sit_cand'].isin (['Deferido', 'Deferido com recurso'])]
    df_fichas['ds_eleicao'] = df_fichas['ds_eleicao'].replace({
        'Eleito por média': 'Eleito',
        'Eleito por QP': 'Eleito',
        'Suplente' : 'Não eleito',
        'Concorrendo' : 'Não eleito',
    })
    
    df_fichas['ds_raca'] = df_fichas['ds_raca'].replace({
        'INDÍGENA': 'PRETA',
        'AMARELA': 'PRETA',
        'PARDA' : 'PRETA',
        #'SEM INFORMAÇÃO' : 'PRETA',
    })
    
    if ano == "2024":
        df_fichas['ds_eleicao'] = df_fichas['ds_eleicao'].replace({
        "2º turno" : "Não eleito"
        })
        df_fichas.rename(columns={'munCandidatura': 'id_municipio'}, inplace =True)
        
    df_fichas['nm_cargo'] = df_fichas['nm_cargo'].replace({'Deputado Distrital': 'Deputado Estadual'})
    #df_fichas['id_cand'] = df_fichas['id_cand'].astype(str)

    df_fichas.drop(columns=['ds_sit_urna', 'sit_partido', 'sit_cand', 'nu_cpf',
                            'st_reeleicao', 'dt_atualizacao', 'nu_partido',
                            'ds_coligacao', 'nu_urna', 'cd_sit_candidato', 'ds_sit_candidato', 
                            'ds_totalizacao', 'cd_cargo', 'ds_email', 'nu_cnpj', 'ds_composicao'], inplace=True)
    
    df_fichas['li_foto'] = df_fichas['li_foto'].str.replace('datarepo', 'datalake')
    if ano == '2022':
        df_fichas.loc[df_fichas['nu_titulo_eleitor'] == '026474760906', 'ds_eleicao'] = 'Eleito' #Incluir GEOVANIA DE SA na lista de eleitos
     
    
    return df_fichas

