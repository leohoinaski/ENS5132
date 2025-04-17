# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 13:48:12 2025


Este script será utilizado para analisar os dados de qualidade do ar disponibi-
lizados pela plataforma do Instituto Energia e Meio Ambiente. 


     Abrir corretamente o dado
     Inserir coluna datetime 
     Criar coluna com estação do ano
     Filtrar dataframe
     Extrair estatísticas básicas
     Estatísticas por agrupamento
     Exportar estatísticas agrupadas
     Criar uma função para realizar as tarefas acima
     Criar função para gerar figuras 
     Loop para qualquer arquivo dentro da pasta
     Estatística univariada e bivariada – função exclusiva
     Análise de dados usando o statsmodel



@author: Leonardo.Hoinaski
"""

# Importação dos pacotes
import pandas as pd
import numpy as np
import os


def airQualityAnalysis(uf,repoPath):
    # -------------------------- Abrir os dados -----------------------------------
    # Criando variável com o nome do estado
    #uf = 'SP'
    
    # Definindo o caminho para a pasta de dados
    dataDir = repoPath+'/inputs/'+ uf
    
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
    aqData = pd.concat(allFiles)
    
    # Caminho para um dos arquivos
    #aqPath = r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\projeto01\inputs\SP\SP201501.csv"
    
    # Abrir dados de apenas uma das estações de monitoramento de SP
    #aqData = pd.read_csv(aqPath, encoding='latin1')
    
    
    # ----------------------- Inserir coluna datetime------------------------------
    # Criando coluna datetime
    datetimeDf = pd.to_datetime(aqData.Data, format='%Y-%m-%d')
    
    # Criando coluna datetime dentro de aqData
    aqData['datetime'] = datetimeDf
    
    # Transformando a coluna de datetime em index
    aqData = aqData.set_index(aqData['datetime'])
    
    # Extrair o ano e mês
    aqData['year'] = aqData.index.year
    aqData['month'] = aqData.index.month
    aqData['day'] = aqData.index.day
    
    # Extraindo a hora
    horas  = aqData.Hora.str.split(':')
    
    horaDf = []
    for hora in horas:
        #print(hora[0])
        horaDf.append(hora[0])
    
    aqData['hour'] = horaDf
    
    
    # Corrigindo a coluna datetime
    aqData['datetime'] = pd.to_datetime(
        aqData[['year', 'month','day','hour']],format='%Y%m%d %H')
    
    # Reiniciando minha index datetime
    aqData = aqData.set_index(aqData['datetime'])
    
    
    # ------------------------Estação do ano---------------------------------------
    # Criando uma coluna de Estacao com NaN 
    aqData['Season'] = np.nan
    
    # Verão
    aqData['Season'][(aqData.month==1) | (aqData.month==12) | 
                      (aqData.month==2) ] = 'Verão'
    # Outono
    aqData['Season'][(aqData.month==3) | (aqData.month==5) | 
                      (aqData.month==4) ] = 'Outono'
    # Inverno
    aqData['Season'][(aqData.month==6) | (aqData.month==7) | 
                      (aqData.month==8) ] = 'Inverno'
    # Primavera
    aqData['Season'][(aqData.month==9) | (aqData.month==10) | 
                      (aqData.month==11) ] = 'Primavera'
    
    
    # ---------------------Estatísticas básicas ----------------------------------
    # Extrair o nome dos poluentes sem redundância
    #pollutants = np.unique(aqData.Poluente)
    
    # lista de estações
    stations = np.unique(aqData.Estacao)
    
    # criando pasta para salvar os dado
    os.makedirs(repoPath+'/outputs/'+uf,exist_ok=True)
    
    # # Loop para cada poluente e extraindo as estatísticas básicas
    # for st in stations:
    #     print(st)
    #     statAll =[]
    #     for pol in pollutants:
    #         print(pol)
    #         basicStat = aqData['Valor'][(aqData.Poluente==pol) & 
    #                                     (aqData.Estacao==st)].describe()
    #         basicStat = pd.DataFrame(basicStat)
    #         basicStat.columns =[pol]
    #         statAll.append(basicStat)       
        
    #     # Unindo as estatísticas por poluente
    #     dfmerge = pd.concat(statAll,axis=1)
        
    #     # Salva as estatísticas por estação    
    #     dfmerge.to_csv(r'C:\Users\Leonardo.Hoinaski\Documents\ENS5132\projeto01\outputs'
    #                          +'/'+uf+'/basicStat_'+st+'.csv')
    
    
    # Estatística básica usando groupby
    statGroup = aqData.groupby(['Estacao','Poluente']).describe()
    
    # Salvando em csv
    statGroup.to_csv(repoPath+'/outputs/'+uf+'/basicStat_ALL.csv')
    
    # Coloca o índice da matriz como a coluna datetime
    aqData = aqData.set_index(pd.DatetimeIndex(aqData['datetime']))
    
    # Criando uma tabela de dados com cada poluente em colunas diferentes.
    aqTable = aqData.reset_index(drop=True).pivot_table(
        columns='Poluente',
        index=['Estacao','datetime'],
        values='Valor')

    return aqData, stations, aqTable