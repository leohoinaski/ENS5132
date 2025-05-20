# -*- coding: utf-8 -*-
"""
Created on Tue May 13 13:52:39 2025

Este script será utilizado para realizar análise no espaço com shapefiles de 
municípios do IBGE (https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2024/Brasil/BR_Municipios_2024.zip)

@author: Leonardo.Hoinaski
"""

# Importação de pacotes
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import matplotlib.pyplot as plt
import folium
import contextily as cx
import rasterio as rio

# Caminho para o arquivo com o shapefile dos municípios
munPath = r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\projeto02\inputs\BR_Municipios_2024\BR_Municipios_2024.shp"

# Abrindo o arquivo shapefile
geoMun = gpd.read_file(munPath)

# Extraindo o sistema de coordenada de referência
geoMun.crs

# Extraindo a área - CUIDADO AINDA NÃO CONVERTI
geoMun['AREA_graus'] = geoMun.geometry.area

# Converter para UTM - PSEUDO MERCATOR - Cuidado com deformação
geoMun = geoMun.to_crs('epsg:3857')

# Extraindo a área - CUIDADO AINDA NÃO CONVERTI
geoMun['AREA_km2Novo'] = geoMun.geometry.area/(10**6)

# Converter para WGS84
geoMun = geoMun.to_crs('epsg:4326')

# Extraindo o centroide
geoMun['centroid'] = geoMun.centroid

# Extraindo as bordas - contorno 
geoMun['boundary'] = geoMun.boundary

# Extraindo limites 
geoMun.geometry[0].bounds

# Criando um ponto e transformando em um geopandas
# Objeto shapely
pontoQualquer = Point(-27, -49)

# Para geopandas
pontoQualquer = gpd.GeoSeries(pontoQualquer, crs=4326)

# Calculando distância entre pontoQualquer e centroid das cidades
geoMun['dist'] = [float(pontoQualquer.distance(centroid)) / 1000 for centroid in geoMun.centroid]

# Abrindo um arquivo com coordenadas
stationPath = r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\projeto02\inputs\Monitoramento_QAr_BR_latlon_2024.csv"

# Abrindo com pandas
stations = pd.read_csv(stationPath)

# Transformando para geopandas
gdf = gpd.GeoDataFrame(stations,
                       geometry=gpd.points_from_xy(
                                stations.LONGITUDE, stations.LATITUDE), 
                             crs="EPSG:4326" ) 

# Plotando na figura
fig, ax = plt.subplots()
geoMun.boundary.plot(ax=ax,color='gray', linewidth = 0.2)
gdf.plot(ax=ax)

# Plot usando folium 
gdf.geometry.explore()


# Buffer ao redor das estações
gdf['buffer'] = gdf.to_crs('epsg:3857').buffer(3000).to_crs('epsg:4236')

# área total monitorada
areaMonitorada = gdf['buffer'].to_crs('epsg:3857').unary_union.area/(10**6)

# área do BR
areaBR = geoMun.AREA_km2Novo.sum()

# Porcentagem monitorada
porcentagemMonitorada = (areaMonitorada/areaBR)*100
print(porcentagemMonitorada)

# Unindo geometrias
geoUnion = gpd.sjoin(geoMun,gdf,how='inner')

# Figura com mapa de fundo
ax = gdf.to_crs('epsg:3857').plot(column=gdf['ESTADO'],figsize=(10, 10), alpha=0.5, edgecolor="k")
cx.add_basemap(ax, source=cx.providers.Esri.WorldPhysical)


#%% Análise usando um raster

#Caminho para o arquivo do mapbiomas
mapBiomasPath = r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\projeto02\inputs\mapbiomas_10m_collection2_integration_v1-classification_2023 (2).tif"

# Abrindo o arquivo utilizando o rasterio
src = rio.open(mapBiomasPath)

# Extraindo coordenadas dos pontos para uma lista
gdfUnique = gdf.geometry.unique()
coord_list = [(x,y) for x, y in zip(gdf.geometry.x, gdf.geometry.y)]

# Amonstrando os pontos no raster do mapbiomas
gdf['mapbiomas'] = [x[0] for x in src.sample(coord_list)]

# Contagem de estações por uso do solo
contaUso = gdf.groupby(['mapbiomas']).count()

# Gráfico de barras com o uso do solo onde as estações estão instaladas
fig, ax = plt.subplots()
ax.bar(contaUso.index,contaUso.ESTADO)


# Recortando para uma cidade 
import rasterio.mask
with rio.open(mapBiomasPath) as src:
    out_image, out_transform = rasterio.mask.mask(src,
                                             geoMun[geoMun.NM_MUN=='Florianópolis'].geometry,
                                             crop=True)

# Cuidado com o tamanho da figura
fig,ax = plt.subplots()
ax.pcolor(out_image[0,:,:])


with rio.open(mapBiomasPath) as src:
    out_image, out_transform = rasterio.mask.mask(src,
                                             [gdf.iloc[0,:].buffer],
                                             crop=True)


top,height, width = out_image.shape #Find the height and width of the array

import numpy as np
#Two arrays with the same shape as the input array/raster, where each value is the x or y index of that cell
cols, rows = np.meshgrid(np.arange(width), np.arange(height)) 

# Extraindo coordenadas
xs, ys = rasterio.transform.xy(out_transform, rows, cols) 

# Cuidado com o tamanho da figura
fig,ax = plt.subplots()
ax.pcolor(xs.reshape(cols.shape),ys.reshape(cols.shape),out_image[0,:,:])


gdfTarget = gdf.to_crs('epsg:4326')[gdf.index==0]

# Figura com mapa de fundo
ax = gdfTarget.plot(figsize=(10, 10), alpha=0.5, edgecolor="k")
plt.pcolor(xs.reshape(cols.shape),ys.reshape(cols.shape),out_image[0,:,:],alpha=0.2)
cx.add_basemap(ax, source=cx.providers.Esri.WorldPhysical)

