import streamlit as st

def filtrar_uf(base):
    selecionar_uf = base['uf_cand'].unique().tolist()
    filtro_uf = st.sidebar.multiselect(
        'Selecione as UFs',
        selecionar_uf,
        help="Selecione as UFs para filtrar os dados.",
    )    
    return filtro_uf

def filtro_partido(base):
    # Primeiro: filtro de partido
    selecionar_partido = base['sg_partido'].unique().tolist()
    filtro_partido = st.sidebar.multiselect(
        "Selecione os partidos",
        selecionar_partido,
        default= 'PSDB',
        help="Selecione os partidos para filtrar os dados.",
    )
    return filtro_partido

def filtro_eleitorado(base):
    # Calcular min e max
    if len(base) > 0:
        min_slider = int(base['Eleitorado'].min())
        max_slider = int(base['Eleitorado'].max())
    else:
        min_slider = int(base['Eleitorado'].min())
        max_slider = int(base['Eleitorado'].max())
    
    # Verificar se todos os valores são iguais
    if min_slider == max_slider:
        # Formatar número com separadores de milhar
        valor_formatado = f"{min_slider:,.0f}".replace(",", ".")
        
        st.write("**Eleitorado por município**")
        st.info(f"🎯 {valor_formatado} eleitores")
        st.caption("Todos os municípios filtrados têm o mesmo eleitorado")
        
        return base
    else:
        # Slider normal
        intervalo_votos = st.slider(
            label="Eleitorado por município",
            min_value=min_slider,
            max_value=max_slider,
            value=(min_slider, max_slider),
            step=50000,
            help="Deslize para filtrar por quantidade de eleitorado (incrementos de 50.000)"
        )
        
        votos_min, votos_max = intervalo_votos
        base = base[
            (base['Eleitorado'] >= votos_min) & 
            (base['Eleitorado'] <= votos_max)
        ]
        return base

def filtro_resultado(base):
    opcoes_resultado = ["Eleito", "Não eleito"]
    filto_resultado = st.sidebar.pills("Resultado:", opcoes_resultado, selection_mode="single", default="Eleito")

    if filto_resultado is not None:
        base = base[base['ds_eleicao'] == filto_resultado]
    return base

def filtro_cargo(base):
    opcoes_resultado = ["Prefeito", "Vereador", "Vice-prefeito"]
    filtro_cargo = st.pills("Cargo:", opcoes_resultado, selection_mode="single", default='Prefeito')

    if filtro_cargo is not None:
        base = base[base['nm_cargo'] == filtro_cargo]
        
    return base

def filtro_top_partido(base, filtro):
    top_5_siglas = (
        base[
            (base['nm_cargo'] == filtro) & 
            (base['ds_eleicao'] == 'Eleito')
        ]
        .groupby('sg_partido')
        .size()
        .nlargest(4) # Top partidos por número de eleitos + PSDB
        .index
        .tolist()
    )

    if 'PSDB' not in top_5_siglas:
        top_5_siglas.append('PSDB')
    return top_5_siglas

def filtro_base_uf(base, filtro):
    if filtro is not None:
        base = base[base['uf_cand'] == filtro]
        return base
    return base

