"""
Destinado para a execução do servidor streamlit

()
"""
import pandas as pd
import streamlit as st 
from core import *

@st.cache_data
def carregar_csv():
    df = pd.read_csv('Pokemon.csv')
    return df

df = carregar_csv()

st.title("📊Dashboard interativo de Pokemon📊")

st.sidebar.title('Configurações')

st.sidebar.header("Análise de Atributos")
atributo = st.sidebar.selectbox(
    "Escolha o atributo para análise:",
    ['HP','Attack','Defense','Sp. Atk','Sp. Def', 'Speed']
)

st.header("Comparativo: Pokémon de Um Tipo vs. Dois Tipos")
fig_comparacao = comparar_tipos(df, atributo)
st.pyplot(fig_comparacao)

st.divider()

st.header("Análise de Balanço Ofensivo vs. Defensivo")
st.sidebar.header("Filtros do Gráfico de Balanço")

todos_tipos = sorted(pd.concat([df['Type 1'], df['Type 2']]).dropna().unique())

tipos_selecionados = st.sidebar.multiselect(
    'Selecione os tipos para exibir:',
    options=todos_tipos,
    default=todos_tipos
)

gerar_grafico_balanco(df, tipos_selecionados)
