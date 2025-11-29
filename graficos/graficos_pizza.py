import streamlit as st
import plotly.express as px
from configuracoes.cores import cores


def grafico_pizza_distribuicao_fefc_partido(base_filtrada):
    #df_base = base[base['nm_cargo'] == filtro]

    pizza = px.pie(
        base_filtrada,
        names='sg_partido',
        values='FEFC',
        title='Distribuição de FEFC por Partido',
        color='sg_partido',
        color_discrete_map=cores,
        hole=0.3,
        labels={'sg_partido': 'Partido', 'FEFC': 'Valor FEFC'}
    )
    pizza.update_traces(textposition='inside')
    pizza.update_layout(uniformtext_minsize=12,uniformtext_mode='hide')
    pizza.update_layout(
        legend=dict(
            title='Partidos',
            orientation='v',  # Vertical (padrão)
            yanchor='top',    # Ancora no topo
            xanchor='left',   # Ancora à esquerda (dentro da área da legenda)
            #x=1.5,           # Posiciona fora do gráfico (valores >1 ou <0 permitem ajuste fino)
            y=1,             # Alinha ao topo do gráfico
            itemsizing='constant',  # Mantém tamanho consistente dos itens
            tracegroupgap=10,       # Espaço entre grupos (útil se houver subgrupos)
            itemwidth=30,           # Largura de cada item (ajuste conforme necessário)
            font=dict(size=12),     # Tamanho da fonte (opcional)
            # Se quiser múltiplas colunas, use:
            entrywidthmode='fraction',  # Define largura proporcional
            entrywidth=0.5,             # Largura de cada entrada (ajuste conforme necessário)
        ),
        margin=dict(r=180)  # Aumenta a margem direita para caber a legenda
    )

    st.plotly_chart(pizza, use_container_width=True)
    
    
def grafico_raca_genero_resultado(base_filtrada):
    # Gráfico de distribuição por raça/gênero
    fig = px.sunburst(base_filtrada, path=['ds_raca', 'ds_genero', 'ds_eleicao'], 
                    title='Distribuição de Candidatos por Raça, Gênero e Resultado')
    st.plotly_chart(fig) 