# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 15:49:21 2025

@author: Leonardo.Hoinaski
"""

import matplotlib.pyplot as plt
import os
import numpy as np

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