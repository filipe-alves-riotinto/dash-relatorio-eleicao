import requests
from io import BytesIO
import geopandas as gpd
import urllib3
import streamlit as st

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def carregar_marcadores_regiao():
    # CARREGAR SEPARAÇÃO DE REGIAO
    url = "https://servicodados.ibge.gov.br/api/v4/malhas/paises/BR"
    params = {'formato': 'application/vnd.geo+json','qualidade':'minima', 'intrarregiao': 'regiao'}
    response = requests.get(url, params=params)
    regiao_marcadores = gpd.read_file(BytesIO(response.content))
    regiao_marcadores = regiao_marcadores.to_crs('EPSG:4326')
    return regiao_marcadores


#@st.cache_data
def carregar_marcadores_uf():
    # CARREGAR SEPARAÇÃO DE UF
    url = "https://servicodados.ibge.gov.br/api/v4/malhas/paises/BR"
    params = {'formato': 'application/vnd.geo+json', 'qualidade':'minima','intrarregiao': 'UF'}
    response = requests.get(url, params=params)
    uf_marcadores = gpd.read_file(BytesIO(response.content))
    uf_marcadores = uf_marcadores.to_crs('EPSG:4326')
    return uf_marcadores

print(carregar_marcadores_uf().dtypes)

@st.cache_data
def carregar_marcadores_municipio():
    # CARREGAR SEPARAÇÃO DE MUNICIPIO
    url = "https://servicodados.ibge.gov.br/api/v4/malhas/paises/BR"
    params = {'formato': 'application/vnd.geo+json','qualidade':'minima', 'intrarregiao': 'municipio'}
    response = requests.get(url, params=params)
    muncipio_marcadores = gpd.read_file(BytesIO(response.content))
    muncipio_marcadores = muncipio_marcadores.to_crs('EPSG:4326')
    return muncipio_marcadores