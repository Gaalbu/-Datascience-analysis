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
comparar_tipos(df, atributo)


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

st.divider()

st.header("Análise de Correlação")
cols = st.multiselect('Selecione colunas numéricas', df.select_dtypes(include = 'number').columns)
if len(cols) >= 2:
    fig_corr = plotMatrizCorrelacao(df, cols)
    st.plotly_chart(fig_corr)

    #Mostrando a correlação das duas escolhidas
    col1 = st.selectbox('Coluna 1', cols)
    col2 = st.selectbox('Coluna 2', cols)
    corr, pval = correlacaoPearson(df, col1, col2)
    st.write(f'Correlação {col1} vs {col2}: **{corr:.3f}** (p={pval:.3e})') #formatações de outputs

#Sessão da Regressão

st.header('Regressão Linear')
alvo = st.selectbox('Variável alvo:', df.select_dtypes(include = 'number').columns)

#Todas sem ser o alvo p/ comparar
features = st.multiselect('Variáveis explicativas:', [c for c in df.select_dtypes(include='number').columns if c != alvo]) 

if features:
    #Treino
    modelo, yTeste, yPredicao, metricas = treinar_regressao(df=df,features=features,alvo=alvo)
    st.write('### Métricas do Modelo')
    
    #Sabendo minuciosamente os params
    st.json(metricas)
    
    #Plotando o scatter do output
    fig = scatterAtualVsPredicao(yTeste, yPredicao, alvo)
    st.plotly_chart(fig)
else:
    st.warning("Selecione ao menos uma variável explicativa para treinar a regressão.")