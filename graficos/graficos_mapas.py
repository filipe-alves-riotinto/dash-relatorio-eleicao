import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from dados.mapa import carregar_marcadores_regiao, carregar_marcadores_uf, carregar_marcadores_municipio
from configuracoes.cores import cores
import streamlit as st

def mapa_municipal(base):
    #col1, col2, col3 = st.columns([1, 2, 1])
    #with col2:                 
    fichas = base[['uf_cand', 'nm_municipio','sg_partido', 'nm_cargo', 'nm_cand','co_ibge']]
    cores_dict = cores
    df_point = pd.merge(
        fichas,
        carregar_marcadores_municipio(),
        left_on='co_ibge',
        right_on='codarea',
        how='left'
    )
    df_point = gpd.GeoDataFrame(df_point, geometry=df_point['geometry'])
    ### CRIAR MAPA
    # Crie o mapa base
    mapa = folium.Map(location=[-15.7797, -47.9297],
                    tiles='CartoDB positron',
                    max_bounds=True,
                    zoom_start=4,
                    min_zoom=4,
                    max_zoom=4,
                    )

    
        # Camada de Região
    # folium.GeoJson(
    #     carregar_marcadores_regiao(), 
    #     name='Regiao',
    #     style_function=lambda x: {
    #     #'fillColor': 'blue',
    #     #'fillColor': 'black',
    #     'color': 'black',
    #     'weight': 1.5,
    #     'fillOpacity': 0.1
    #     },
    #     ).add_to(mapa)

    # Camada de UF
    folium.GeoJson(
        carregar_marcadores_uf(), 
        name='Brasil',
        style_function=lambda x: {
        #'fillColor': 'blue',
        #'fillColor': 'black',
        #'color': 'blue',
        'weight': 1.5,
        'fillOpacity': 0.1
        },
        ).add_to(mapa)


    # Camada dos municípios
    folium.GeoJson(
        df_point,  # Seu DataFrame com os municípios
        name='Prefeituras',
        style_function=lambda feature: {
            'fillColor': cores_dict.get(feature['properties']['sg_partido']),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['uf_cand','nm_municipio', 'nm_cargo', 'nm_cand',  'sg_partido'],
            aliases=['UF: ','Município:', 'Cargo:', 'Candidato:', 'Partido: '],
            localize=True
        )
    ).add_to(mapa)

    


    mapa.options['maxBounds'] = [[-35, -75], [6, -30]]  # Limites do Brasil
    mapa.options['worldCopyJump'] = False  # Impede rotação infinita do mapa

    # Controle de camadas
    folium.LayerControl().add_to(mapa)

    st_folium(mapa, width=700, height=500)
    
def mapa_federal(base):
    #col1, col2, col3 = st.columns([1, 2, 1])
    #with col2:                 
    fichas = base[['uf_cand', 'nm_municipio','sg_partido', 'nm_cargo', 'nm_cand','id_uf']]
    fichas['id_uf'] = fichas['id_uf'].astype(str)
    cores_dict = cores

    # Agrupar os candidatos por UF
    candidatos_por_uf = fichas.groupby('id_uf').apply(
        lambda x: '<br>'.join([
            f"{row['nm_cand']} - ({row['sg_partido']})"
            for _, row in x.iterrows()
        ])
    ).to_dict()

    # Contar candidatos por UF
    contagem_por_uf = fichas.groupby('id_uf').size().to_dict()

    df_point = pd.merge(
        fichas,
        carregar_marcadores_uf(),
        left_on='id_uf',
        right_on='codarea',
        how='left'
    )
    df_point = gpd.GeoDataFrame(df_point, geometry=df_point['geometry'])

    # Adicionar colunas com informações agrupadas ao DataFrame
    df_point['total_candidatos'] = df_point['id_uf'].map(contagem_por_uf)
    df_point['lista_candidatos'] = df_point['id_uf'].map(candidatos_por_uf)

    # Remover duplicatas para ter uma linha por UF
    df_point_uf = df_point.drop_duplicates(subset=['id_uf']).copy()

    ### CRIAR MAPA
    # Crie o mapa base
    mapa = folium.Map(location=[-15.7797, -47.9297],
                    tiles='CartoDB positron',
                    max_bounds=True,
                    zoom_start=4,
                    min_zoom=4,
                    max_zoom=4,
                    )

    # Camada da UF
    folium.GeoJson(
        carregar_marcadores_uf(), 
        name='Brasil',
        style_function=lambda x: {
        'weight': 1.5,
        'fillOpacity': 0.1
        },
    ).add_to(mapa)

    # Camada dos estados
        # Camada dos estados com popup
    geojson_layer = folium.GeoJson(
        df_point_uf,
        name='Estados',
        style_function=lambda feature: {
            'fillColor': cores_dict.get(feature['properties']['sg_partido']),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['uf_cand', 'total_candidatos'],
            aliases=['UF: ', 'Total de Candidatos: '],
            localize=True
        )
    )

    geojson_layer.add_child(folium.features.GeoJsonPopup(
        fields=['uf_cand', 'total_candidatos', 'lista_candidatos'],
        aliases=['UF: ', 'Total: ', 'Candidatos: '],
        localize=True,
        labels=True
    ))

    geojson_layer.add_to(mapa)

    mapa.options['maxBounds'] = [[-35, -75], [6, -30]]
    mapa.options['worldCopyJump'] = False

    # Controle de camadas
    folium.LayerControl().add_to(mapa)

    st_folium(mapa, width=700, height=500)
    
