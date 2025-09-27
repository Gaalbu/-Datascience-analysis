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
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

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


def gerar_grafico_balanco(df, tipos_selecionados):
    df_copy = df.copy()
    df_copy.rename(columns={
        'Type 1': 'Type1', 'Type 2': 'Type2',
        'Sp. Atk': 'SpAtk', 'Sp. Def': 'SpDef'
    }, inplace=True)

    df_copy['AtaqueTotal'] = df_copy['Attack'] + df_copy['SpAtk']
    df_copy['DefesaTotal'] = df_copy['Defense'] + df_copy['SpDef']

    df_type1 = df_copy[['Name', 'Type1', 'AtaqueTotal', 'DefesaTotal']].rename(columns={'Type1': 'Type'})
    df_type2 = df_copy[['Name', 'Type2', 'AtaqueTotal', 'DefesaTotal']].rename(columns={'Type2': 'Type'}).dropna()
    df_types = pd.concat([df_type1, df_type2], ignore_index=True)

    type_stats = df_types.groupby('Type').agg(
        AtaqueMedio=('AtaqueTotal', 'mean'),
        DefesaMedia=('DefesaTotal', 'mean'),
        Contagem=('Name', 'count')
    ).reset_index()

    type_stats['AtaqueMedio'] = round(type_stats['AtaqueMedio'], 2)
    type_stats['DefesaMedia'] = round(type_stats['DefesaMedia'], 2)
    
    if tipos_selecionados:
        type_stats_filtrado = type_stats[type_stats['Type'].isin(tipos_selecionados)]
    else:
        type_stats_filtrado = type_stats
    
    if type_stats_filtrado.empty:
        st.warning("Nenhum tipo selecionado para exibição.")
        return

    fig = px.scatter(
        type_stats_filtrado,
        x='AtaqueMedio',
        y='DefesaMedia',
        color='Type',
        text='Type',
        size='Contagem',
        hover_name='Type',
        hover_data={'AtaqueMedio': ':.2f', 'DefesaMedia': ':.2f', 'Type': False}
    )

    max_val = max(type_stats['AtaqueMedio'].max(), type_stats['DefesaMedia'].max()) + 15
    fig.add_shape(type='line', x0=70, y0=70, x1=max_val, y1=max_val,
                  line=dict(color='Red', dash='dash'))

    fig.update_traces(textposition='top center')
    fig.update_layout(
        title='Ataque Médio vs. Defesa Média por Tipo de Pokémon',
        xaxis_title='Ataque Total Médio (Físico + Especial)',
        yaxis_title='Defesa Total Média (Física + Especial)',
        height=700,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)



#Treinamento da regressão linear, modelagem
def treinar_regressao(df, features, alvo):
    
    if not features:
        raise ValueError ('Sem features p/ regressão')

    x = df[features]
    y = df[alvo]

    xTreino, xTeste, yTreino, yTeste = train_test_split(x, y, test_size=0.2, random_state=42)

    modelo = LinearRegression()
    modelo.fit(xTreino, yTreino)
    yPredicao = modelo.predict(xTeste)

    metricas = {
        'MSE': mean_squared_error(yTeste, yPredicao),
        'R2': r2_score(yTeste, yPredicao)
    }
    return modelo, yTeste, yPredicao, metricas

#teste
def correlacaoPearson(df, col1, col2):
    corr, p = sts.pearsonr(df[col1], df[col2])
    return corr, p


#Scatter da comparação entre o teste e a predição
def scatterAtualVsPredicao(yTeste, yPredicao, alvo):
    fig = px.scatter(
        x = yTeste, y=yPredicao,
        labels = {'x': f'{alvo} real', 'y':f'{alvo} previsto'},
        title=f'Regressão Linear - {alvo}'
    )
    fig.add_shape(
        type='line', x0 = yTeste.min(), y0 = yTeste.min(),
        x1 = yTeste.max(), y1 = yTeste.max(),
        line = dict(color = 'red', dash = 'dash')
    )
    return fig

#Plotando a matriz no streamlit
def plotMatrizCorrelacao(df, cols):
    matrizCorrelacao = df[cols].corr()
    fig = px.imshow(
        matrizCorrelacao,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        title='Matriz de Correlação Pokémon'
    )
    return fig