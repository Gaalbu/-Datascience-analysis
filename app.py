"""
Destinado para a execução do servidor streamlit

()
"""
import pandas as pd
import streamlit as st 
from core import *

df = pd.read_csv('Pokemon.csv')

st.title("📊Dashboard interativo de Pokemon📊")

st.sidebar.title('Configurações')

atributo = st.sidebar.selectbox(
    "Escolha o atributo para análise:",
    ['HP','Attack','Defense','Sp. Atk','Sp. Def', 'Speed']
)
comparar_tipos(df,atributo)
