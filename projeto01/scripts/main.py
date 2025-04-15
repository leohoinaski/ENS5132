# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 15:32:16 2025

@author: Leonardo.Hoinaski
"""

from airQualityAnalysis import airQualityAnalysis
from airQualityFigures import airQualityHist, airQualityTimeSeries
import os



# Reconhecer pasta do repositório
repoPath = os.path.dirname(os.getcwd())

# Definindo pasta de dados
dataPath = repoPath +'/inputs'

# Lista pastas dentro de dataPath
ufs = os.listdir(dataPath)


# Loop para todos os estados
for uf in ufs:
    
    aqData, stations, aqTable = airQualityAnalysis(uf)
    
    os.chdir(repoPath+'/scripts')
    #airQualityHist(aqData,stations,uf,repoPath)
    airQualityTimeSeries(aqData,stations,uf,repoPath)



