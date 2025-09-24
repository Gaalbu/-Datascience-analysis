"""
Arquivo de conexão servidor-notebook
"""

# %% [markdown]
# # Imports

# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as sts
import seaborn as sns
import plotly.express as px
# %%
df = pd.read_csv('Pokemon.csv')
df.head(5)

# %%
df.info()

# %% [markdown]
# ### Indentificando valores nulos/NaN

# %%
df['Type 2'].isnull().sum()

# %% [markdown]
# Os dados que não possuem entrada se referem aos pokemons únicamente tipados.

# %% [markdown]
# ### Entendendo relações

# %% [markdown]
# Com o dataset analisado, podemos começar a gerar insights sobre o mesmo.

# %% [markdown]
# $$
#     H0: Fd = Fu
# $$

# %% [markdown]
# Aqui estamos tentando analisar se a força(Attack) dos pokemons duplamente tipados é superior aos unicamente tipados, utilizando o Teste t de Student para tal.

# %%
###PLOT DA DISTRIBUICAO DE ATAQUE X TIPAGEM
def plot_AtaqxTip():
    Fduplamente_tipados = df[df["Type 2"].notnull()]['Attack']
    Funicamente_tipados = df[df["Type 2"].isnull()]['Attack']


    plt.figure(figsize=(10,6))
    plt.hist(x = Fduplamente_tipados, edgecolor = 'black',density = True,label='Duplamente tipados')
    plt.hist(x = Funicamente_tipados, edgecolor = 'black',density = True,alpha = 0.65,label='Unicamente tipados')
    plt.xlabel("Força de ataque")
    plt.ylabel("Distribuição de pokemons")
    plt.title("Distribuição X Ataque")
    plt.legend()
    plt.show()



# %% [markdown]
# Então, se a H0 é falsa, vamos entender qual o comportamento da força entre os tipos.
# A força dos duplamente tipados é maior?
# $$
# H1: Fd > Fu
# $$

# %%
#alpha = 0.05
#ForcaFinal = sts.ttest_ind(Fduplamente_tipados,Funicamente_tipados,equal_var=pForça,alternative='greater').pvalue
#if ForcaFinal < alpha:
#    print("H1 é verdadeira, logo a força de ataque dos duplamente tipados é maior")
#else:
#    print("H1 é falsa, então a força dos duplamente tipados é menor que a força dos unicamente tipados")

# %%


# %%



