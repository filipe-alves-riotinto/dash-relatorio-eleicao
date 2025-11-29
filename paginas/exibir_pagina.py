import streamlit as st
from paginas.abas.relatorio_cand import relatorio_candidato
from utils.carga_banco import iniciar_municipal
from graficos.graficos_card import grafico_card_resultados
from graficos.graficos_mapas import mapa_municipal
from graficos.graficos_tabela import grafico_tabela_dados
from filtros.filtros import filtro_eleitorado, filtrar_uf, filtro_partido
import plotly.express as px


def exibir_pagina(df, filtro_resultado, pagina):
    st.title(f'{pagina}')
        #APLICA FILTRO DE RESULTADO DA ELEIÇÃO
    if filtro_resultado is not None:
        df_resultado = df[df['ds_eleicao'] == filtro_resultado]
    else:
        df_resultado = df
        
    #APLICA FILTRO DE PARTIDO
    filtro_partido_selecioando = filtro_partido(df_resultado)
        # Aplica filtro de partido se houver seleção
    if filtro_partido_selecioando:
        base_filtrada_partido = df_resultado[df_resultado['sg_partido'].isin(filtro_partido_selecioando)]
    else:
        base_filtrada_partido = df_resultado
        
    #APLICAR FILTRO UF
    filtro_uf = filtrar_uf(base_filtrada_partido)
        # Aplica filtro de UF se houver seleção
    if filtro_uf:
        base_filtrada = base_filtrada_partido[base_filtrada_partido['uf_cand'].isin(filtro_uf)]
    else:
        base_filtrada = base_filtrada_partido
    
    relatorio_candidato(df, base_filtrada, ufs=filtro_uf, partidos=filtro_partido_selecioando, cargo = pagina)

    # #MONTAR ABAS
    # aba_candidato, aba_partido = st.tabs(['📈Relatótio de candidato', '🏛️Relatótio de partido'])
    
    # with aba_candidato:
    #     relatorio_candidato(df, base_filtrada, ufs=filtro_uf, partidos=filtro_partido_selecioando, cargo = pagina)

    
    # with aba_partido:      
    #     st.title('ABA PARTIDO')