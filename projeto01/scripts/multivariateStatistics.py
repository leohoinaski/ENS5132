# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 14:32:09 2025

@author: Leonardo.Hoinaski
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# pip install scikit-learn
from sklearn.linear_model import LinearRegression
from sklearn import svm

def multivariateStatistics(aqTable):
    
    aqTableAlvo = aqTable.reset_index()[aqTable.reset_index()['Estacao']==stations[10]].iloc[:,3:]

    
    # Boxplot dos dados comparando todos os poluentes
    fig, ax = plt.subplots(2)
    sns.boxplot(data=aqTableAlvo,ax=ax[0])
    sns.violinplot(data=aqTableAlvo,ax=ax[1])
    
    
    # pairplot
    fig, ax = plt.subplots()
    sns.pairplot(aqTableAlvo)
    
    #regplot
    fig, ax = plt.subplots()
    sns.regplot(x= 'NO', y= 'NO2', data = aqTableAlvo)
    
    #pairgrid
    fig, ax = plt.subplots()
    g = sns.PairGrid(aqTableAlvo)
    g=g.map_upper(sns.scatterplot)
    g=g.map_lower(sns.kdeplot)
    g=g.map_diag(sns.kdeplot,lw=2)
    
    # Matriz de correlação
    fig, ax = plt.subplots()
    corr = aqTableAlvo.corr()
    corr.style.background_gradient(cmap='coolwarm', axis=None)
    sns.heatmap(corr,cmap='coolwarm')

    #Regressão linear multivariada
    # Eliminando colunas com nan e linhas com nan
    regData = np.array(aqTableAlvo[['MP10','NO','NO2','O3']].copy().dropna(axis=0))
    
    # aplicando a regressão - fit = otimização dos parâmetros do modelo
    reg = LinearRegression().fit(regData[:,1:],regData[:,0])
    
    # Erro quadrado do meu modelo
    reg.score(regData[:,1:],regData[:,0])
    
    # Coeficientes da equação
    reg.coef_
    
    
    # Previsão
    reg.predict(np.array([[10,100,100]]))
    
    # Usando aprendizagem de máquina
    clf = svm.SVC()
    clf.fit(regData[:,1:],regData[:,0])
    
    # Score
    clf.score(regData[:,1:],regData[:,0])
    clf.predict(np.array([[10,100,100]]))
    
    
    return 
