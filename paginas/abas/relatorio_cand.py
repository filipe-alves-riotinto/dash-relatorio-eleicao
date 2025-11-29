
import streamlit as st

from graficos.graficos_linhas import grafico_linha_cand_por_uf
from graficos.graficos_pizza import grafico_raca_genero_resultado
from graficos.graficos_card import grafico_card_resultados
from graficos.graficos_mapas import mapa_federal, mapa_municipal
from graficos.graficos_tabela import grafico_tabela_dados
from graficos.graficos_barras import grafico_barra_cand_por_partido, grafico_barra_cand_região, grafico_barra_votos_região
from graficos.graficos_card import grafico_card_resultados


def relatorio_candidato(df, base_filtrada, ufs, partidos, cargo):
    
    grafico_card_resultados(df, ufs, partidos)

    col1, col2 = st.columns(2)
    with col1:
        if cargo in ["Prefeito", "Vereador"]:
            mapa_municipal(base_filtrada)
        else:
            mapa_federal(base_filtrada)
        grafico_barra_votos_região(base_filtrada)
        grafico_raca_genero_resultado(base_filtrada)
        
    with col2:
        grafico_barra_cand_por_partido(base_filtrada, filtro=cargo)
        grafico_barra_cand_região(base_filtrada)
        grafico_linha_cand_por_uf(base_filtrada, filtro=cargo)
        
                 
    # # Top 10 candidatos mais votados
    # top_candidatos = base_filtrada.nlargest(10, 'qt_votos_nom_validos')
    # fig2 = px.bar(top_candidatos, x='nm_cand', y='qt_votos_nom_validos',
    #             color='sg_partido', title="Top 10 Candidatos Mais Votados")
    # st.plotly_chart(fig2)
        
    grafico_tabela_dados(base_filtrada)