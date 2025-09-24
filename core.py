"""
Arquivo de conexão servidor-notebook
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as sts
import seaborn as sns
import plotly.express as px
import streamlit as st

def comparar_tipos(df:pd.DataFrame, atributo: str):
    """
    Gera o gráfico e executa o t-test, entre os monotipos e duplo tipo

    params:
    -df: Dataframe com os dados
    -atributo: String com nome da coluna númerica
    """

    #Coluna comparativa
    df['eh_duplo'] = df['Type 2'].notnull()

    #Separação
    grupo_mono = df[df['eh_duplo'] == False]
    grupo_dual = df[df['eh_duplo'] == True]

    #erro aceitavel, para verificacao na levene func
    alpha = 0.05

    if sts.levene(grupo_mono[atributo],grupo_dual[atributo]).pvalue > alpha:
        t_stat, p = sts.ttest_ind(grupo_mono[atributo], grupo_dual[atributo],equal_var=False)
    else:
        t_stat, p = sts.ttest_ind(grupo_mono[atributo], grupo_dual[atributo],equal_var=True)

    #Resultado textual
    st.subheader(f"Teste t: Monotipo vs Duplo tipo para '{atributo}'")
    st.markdown(f"**Estatística t: ** {t_stat:.3f}")
    st.markdown(f"**p-valor:** {p:.5f}")

    if p < alpha:
        st.success(f"Diferença estatisticamente significativa (p < {alpha})")
    else:
        st.info(f"Sem diferença estatisticamente significativa (p >= {alpha})")
    
    #Gráfico
    fig = px.box(df, x = 'eh_duplo', y = atributo, color = 'eh_duplo', labels={'eh_duplo': 'Duplo tipo?', atributo: atributo}, title = f"Distribuição de {atributo} entre Mono tipo e Duplo tipo")

    st.plotly_chart(fig, use_container_width=True)