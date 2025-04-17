# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 15:49:21 2025

@author: Leonardo.Hoinaski
"""

import matplotlib.pyplot as plt
import os
import numpy as np
from scipy import stats
import statsmodels.api as sm

def airQualityHist(aqData,stations,uf,repoPath):
    os.makedirs(repoPath+'/figuras/'+uf, exist_ok=True)
    
    for st in stations:
        fig, ax = plt.subplots()
        aqData[aqData.Estacao==st].hist('Valor',by='Poluente', ax=ax)
        fig.savefig(repoPath+'/figuras/'+uf+'/hist_'+st+'.png')
        
def airQualityTimeSeries(aqData,stations,uf,repoPath):
    os.makedirs(repoPath+'/figuras/'+uf, exist_ok=True)
    
    # Loop para cada estação
    for st in stations:
        
        #Extraindo poluentes para determinada estação
        pollutants = np.unique(aqData[aqData.Estacao==st].Poluente)
        
        # Criando figura com número de poluentes de cada estação
        fig, ax = plt.subplots(pollutants.size)
        
        # Loop para cada poluente
        for ii, pol in enumerate(pollutants):
            if pollutants.size>1:
                ax[ii].plot(
                    aqData[(aqData.Estacao==st) & (aqData.Poluente == pol)].Valor)
                fig.savefig(repoPath+'/figuras/'+uf+'/plot_'+st+'.png')
            else:
                ax.plot(
                    aqData[(aqData.Estacao==st) & (aqData.Poluente == pol)].Valor)
                fig.savefig(repoPath+'/figuras/'+uf+'/plot_'+st+'.png')
                

def normalityCheck(aqTableAlvo,repoPath,uf,stationAlvo,pol):
    # Figura para verificar a distribuição dos dados 
    fig, ax = plt.subplots(3)
    ax[0].hist(np.log(aqTableAlvo[pol].dropna()),facecolor='red')
    ax[0].set_title('Log')
    ax[0].set_ylabel('Frequência')
    ax[1].hist(stats.boxcox(aqTableAlvo[pol].dropna()),facecolor='green')
    ax[1].set_title('Boxcox')
    ax[1].set_ylabel('Frequência')
    ax[2].hist(aqTableAlvo[pol].dropna())
    ax[2].set_title('Dado original')
    ax[2].set_ylabel('Frequência')
    fig.tight_layout() 
    fig.savefig(repoPath+'/figuras/'+uf+'/histogramDataNormalization_'+pol+'_'+stationAlvo+'.png')
    return fig

def trendFigures(data,result):
    fig, ax = plt.subplots(2)
    sm.graphics.tsa.plot_acf(data, lags=5, ax=ax[0]);
    ax[0].set_title('Autocorrelação ACF')
    trend_line = np.arange(len(data)) * result.slope + result.intercept
    data.plot(ax=ax[1])
    ax[1].plot(data.index, trend_line)
    ax[1].legend(['data', 'trend line'])
    ax[1].set_title('Tendência')
    return fig

def timeSeriesForecast(complete_data,repoPath,uf,pol,stationAlvo):
    # Previsão usando modelo de série temporal
    # pip install pmdarima
    from pmdarima.arima import auto_arima

    stepwise_model = auto_arima(complete_data, start_p=1,start_q=1,max_p=3,max_q=3,m=12,
                       seasonal=True, error_action='ignore')

    print(stepwise_model.aic())
    
    # Segregando grupo de treinamento e test 
    train = pd.DataFrame({'train':complete_data.iloc[0:int(complete_data.shape[0]*0.7)]})
    test = pd.DataFrame({'test':complete_data.iloc[int(complete_data.shape[0]*0.7):]})
    
    # Calibrando o modelo
    stepwise_model.fit(train)
    
    #
    future_forecast = pd.DataFrame({'future_forecast':stepwise_model.predict(n_periods=test.shape[0])})
    
    fig, axes = plt.subplots()
    #pd.concat([test,future_forecast],axis=1).dropna(axis='rows').plot() 
    pd.concat([complete_data,future_forecast],axis=1).plot(ax=axes) 
    fig.savefig(repoPath+'/figuras/'+uf+'/timeSeriesForecast'+pol+'_'+stationAlvo+'.png')
    return fig