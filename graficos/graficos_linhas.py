import streamlit as st
import plotly.express as px
from configuracoes.cores import cores

def grafico_linha_cand_por_uf(base_filtrada, filtro = None):
    ##TABELAS
    total_por_uf = base_filtrada.groupby(['uf_cand', 'sg_partido']).size().reset_index(name=f'Total {filtro} por UF')

    ## GRAFICOS
    fig_grafico_linha = px.line(
        total_por_uf, 
        x='uf_cand', 
        y=f'Total {filtro} por UF', 
        color='sg_partido',
        color_discrete_map=cores,
        markers=True,
        #title='Deputado Federal',
        labels={
            'uf_cand': 'UF',
            f'Total {filtro} por UF': f'Total {filtro} por UF',
            'sg_partido': 'Partido'
        },
        category_orders={"uf_cand": sorted(total_por_uf['uf_cand'].unique())}
    )

    fig_grafico_linha.update_layout(
        hovermode='x unified',
        legend=dict(
            title='Partidos',
            orientation='h',
            yanchor='bottom',
            y= 1.0,
            xanchor='right',
            x=1
        )
    )
    st.plotly_chart(fig_grafico_linha)
