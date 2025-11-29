import streamlit as st
from paginas.exibir_pagina import exibir_pagina
from utils.carga_banco import iniciar_federal
from utils.css import css


def main():
    css()
    iniciar_federal()
    df = st.session_state.federal

    ### Configurações do Streamlit
    st.set_page_config(layout='wide', page_title='Eleição')
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Filtros")
        # Seleção de aba via sidebar (opcional)
        aba_selecionada = st.radio(
            "Cargo:",
            ["🧑‍💼 Dep. Federal", "👥 Dep. Estadual"]
        )
        if aba_selecionada == '🧑‍💼 Dep. Federal':
            cargo = 'Deputado Federal' 
        elif aba_selecionada == "👥 Dep. Estadual":
            cargo = 'Deputado Estadual'
            
        df = df[df['nm_cargo'] == cargo]
        
        #RESULTADO
        opcoes_resultado = ["Eleito", "Não eleito"]
        filtro_resultado = st.sidebar.pills("Resultado:", opcoes_resultado, selection_mode="single", default="Eleito")

        #Chama a aba
    if aba_selecionada == "🧑‍💼 Dep. Federal":
        #exibir_depFederal(df, filtro_resultado, pagina=cargo)
        exibir_pagina(df, filtro_resultado, pagina=cargo)
    else:
        exibir_pagina(df, filtro_resultado, pagina=cargo)
    #st.dataframe(df)

if __name__ == "__main__":
    main()