import streamlit as st
import plotly.express as px
from configuracoes.cores import cores


def grafico_barra_cand_região(base_filtrada):
        # Mapa por região/estado
    regiao_analysis = base_filtrada.groupby('no_regiao_brasil').agg({
        'nu_titulo_eleitor': 'count'
    }).reset_index()

    fig = px.bar(regiao_analysis, 
                 x='no_regiao_brasil', 
                 y='nu_titulo_eleitor',
                 color='no_regiao_brasil',
                title='Total de Candidatos por Região',
                labels={
                     'no_regiao_brasil': 'Região',
                     'nu_titulo_eleitor': 'Candidatos'
                 })
    st.plotly_chart(fig)

def grafico_barra_votos_região(base_filtrada):
        # Mapa por região/estado
    regiao_analysis = base_filtrada.groupby('no_regiao_brasil').agg({
        'nu_titulo_eleitor': 'count',
        'qt_votos_nom_validos': 'sum'
    }).reset_index()

    fig = px.bar(regiao_analysis, 
                 x='no_regiao_brasil', 
                 y='qt_votos_nom_validos',
                 color='no_regiao_brasil',
                title='Total de Votos por Região',
                                labels={
                     'no_regiao_brasil': 'Região',
                     'qt_votos_nom_validos': 'Total de Votos'
                 })
    st.plotly_chart(fig)

def grafico_barra_cand_por_partido(base_filtrada, filtro):
    
    #base_filtrada = base[base['nm_cargo'] == filtro]
    total_por_partido = base_filtrada.groupby(['sg_partido']).size().reset_index(name=f'Total {filtro} por Partido')

    fig_grafico_barra = px.bar(
        total_por_partido, 
        x='sg_partido', 
        y=f'Total {filtro} por Partido', 
        color='sg_partido',
        color_discrete_map=cores,
        height=500,
        labels={
            'sg_partido': 'Partido',
            f'Total {filtro} por Partido': f'Total {filtro} por Partido'
        },
        category_orders={"sg_partido": sorted(total_por_partido['sg_partido'].unique())}
    )
    fig_grafico_barra.update_layout(
        legend=dict(
            title='Partidos',
            orientation='h',
            yanchor='bottom',
            y= 1.0,
            xanchor='right',
            x=1
        ))
    fig_grafico_barra.update_traces(texttemplate='%{y}', textposition='outside')
    
    st.plotly_chart(fig_grafico_barra)
    
def grafico_barra_valor_partido(base, filtro):
    df_valor = base[base['nm_cargo'] == filtro]
    total_por_partido = df_valor.groupby(['sg_partido'])['FEFC'].sum().reset_index()
    #total_por_partido['FEFC'] = total_por_partido['FEFC'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) 
    #total_por_partido['FEFC'] = total_por_partido['FEFC'].apply(lambda x: format(x, '.2f'))

    #total_uf_partido = df_valor.groupby('sg_partido').agg({
    #    'nm_cand': 'count',
    #    'FEFC': 'sum'
    #}).reset_index()


    fig_grafico_barra = px.bar(
            total_por_partido, 
            x='sg_partido', 
            y='FEFC',
            text = total_por_partido['FEFC'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
            color='sg_partido',
            #title='Gráfico FEFC',
            color_discrete_map=cores,
            #labels={'FEFC': 'Valor'},
            text_auto='.2s',
            #category_orders={"sg_partido": sorted(total_por_partido['sg_partido'].unique())}
        )

    fig_grafico_barra.update_layout(
        legend=dict(
            title='Partidos',
            orientation='h',
            yanchor='bottom',
            y= 1.0,
            xanchor='right',
            x=1
        )
    )

    st.plotly_chart(fig_grafico_barra, use_container_width=True)