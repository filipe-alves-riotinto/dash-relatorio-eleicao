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
            ["Governador","Vice-governador","Senador","Dep. Federal", "Dep. Estadual"],
            #index = None
        )        
        if aba_selecionada == "Governador":
            cargo = 'Governador'
        elif aba_selecionada == "Vice-governador":
            cargo = 'Vice-governador'
        elif aba_selecionada == "Senador":
            cargo = 'Senador'
        elif aba_selecionada == 'Dep. Federal':
            cargo = 'Deputado Federal' 
        elif aba_selecionada == "Dep. Estadual":
            cargo = 'Deputado Estadual'
            
        df = df[df['nm_cargo'] == cargo]

    st.dataframe(df)
    #Chama a aba
    if aba_selecionada == "Governador":
        exibir_pagina(df, pagina=cargo)
    elif aba_selecionada == "Vice-governador":
        exibir_pagina(df, pagina=cargo)
    elif aba_selecionada == "Senador":
        exibir_pagina(df, pagina=cargo)
    elif aba_selecionada == "Dep. Federal":
        exibir_pagina(df, pagina=cargo)
    elif aba_selecionada == "Dep. Estadual":
        exibir_pagina(df, pagina=cargo)   
    

if __name__ == "__main__":
    main()