# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 14:43:46 2025

Script para realizar estatística univariada dos dados de qualidade do ar para
cada estação e poluente. 

@author: Leonardo.Hoinaski
"""
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mk
from statsmodels.tsa.seasonal import seasonal_decompose


# CUIDADO AS VARIÁVEIS stations e aqTable não existem neste script. Precisará 
# rodar o main.py
# Usando a primeira estação como exemplo
stationAlvo = stations[0]

# Criando novo aqTable com colunas de datetime e Estacao
aqTableNew = aqTable.reset_index()

# Usando lógica para selecionar o dado da estação no DataFrame
aqTableAlvo = aqTableNew[aqTableNew.Estacao==stationAlvo]

# Teste de normalidade- Gaussianidade
testLog = stats.normaltest(np.log(aqTableAlvo['MP10'].dropna()))
testBox = stats.normaltest(stats.boxcox(aqTableAlvo['MP10'].dropna())[0])


#
fig, ax = plt.subplots(3)
ax[0].hist(np.log(aqTableAlvo['MP10'].dropna()))
ax[0].set_xlabel('Log')
ax[1].hist(stats.boxcox(aqTableAlvo['MP10'].dropna()))
ax[1].set_xlabel('Boxcox')
ax[2].hist(aqTableAlvo['MP10'].dropna())
ax[2].set_xlabel('Dado original')


# Teste de tendência - MannKendall
# Tarefa... fazer média anual e extrair o coeficiente de tedÊncia. Usar groupby
#result = mk.original_test(np.array(aqTableAlvo['MP10'].dropna()))


# Análise de sazonalidade
def markham_index(monthly_values):
    """
    Calculate the Markham Seasonality Index.

    Parameters:
    monthly_values (list or np.array): 12 monthly values (e.g., number of events per month)

    Returns:
    float: Markham Index (0 to 100)
    """
    monthly_values = np.array(monthly_values)
    mean_value = np.mean(monthly_values)
    
    numerator = np.sum(np.abs(monthly_values - mean_value))
    denominator = 2 * np.sum(monthly_values)
    
    msi = (numerator / denominator) * 100
    return msi

# Example usage
# Monthly data (e.g., fire counts per month)
msi = markham_index(aqTableAlvo['MP10'].dropna())
print(f"Markham Seasonality Index: {msi:.2f}")


# Decomposição da série temporal - AINDA FALTA FAZER FUNCIONAR
dataDecompose = aqTableAlvo[['MP10','datetime']]
dataDecompose = dataDecompose.set_index('datetime')
dataDecompose[dataDecompose['MP10']==np.nan]= np.median(dataDecompose[dataDecompose['MP10']==np.nan])
#decompose = seasonal_decompose(dataDecompose)


# Previsão usando modelo de série temporal
import plotly as ply
# pip install pyramid-arima
from pyramid.arima import auto_arima



model = pyramid.arima.auto_arima(dataDecompose, start_p=1,start_q=1,max_p=3,max_q=3,m=12,
                   seasonal=True, error_action='ignore')






