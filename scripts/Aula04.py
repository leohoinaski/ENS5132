# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 13:42:20 2025

Este script utilizei durante a aula 04 no dia 01/04/2025. 


@author: Leonardo.Hoinaski
"""

#%% Importando os pacotes que utilizarei
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#%% Revisão numpy

# Criando um vetor com arranjo de dados
x = np.arange(-10,20,0.15)

# Brincando com indexação
print('Esta é a quarta posição do meu vetor x:' + str(x[3]))

print('Estes são os 3 primeiros valores' + str(x[0:3]))

# Substituir um valor dentro do vetor
x[9] = 99999999 # exemplo de medição errada
x[11] = -99999999 # exemplo de medição errada

# extraindo a média 
meanX = np.mean(x)
print(meanX)

# Operação booleana 
# and = &
# or = |
# Encontrando valores errados
vecBool = (x>20) | (x<-10) # estou usando o simbolo | para or

# Extraindo valores errados usando lógica booleana
valErrado = x[vecBool]

# Substituindo os valores errados por 0
x2 = x.copy() # criando uma cópia independente
x2[vecBool] = 0
print('Esta é a média de x substituindo valores errados por 0: '+
      str(np.mean(x2)))

# Substituindo por NaN - Not a number
x3 = x.copy() # criando uma cópia independente
x3[vecBool] = np.nan
print('Esta é a média de x substituindo valores errados por nan: '+
      str(np.mean(x3)))

print('Esta é a média usando np.nanmean de x substituindo valores errados por nan: '+
      str(np.nanmean(x3)))

# Substuindo pela média
x4 = x.copy() # criando uma cópia independente
x4[vecBool] = np.nanmean(x3)
print('Esta é a média de x substituindo valores errados por nan: '+
      str(np.mean(x4)))


#%% Usando matplotlib para inspecionar os vetores

fig, ax = plt.subplots(4)
ax[0].plot(x)
ax[1].plot(x2)
ax[2].plot(x3)
ax[3].plot(x4)


#%% Loop em python

# Loop utilizando Range
for ii in range(0,10):
    val = 2**ii
    print(val)

# Loop utilizando Range e acumulando em um vetor
vetor = []
for ii in range(0,10):
    val = 2**ii
    vetor.append(val)
    
# Loop utilizando Range e acumulando o valor de val em um vetor
vetorAcumulado = []
val = 0
for ii in range(0,10):
    val = val+2**ii
    vetorAcumulado.append(val)
    

# Loop utilizando uma lista
alunas = ['Mariana', 'Bianca', 'AnaJúlia', 'Mariah']

for aluna in alunas:
    print( 'A nota da '+aluna+' é : '+str(np.random.rand(1)*10))


#%% Trabalhando com Pandas!!

# Criando um DataFrame manualmente

df = pd.DataFrame(columns=['date','NH3'],
                  data=[
                      ['2025/04/01',0.35],
                      ['2025/04/02',1.01]
                      ])

# Criando mais coisas dentro do df
df['NO3'] = np.nan 
df['O2'] = [2 , 10]
df['SO4'] = np.nan 
df['SO4'][0] = 10

#%% Trabalhando com dado real
# Criando variável com o nome do estado
uf = 'SP'

# Definindo o caminho para a pasta de dados
dataDir = r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\data\MQAR" +'/'+ uf

# Lista de arquivos dentro da pasta
dataList = os.listdir(dataDir)

# Movendo para a pasta de dados/uf
os.chdir(dataDir)

allFiles =[]
# Loop na lista dataList 
for fileInList in dataList:
    print(fileInList)
    dfConc = pd.read_csv(fileInList,encoding='latin1')
    allFiles.append(dfConc)

# Concatenando meus DataFrames
allFiles = pd.concat(allFiles)

# Extraindo nomes das estações sem redundância
stations = pd.unique(allFiles['Estacao'])

# usando lógica...
stationDf = allFiles[allFiles['Estacao'] == stations[0]]

# Criando coluna datetime
datetimeDf = pd.to_datetime(stationDf.Data, format='%Y-%m-%d')

# Criando coluna datetime dentro de stationDf
stationDf['datetime'] = datetimeDf

# Transformando a coluna de datetime em index
stationDf = stationDf.set_index(stationDf['datetime'])

# Extrair o ano e mês
stationDf['year'] = stationDf.index.year
stationDf['month'] = stationDf.index.month
stationDf['day'] = stationDf.index.day

# Extraindo a hora
horas  = stationDf.Hora.str.split(':')

horaDf = []
for hora in horas:
    print(hora[0])
    horaDf.append(hora[0])

stationDf['hour'] = horaDf


# Corrigindo a coluna datetime
stationDf['datetime'] = pd.to_datetime(stationDf.astype(str).year+
                                       stationDf.astype(str).month+
                                       stationDf.astype(str).day+
                                       stationDf.astype(str).hour,
                                       format='%Y%m%d%H')


