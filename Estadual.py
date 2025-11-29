import streamlit as st
from paginas.exibir_pagina import exibir_pagina
from utils.css import css
from utils.carga_banco import iniciar_municipal
from graficos.graficos_card import grafico_card_resultados
from graficos.graficos_mapas import mapa_municipal
from graficos.graficos_tabela import grafico_tabela_dados
from filtros.filtros import filtro_eleitorado, filtrar_uf, filtro_partido
import plotly.express as px


def exibir_vereadores(df, filtro_resultado):
    
    st.title('Vereadores')
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


    grafico_card_resultados(df, partidos=filtro_partido_selecioando)
    
    grafico_tabela_dados(base_filtrada_partido)
    
    
def main():
    css()
    iniciar_municipal()
    df = st.session_state.municipal
    
    ### Configurações do Streamlit
    st.set_page_config(layout='wide', page_title='Eleição')
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Filtros")
        # Seleção de aba via sidebar (opcional)
        aba_selecionada = st.radio(
            "Cargo:",
            ["🧑‍💼 Prefeitos", "👥 Vereadores"]
        )
        cargo = 'Prefeito' if aba_selecionada == "🧑‍💼 Prefeitos" else 'Vereador'
        df = df[df['nm_cargo'] == cargo]
        
        #RESULTADO
        opcoes_resultado = ["Eleito", "Não eleito"]
        filtro_resultado = st.sidebar.pills("Resultado:", opcoes_resultado, selection_mode="single", default="Eleito")


    #Chama a aba
    if aba_selecionada == "🧑‍💼 Prefeitos":
        exibir_pagina(df, filtro_resultado, pagina=cargo)
    else:
        exibir_pagina(df, filtro_resultado, pagina=cargo)


if __name__ == "__main__":
    main()