import streamlit as st


def grafico_card_resultados(base, ufs=None, partidos=None):
    # Aplica filtros de UF se fornecidos
    if ufs:
        base = base[base['uf_cand'].isin(ufs)]
    
    # Aplica filtros de partidos se fornecidos
    if partidos:
        base = base[base['sg_partido'].isin(partidos)]

    total_candidatos = base['nu_titulo_eleitor'].nunique()
    total_candidatos_eleitos = base[base['ds_eleicao'] == 'Eleito'].shape[0]
    total_candidatos_não_eleitos = base[base['ds_eleicao'] == 'Não eleito'].shape[0]
    
    total_votos_eleitos = base[base['ds_eleicao'] == 'Eleito']['qt_votos_nom_validos'].sum()
    total_votos = base['qt_votos_nom_validos'].sum()
    taxa_eleicao = (base['ds_eleicao'] == 'Eleito').mean() * 100
    
    # Formata os números com separador de milhares
    total_eleitos_formatado = "{:,.0f}".format(total_candidatos_eleitos).replace(",", ".")
    total_nao_eleitos_formatado = "{:,.0f}".format(total_candidatos_não_eleitos).replace(",", ".")
    total_candidatos_formatado = "{:,.0f}".format(total_candidatos).replace(",", ".")
    total_votos_formatado = "{:,.0f}".format(total_votos).replace(",", ".")
    total_votos_eleitos_formatado = "{:,.0f}".format(total_votos_eleitos).replace(",", ".")
    
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Eleito', total_eleitos_formatado)
        #st.metric("Total de Votos - Eleitos", total_votos_eleitos_formatado)
    with col2:
        st.metric('Não eleito', total_nao_eleitos_formatado)
        #st.metric("Total de Votos - Não eleitos", total_votos_formatado)
    with col3:
        st.metric('Total de candidatos', total_candidatos_formatado)
        
    with col4:
        st.metric("Taxa de Eleição", f"{taxa_eleicao:.1f}%")