# utils.py
import streamlit as st
from dados.processamento import base_federal, base_estadual  # ajuste com seu import real

#def inicializar_session_state():
#    """Inicializa ou atualiza o session_state"""
#    if 'ano_selecionado' not in st.session_state:
#        st.session_state.ano_selecionado = "2022"
#    if 'tipo_dados' not in st.session_state:
#        st.session_state.tipo_dados = "federal"  # ou "municipal"
#    if 'base_dados' not in st.session_state:
#        st.session_state.base_dados = base_federal(st.session_state.ano_selecionado, tipo='federal')
        
def iniciar_municipal():
    if 'municipal' not in st.session_state:
        st.session_state.municipal = base_estadual(ano='2024')

def iniciar_federal():
    if 'federal' not in st.session_state:
        st.session_state.federal = base_federal(ano='2022')