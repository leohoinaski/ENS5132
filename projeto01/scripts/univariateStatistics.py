# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 14:43:46 2025

Script para realizar estatística univariada dos dados de qualidade do ar para
cada estação e poluente. 

@author: Leonardo.Hoinaski
"""
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mk
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
from airQualityFigures import normalityCheck, trendFigures,timeSeriesForecast
from datetime import datetime
# Análise de sazonalidade
import warnings
warnings.filterwarnings('ignore')

def markham_index(monthly_values):
    """
    Calculate the Markham Seasonality Index.

    Parameters:
    monthly_values (list or np.array): 12 monthly values (e.g., number of events per month)

    Returns:
    float: Markham Index (0 to 100)
    """
    monthly_values = np.array(monthly_values)
    mean_value = np.nanmean(monthly_values)
    
    numerator = np.nansum(np.abs(monthly_values - mean_value))
    denominator = 2 * np.nansum(monthly_values)
    
    msi = (numerator / denominator) * 100
    return msi


def timeSeriesDecompose(aqTableAlvo,pol,uf,repoPath,stationAlvo):
    
    # Decomposição da série temporal
    # Seleciona apenas a coluna de um dos poluentes
    dataDecompose = aqTableAlvo[[pol,'datetime']]
    #dataDecompose = dataDecompose.set_index('datetime')
    dataDecomposeMonthly = dataDecompose.groupby(pd.PeriodIndex(dataDecompose['datetime'], freq="M"))[pol].mean()
    
    # Formta a o dataframe para funcionar na função seasonal_decompose do statsmodel
    dataDecomposeMonthly = pd.Series(np.array(dataDecomposeMonthly), index = pd.PeriodIndex(dataDecomposeMonthly.index))

    # Gerando um PeriodIndex completo no intervalo desejado
    full_index = pd.period_range(start=dataDecomposeMonthly.index.min(), end=dataDecomposeMonthly.index.max(), freq='M')

    # Reindexando para preencher os períodos faltantes com NaN
    complete_data = dataDecomposeMonthly.reindex(full_index)
    
    # Interpolando dados que possuem nan
    complete_data = complete_data.interpolate().dropna()
    complete_data.index = complete_data.index.to_timestamp()
    # Decompondo a série repetição em 12 meses
    res = seasonal_decompose(complete_data,period=12) 
    
    # Gerando figura
    fig, axes = plt.subplots(ncols=1, nrows=4, sharex=True)
    res.observed.plot(ax=axes[0], legend=False,color='blue')
    axes[0].set_ylabel('Observed')
    res.trend.plot(ax=axes[1], legend=False, color='red')
    axes[1].set_ylabel('Trend')
    res.seasonal.plot(ax=axes[2], legend=False, color='yellow')
    axes[2].set_ylabel('Seasonal')
    res.resid.plot(ax=axes[3], legend=False, color='gray')
    axes[3].set_ylabel('Residual')
    fig.savefig(repoPath+'/figuras/'+uf+'/decompose_'+pol+'_'+stationAlvo+'.png')
    
    return res,complete_data

def univariateStatistics(aqTable,stations,uf,repoPath):

    
    # CUIDADO AS VARIÁVEIS stations e aqTable não existem neste script. Precisará 
    # rodar o main.py
    # Usando a primeira estação como exemplo
    
    # Incializando as lista para acumular os testes de tendência para cada estação
    trend, h, p, z, Tau, s, var_s, slope, intercept = [],[],[],[],[],[],[],[],[]
    
    #Incializando as lista para acumular os testes de Markham de sazonalidade para cada estação
    MarkhamIndex=[]
    
    # INiciando lista para loop em estações e poluentes
    st, pols = [], [] 
    
    #loop em todas as estações
    for stationAlvo in stations:
        print(stationAlvo+'==========')
        #stationAlvo = stations[0]
        
        # Criando novo aqTable com colunas de datetime e Estacao
        aqTableNew = aqTable.reset_index()
        
        # Usando lógica para selecionar o dado da estação no DataFrame
        aqTableAlvo = aqTableNew[aqTableNew.Estacao==stationAlvo].dropna(axis=1, how='all')
        
        # Teste de normalidade- Gaussianidade
        #testLog = stats.normaltest(np.log(aqTableAlvo['MP10'].dropna()))
        #testBox = stats.normaltest(stats.boxcox(aqTableAlvo['MP10'].dropna())[0])
        
        #Extraindo poluentes para determinada estação
        pollutants = aqTableAlvo.columns[2:]
        
        #Loop para cada poluente
        for ii, pol in enumerate(pollutants):
            print(pol + '------------')
            
            # Indice de Markham mensal
            dataDecomposeMonthly = aqTableAlvo.groupby(
                pd.PeriodIndex(aqTableAlvo['datetime'], freq="M"))[pol].agg(np.nanmean)
            
            # Gerando um PeriodIndex completo no intervalo desejado
            full_index = pd.period_range(
                start=datetime(int(pd.DatetimeIndex(dataDecomposeMonthly.index.to_timestamp()).year.min()),1,1),
                end=datetime(int(pd.DatetimeIndex(dataDecomposeMonthly.index.to_timestamp()).year.max()),12,31),
                freq='M')

            # Reindexando para preencher os períodos faltantes com NaN
            complete_data = dataDecomposeMonthly.reindex(full_index)
            
            
            
            # chama a função que cria a figura no scrip airQualityFigures para gerar
            # Histogramas com transformações
            # normalityCheck(aqTableAlvo,repoPath,uf,stationAlvo,pol)
            
            
            # Decomposição e previsão
            try:
                res,complete_data=timeSeriesDecompose(aqTableAlvo,pol,uf,repoPath,stationAlvo)
                timeSeriesForecast(complete_data,repoPath,uf,pol,stationAlvo)
            except:
                print('Não foi possível decompor a série de dados')
                    
            
            # Teste de tendência - MannKendall
            # acumulando para cada estação
            try:
                result = mk.original_test(aqTableAlvo.groupby(pd.PeriodIndex(
                    aqTableAlvo['datetime'], freq="A"))[pol].median())              
                #print(result)
                trend.append(result.trend)
                h.append(result.h)
                p.append(result.p)
                z.append(result.z)
                Tau.append(result.Tau)
                s.append(result.s)
                var_s.append(result.var_s)
                slope.append(result.slope)
                intercept.append(result.intercept)
                st.append(stationAlvo)
                pols.append(pol)
                msi = markham_index(complete_data)
                MarkhamIndex.append(msi)
                print(f"Markham Seasonality Index: {msi:.2f}")
                
                # Gerar figuras das tendÊncias
                trendFigures(aqTableAlvo.groupby(pd.PeriodIndex(
                    aqTableAlvo['datetime'], freq="A"))[pol].median(),result)
                
            except:
                trend.append(np.nan)
                h.append(np.nan)
                p.append(np.nan)
                z.append(np.nan)
                Tau.append(np.nan)
                s.append(np.nan)
                var_s.append(np.nan)
                slope.append(np.nan)
                intercept.append(np.nan)
                st.append(stationAlvo)
                pols.append(pol)
                MarkhamIndex.append(np.nan)

    
    # Preenchendo o dataframe com os dados do teste de tendência para cada estação
    univariateStats = pd.DataFrame({'station':st,
                                    'pollutant':pols,
                                    'trend':trend, 
                                    'h':h, 
                                    'p':p, 
                                    'z':z,
                                    'Tau':Tau, 
                                    's':s, 
                                    'var_s':var_s,
                                    'slope':slope,
                                    'intercept':intercept,
                                    'MarkhamIndex':MarkhamIndex})    
        
    univariateStats.to_csv(repoPath+'/outputs/'+uf+'/univariateStats.csv')
    
    return univariateStats