# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 15:32:16 2025

Lembre-se de criar as pastas corretamente

@author: Leonardo.Hoinaski
"""

# Importação de pacotes
from airQualityAnalysis import airQualityAnalysis
from airQualityFigures import airQualityHist, airQualityTimeSeries
import os
from univariateStatistics import univariateStatistics


# Reconhecer pasta do repositório
repoPath = os.path.dirname(os.getcwd())
print(repoPath)

# Definindo pasta de dados
dataPath = repoPath +'/inputs'

# Cria a pasta se ela não existir... precisam colocar os dados dentro dela.
os.makedirs(dataPath, exist_ok = True)

# Lista pastas dentro de dataPath
ufs = os.listdir(dataPath)

# Loop para todos os estados
for uf in ufs:
    
    #
    aqData, stations, aqTable = airQualityAnalysis(uf,repoPath)
    
    os.chdir(repoPath+'/scripts')
    #airQualityHist(aqData,stations,uf,repoPath)
    airQualityTimeSeries(aqData,stations,uf,repoPath)
    univariateStatistics(aqTable,stations,uf,repoPath)



