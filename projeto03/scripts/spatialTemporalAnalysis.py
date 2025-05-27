# -*- coding: utf-8 -*-
"""
Created on Tue May 27 15:36:28 2025

@author: Leonardo.Hoinaski
"""

# pip install netCDF4 xarray
# Ainda não funciona XARRAY
#import xarray as xr
import netCDF4 as nc
import matplotlib.pyplot as plt
import geopandas as gpd

# Abrindo arquivo netCDF
data = nc.Dataset(r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\projeto03\inputs\MERRA2_100.tavgM_2d_aer_Nx.198001.nc4")

# Analisando os dados dentro de data
print(data)

# Extraindo os dados de SO2SMASS
so2 = data['SO2SMASS'][:]
print(data['SO2SMASS'])
print(so2)

# Extraindo latitudes e longitudes
lon = data['lon'][:]
lat = data['lat'][:]

# Abrindo shape do Brasil
# Caminho para o arquivo com o shapefile dos municípios
munPath = r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\projeto02\inputs\BR_Municipios_2024\BR_Municipios_2024.shp"

# Abrindo o arquivo shapefile
geoMun = gpd.read_file(munPath)

fig, ax = plt.subplots()
ax.pcolor(lon,lat,so2[0,:,:])
geoMun.boundary.plot(ax=ax)