import streamlit as st   


def css():
    # CSS mais específico para centralização
    st.markdown("""
    <style>
    [data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    padding: 5px 10px;
    border-radius: 10px;
    text-align: center;
    }
    [data-testid="stMetricLabel"] {
    display: flex;
    justify-content: center;
    font-size: 16px !important;
    font-weight: bold !important;
    }
    [data-testid="stMetricValue"] {
    display: flex;
    justify-content: center;
    font-size: 30px !important;
    font-weight: bold !important;
    }
    [data-testid="stMetricDelta"] {
    display: flex;
    justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)