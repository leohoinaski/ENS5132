# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 14:46:05 2025

Este script foi criado na terceira aula da disciplina ENS5132. Nesta aula, 
trabalharemos com:
    - Arrays numpy
    - Pandas DataFrame
    - Matplotlib
    
    * requisitos: pip install spyder numpy pandas matplotlib

@author: Leonardo.Hoinaski
"""

#%% Importação de pacotes
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% Relembrando listas

# Criando uma lista com inteiros, string e float
listA = [1, 2 ,3 , 'Salve o Corithians', 20.5]
print(listA)

# Criando uma lista com inteiros e float
listB = [1, 2 ,3, 20.5]

#%% Trabalhando com numpy

# Criando um array numpy
arr = np.array([0.7, 0.75, 1.85])
print(arr)

# Criando um array numpy a partir de uma lista
arr2 = np.array(listA)

# Criando um array numpy a partir de uma lista apenas com números
arr3 = np.array(listB)

# Criando uma matriz
precip = np.array([[1.07, 0.44, 1.50],[0.27, 1.33, 1.72]])

# acessando valor da primeira linha e coluna
print(precip[0,0])

# acessando todos os valores da primeira linha
print(precip[0,:])

# acessando todos os valores da primeira coluna
print(precip[:,0])
precipSlice = precip[:,0]

# extraindo os dois primeiros valores da primeira linha
print(precip[0,0:2])

# extraindo o último valor da última coluna
print(precip[-1,-1])

#------------------------------------------------------------------------------
# Criando matrizes com multiplas dimensões

# Criar um arranjo de dados com início, fim e passo
x = np.arange(1,16,1)

# Mundando o shape/dimensão da matriz
xReshape = x.reshape(3,5)

# Transposta
print(xReshape.transpose())


# Criando matriz de números aleatórios 3D
matRand = np.random.rand(10,100,100)

# Recortando matriz
matRandSlice = matRand[0,:,:]

# Criando matriz com 4D
matRand4D = np.random.rand(3,10,100,100)

# Dimensão da matriz
print(matRand4D.ndim)

# Shape da matriz
print(matRand4D.shape)

# Número de elementos
print(matRand4D.size)

# Multiplicação escalar
print(matRand4D*3.9)

# Abrir dados de um arquivo de texto
dataSample = np.loadtxt(r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\data\dataSample.txt")

# Abrir arquivo com formato separado por vírgula .csv
dataSample2 = np.loadtxt(r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\data\dataSample2.csv",
                         delimiter=',')

# Média da matriz 4D
print(matRand4D.mean()) #   Média da matriz inteira

print(matRand4D.max(axis=0))
maxMat4D = matRand4D.max(axis=0)

#%% Pandas DataFrame

# Dados vieram de: https://energiaeambiente.org.br/produto/plataforma-da-qualidade-do-ar
df = pd.read_csv(r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\data\MQAR\SP\SP201501.csv",
                 encoding='Latin1')

df.describe()
df.info()
df[df.Poluente=='MP10'].Valor.plot()
pd.to_datetime(df.Data,format='%Y-%m-%d')


