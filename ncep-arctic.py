import numpy as np
from netCDF4 import Dataset
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import time
from PIL import Image
from math import cos, sin, tan, pi, radians
import cv2

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os.path

from decouple import config
import dropbox

putOnDropbox = False
auto = True
monthLengths = [31,28,31,30,31,30,31,31,30,31,30,31]

class RegionCode: 		# Region codes used in CryoSat auxiliary data
	cab = 1
	beaufort = 2
	chukchi = 3
	ess = 4
	laptev = 5
	kara = 6
	barents = 7
	greenland = 8
	baffin = 9
	stlawrence = 10
	hudson = 11
	caa = 12
	bering = 13
	okhotsk = 14
	
def downloadLatestFiles():
	filename = 'https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis.dailyavgs/pressure/air.2024.nc'
	localfilename = 'air.2024.nc'
	file_object = requests.get(filename) 
	with open(localfilename, 'wb') as local_file:
		local_file.write(file_object.content)
	print('downloaded', filename)
	
	filename = 'https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis.dailyavgs/surface/air.sig995.2024.nc'
	localfilename = 'air.sig995.2024.nc'
	file_object = requests.get(filename) 
	with open(localfilename, 'wb') as local_file:
		local_file.write(file_object.content)
	print('downloaded', filename)

def plotLine(ax, lines, dates, idx, label, color, linewidth=1):
	line = lines[idx].split(",")		
	
	row =  np.array([i.lstrip() for i in np.array(line[1:366])])
	padded = np.pad(row, (0, 365 - row.shape[0]), 'constant', constant_values=(np.nan,))
	paddedfloat = padded.astype(float)
	ax.plot(dates, paddedfloat, label=label, color=color, linewidth=linewidth);	

def plotTemperature(data, ax, ymin, ymax, name):
	print('inside plotTemperature', name, ymin, ymax)
	lines = np.array(data[1:])#[1:]
	print(lines.shape)
	
	matrix = np.array([np.pad(i.lstrip().split(","), (0,366 - len(i.lstrip().split(","))), 'constant', constant_values=(np.nan,)) for i in lines]).astype(float)
	matrix = matrix[:,1:]
	print(matrix.shape)	
			
	dates = np.arange(1,366)
	baseline = np.sum(matrix[1:30],axis=0)/30
	tens = np.sum(matrix[31:43],axis=0)/12

	plotLine(ax, lines, dates, 0, '_1979', (0.99,0.99,0.99));
	plotLine(ax, lines, dates, 1, '_1980', (0.99,0.99,0.99));
	plotLine(ax, lines, dates, 2, '_1981', (0.98,0.98,0.98));
	plotLine(ax, lines, dates, 3, '_1982', (0.97,0.97,0.97));
	plotLine(ax, lines, dates, 4, '_1983', (0.97,0.97,0.97));
	plotLine(ax, lines, dates, 5, '_1984', (0.96,0.96,0.96));
	plotLine(ax, lines, dates, 6, '_1985', (0.95,0.95,0.95));
	plotLine(ax, lines, dates, 7, '_1986', (0.95,0.95,0.95));
	plotLine(ax, lines, dates, 8, '_1987', (0.94,0.94,0.94));
	plotLine(ax, lines, dates, 9, '_1988', (0.93,0.93,0.93));
	plotLine(ax, lines, dates, 10, '_1989', (0.93,0.93,0.93));
	plotLine(ax, lines, dates, 11, '_1990', (0.92,0.92,0.92));
	plotLine(ax, lines, dates, 12, '_1991', (0.91,0.91,0.91));
	plotLine(ax, lines, dates, 13, '_1992', (0.91,0.91,0.91));
	plotLine(ax, lines, dates, 14, '_1993', (0.90,0.90,0.90));
	plotLine(ax, lines, dates, 15, '_1994', (0.89,0.89,0.89));
	plotLine(ax, lines, dates, 16, '_1995', (0.89,0.89,0.89));
	plotLine(ax, lines, dates, 17, '_1996', (0.88,0.88,0.88));
	plotLine(ax, lines, dates, 18, '_1997', (0.87,0.87,0.87));
	plotLine(ax, lines, dates, 19, '_1998', (0.87,0.87,0.87));
	plotLine(ax, lines, dates, 20, '_1999', (0.86,0.86,0.86));
	plotLine(ax, lines, dates, 21, '_2000', (0.85,0.85,0.85));
	plotLine(ax, lines, dates, 22, '_2001', (0.85,0.85,0.85));
	plotLine(ax, lines, dates, 23, '_2002', (0.84,0.84,0.84));
	plotLine(ax, lines, dates, 24, '_2003', (0.83,0.83,0.83));
	plotLine(ax, lines, dates, 25, '_2004', (0.83,0.83,0.83));
	plotLine(ax, lines, dates, 26, '_2005', (0.82,0.82,0.82));
	plotLine(ax, lines, dates, 27, '_2006', (0.81,0.81,0.81));
	plotLine(ax, lines, dates, 28, '_2007', (0.81,0.81,0.81));
	plotLine(ax, lines, dates, 29, '_2008', (0.80,0.80,0.80));
	plotLine(ax, lines, dates, 30, '_2009', (0.79,0.79,0.79));
	plotLine(ax, lines, dates, 31, '_2010', (0.79,0.79,0.79));
	plotLine(ax, lines, dates, 32, '_2011', (0.78,0.78,0.78));
	plotLine(ax, lines, dates, 33, '_2012', (0.77,0.77,0.77));
	plotLine(ax, lines, dates, 34, '_2013', (0.77,0.77,0.77));
	plotLine(ax, lines, dates, 35, '_2014', (0.76,0.76,0.76));
	plotLine(ax, lines, dates, 36, '_2015', (0.75,0.75,0.75));	
	plotLine(ax, lines, dates, 37, '_2016', (0.75,0.75,0.75));
	plotLine(ax, lines, dates, 38, '_2017', (0.74,0.74,0.74));
	plotLine(ax, lines, dates, 39, '_2018', (0.73,0.73,0.73));
	plotLine(ax, lines, dates, 40, '_2019', (0.73,0.73,0.73));
	plotLine(ax, lines, dates, 41, '_2020', (0.72,0.72,0.72));
	plotLine(ax, lines, dates, 42, '_2021', (0.71,0.71,0.71));
	plotLine(ax, lines, dates, 43, '_2022', (0.71,0.71,0.71));
	ax.plot(dates, baseline, label='1980-2009 avg', linestyle='dashed', color=(0,0,0));
	ax.plot(dates, tens, label='2010-2022 avg',  color=(0,0,0));
	plotLine(ax, lines, dates, 44, '2023', (1.0,0.75,0));
	plotLine(ax, lines, dates, 45, '2024', (1.0,0.0,0.0), linewidth=2);
	print('b')
	
	ax.set_ylabel("Temperature (°C)")
	ax.set_title(name)
	ax.legend(ncol=1, loc=8, prop={'size': 8})#, bbox_to_anchor=(0.75,1))
	ax.axis([1, 366, ymin, ymax])
	ax.grid(True);
	
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	ax.set_xticks([1,32,60,91,121,152,182,213,244,274,305,335,366], ['', '', '', '', '', '', '', '', '', '', '', '', ''])
	ax.xaxis.set_minor_locator(ticker.FixedLocator([16.5,46,75.4,106,136.5,167,197.5,228.5,259,289.5,320,350.5]))
	ax.xaxis.set_minor_formatter(ticker.FixedFormatter(months))
	ax.tick_params(which='minor', length=0)	

def printRegionalTemperature(data, ax, col, ymin, ymax, name, north=True):
	print('inside printRegionalTemperature', name, ymin, ymax)
	regional = data[1:,col]
	regional = np.array([i.lstrip() for i in regional]).astype(float)
	padded = np.pad(regional, (0, 365*46 - regional.shape[0]), 'constant', constant_values=(np.nan,))
	matrix = padded.reshape((46,365))
	dates = np.arange(1,366)
	eighties = np.sum(matrix[1:10,:],axis=0)/10
	nineties = np.sum(matrix[11:20,:],axis=0)/10
	noughties = np.sum(matrix[21:30,:],axis=0)/10
	baseline = np.sum(matrix[1:30,:],axis=0)/30
	tens = np.sum(matrix[31:43,:],axis=0)/12	
	ax.plot(dates, matrix[0,:], label='_1979', color=(0.99,0.99,0.99));
	ax.plot(dates, matrix[1,:], label='_1980', color=(0.99,0.99,0.99));
	ax.plot(dates, matrix[2,:], label='_1981', color=(0.98,0.98,0.98));
	ax.plot(dates, matrix[3,:], label='_1982', color=(0.97,0.97,0.97));
	ax.plot(dates, matrix[4,:], label='_1983', color=(0.97,0.97,0.97));
	ax.plot(dates, matrix[5,:], label='_1984', color=(0.96,0.96,0.96));
	ax.plot(dates, matrix[6,:], label='_1985', color=(0.95,0.95,0.95));
	ax.plot(dates, matrix[7,:], label='_1986', color=(0.95,0.95,0.95));
	ax.plot(dates, matrix[8,:], label='_1987', color=(0.94,0.94,0.94));
	ax.plot(dates, matrix[9,:], label='_1988', color=(0.93,0.93,0.93));
	ax.plot(dates, matrix[10,:], label='_1989', color=(0.93,0.93,0.93));
	ax.plot(dates, matrix[11,:], label='_1990', color=(0.92,0.92,0.92));
	ax.plot(dates, matrix[12,:], label='_1991', color=(0.91,0.91,0.91));
	ax.plot(dates, matrix[13,:], label='_1992', color=(0.91,0.91,0.91));
	ax.plot(dates, matrix[14,:], label='_1993', color=(0.90,0.90,0.90));
	ax.plot(dates, matrix[15,:], label='_1994', color=(0.89,0.89,0.89));
	ax.plot(dates, matrix[16,:], label='_1995', color=(0.89,0.89,0.89));
	ax.plot(dates, matrix[17,:], label='_1996', color=(0.88,0.88,0.88));
	ax.plot(dates, matrix[18,:], label='_1997', color=(0.87,0.87,0.87));
	ax.plot(dates, matrix[19,:], label='_1998', color=(0.87,0.87,0.87));
	ax.plot(dates, matrix[20,:], label='_1999', color=(0.86,0.86,0.86));
	ax.plot(dates, matrix[21,:], label='_2000', color=(0.85,0.85,0.85));
	ax.plot(dates, matrix[22,:], label='_2001', color=(0.85,0.85,0.85));
	ax.plot(dates, matrix[23,:], label='_2002', color=(0.84,0.84,0.84));
	ax.plot(dates, matrix[24,:], label='_2003', color=(0.83,0.83,0.83));
	ax.plot(dates, matrix[25,:], label='_2004', color=(0.83,0.83,0.83));
	ax.plot(dates, matrix[26,:], label='_2005', color=(0.82,0.82,0.82));
	ax.plot(dates, matrix[27,:], label='_2006', color=(0.81,0.81,0.81));
	ax.plot(dates, matrix[28,:], label='_2007', color=(0.81,0.81,0.81));
	ax.plot(dates, matrix[29,:], label='_2008', color=(0.80,0.80,0.80));
	ax.plot(dates, matrix[30,:], label='_2009', color=(0.79,0.79,0.79));
	ax.plot(dates, matrix[31,:], label='_2010', color=(0.79,0.79,0.79));
	ax.plot(dates, matrix[32,:], label='_2011', color=(0.78,0.78,0.78));
	ax.plot(dates, matrix[33,:], label='_2012', color=(0.77,0.77,0.77));
	ax.plot(dates, matrix[34,:], label='_2013', color=(0.77,0.77,0.77));
	ax.plot(dates, matrix[35,:], label='_2014', color=(0.76,0.76,0.76));
	ax.plot(dates, matrix[36,:], label='_2015', color=(0.75,0.75,0.75));
	ax.plot(dates, matrix[37,:], label='_2016', color=(0.75,0.75,0.75));
	ax.plot(dates, matrix[38,:], label='_2017', color=(0.74,0.74,0.74));
	ax.plot(dates, matrix[39,:], label='_2018', color=(0.73,0.73,0.73));
	ax.plot(dates, matrix[40,:], label='_2019', color=(0.73,0.73,0.73));
	ax.plot(dates, matrix[41,:], label='_2020', color=(0.72,0.72,0.72));	
	ax.plot(dates, matrix[42,:], label='_2021', color=(0.71,0.71,0.71));
	ax.plot(dates, matrix[43,:], label='_2022', color=(0.71,0.71,0.71));
	ax.plot(dates, baseline, label='1980-2009 avg', linestyle='dashed', color=(0,0,0));
	ax.plot(dates, tens, label='2010-2022 avg',  color=(0,0,0));
	ax.plot(dates, matrix[44,:], label='2023', color=(1,0.75,0));	
	ax.plot(dates, matrix[45,:], label='2024', color=(1.0,0,0), linewidth=2);
	ax.set_ylabel("Temperature (°C)")
	ax.set_title(name)
	ax.legend(ncol=1, loc=(8 if north else 3), prop={'size': 8})
	ax.axis([1, 366, ymin, ymax])
	ax.grid(True);
	
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	ax.set_xticks([1,32,60,91,121,152,182,213,244,274,305,335,366], ['', '', '', '', '', '', '', '', '', '', '', '', ''])
	ax.xaxis.set_minor_locator(ticker.FixedLocator([16.5,46,75.4,106,136.5,167,197.5,228.5,259,289.5,320,350.5]))
	ax.xaxis.set_minor_formatter(ticker.FixedFormatter(months))
	ax.tick_params(which='minor', length=0)	
	
def createPlots():
	print("inside create plots")
	csvFileName = 'data/ncep-arctic-ocean-temperature-925-mb-1979-to-2023.csv'
	uploadToDropbox([csvFileName])
	with open(csvFileName, 'r') as f:
		data = f.readlines()
	fig, axs = plt.subplots(figsize=(8, 5))
	label = "NCEP reanalysis 925 mb temperature over Arctic Ocean (°C) 1979-2024"
	plotTemperature(data, axs, -30, 8.2, label)
	filename = 'ncep-reanalysis-temperature-925-mb-over-arctic-ocean.png'
	fig.savefig(filename)

	csvFileName = 'data/ncep-arctic-ocean-surface-temperature-1979-to-2023.csv'
	uploadToDropbox([csvFileName])
	with open(csvFileName, 'r') as f:
		data = f.readlines()
	
	fig, axs = plt.subplots(figsize=(8, 5))	
	plotTemperature(data, axs, -35, 5, "NCEP reanalysis surface temperature over Arctic Ocean (°C) 1979-2024")
	filename = 'ncep-reanalysis-surface-temperature-over-arctic-ocean.png'
	fig.savefig(filename)

def saveRegionalPlot(col, ymin, ymax, data, name, filename, north = True):
	print('inside saveRegionalPlot', name)
	fig, axs = plt.subplots(figsize=(8, 5))
	printRegionalTemperature(data, axs, col, ymin, ymax, name, north)
	fig.savefig(filename)
	
def plotRegionalGraphs925mb(filename):
	data = np.loadtxt(filename, delimiter=",", dtype=str)

	saveRegionalPlot(4, -40, 20, data, "Beaufort Sea NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-beaufort-temperature.png")
	saveRegionalPlot(5, -40, 20, data, "Chukchi Sea NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-chukchi-temperature.png")
	saveRegionalPlot(6, -35, 20, data, "East Siberian Sea NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-ess-temperature.png")
	saveRegionalPlot(7, -35, 20, data, "Laptev Sea NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-laptev-temperature.png")
	saveRegionalPlot(8, -35, 20, data, "Kara Sea NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-kara-temperature.png")
	saveRegionalPlot(9, -25, 20, data, "Barents Sea NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-barents-temperature.png")
	saveRegionalPlot(10, -20, 15, data, "Greenland Sea NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-greenland-temperature.png")
	saveRegionalPlot(11, -35, 10, data, "Central Arctic Basin NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-cab-temperature.png")
	saveRegionalPlot(12, -40, 15, data, "Canadian Arctic Archipelago NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-caa-temperature.png")
	saveRegionalPlot(13, -25, 15, data, "Baffin Bay NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-baffin-temperature.png")
	saveRegionalPlot(14, -35, 20, data, "Hudson Bay NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-hudson-temperature.png")
	saveRegionalPlot(3, -20, 15, data, "Bering Sea NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-bering-temperature.png")
	saveRegionalPlot(2, -25, 20, data, "Sea of Okhotsk NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-okhotsk-temperature.png")

def plotRegionalGraphs925mbSouth(filename):
	data = np.loadtxt(filename, delimiter=",", dtype=str)

	saveRegionalPlot(2, -30, 2, data, "Weddell Sea NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-weddell-temperature.png", False)
	saveRegionalPlot(3, -40, 3, data, "Bellingshausen-Amundsen Sea NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-bellam-temperature.png", False)
	saveRegionalPlot(4, -35, 2, data, "Ross Sea NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-ross-temperature.png", False)
	saveRegionalPlot(5, -35, 5, data, "West Pacific southern ocean sector NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-pacific-temperature.png", False)
	saveRegionalPlot(6, -30, 2, data, "Indian southern ocean sector NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-indian-temperature.png", False)
	saveRegionalPlot(7, -30, 2, data, "Southern ocean NCEP reanalysis 925mb temperature 1979-2024", "ncep-925mb-southern-temperature.png", False)
	
def plotRegionalGraphsSurface(filename):
	data = np.loadtxt(filename, delimiter=",", dtype=str)

	saveRegionalPlot(4, -40, 12, data, "Beaufort Sea NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-beaufort-temperature.png")
	saveRegionalPlot(5, -40, 12, data, "Chukchi Sea NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-chukchi-temperature.png")
	saveRegionalPlot(6, -40, 12, data, "East Siberian Sea NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-ess-temperature.png")
	saveRegionalPlot(7, -40, 14, data, "Laptev Sea NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-laptev-temperature.png")
	saveRegionalPlot(8, -40, 12, data, "Kara Sea NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-kara-temperature.png")
	saveRegionalPlot(9, -25, 12, data, "Barents Sea NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-barents-temperature.png")
	saveRegionalPlot(10, -15, 10, data, "Greenland Sea NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-greenland-temperature.png")
	saveRegionalPlot(11, -40, 5, data, "Central Arctic Basin NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-cab-temperature.png")
	saveRegionalPlot(12, -40, 13, data, "Canadian Arctic Archipelago NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-caa-temperature.png")
	saveRegionalPlot(13, -25, 12, data, "Baffin Bay NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-baffin-temperature.png")
	saveRegionalPlot(14, -40, 15, data, "Hudson Bay NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-hudson-temperature.png")
	saveRegionalPlot(3, -15, 13, data, "Bering Sea NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-bering-temperature.png")
	saveRegionalPlot(2, -25, 18, data, "Sea of Okhotsk NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-okhotsk-temperature.png")

def plotRegionalGraphsSurfaceSouth(filename):
	data = np.loadtxt(filename, delimiter=",", dtype=str)

	saveRegionalPlot(2, -40, 2, data, "Weddell Sea NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-weddell-temperature.png", False)
	saveRegionalPlot(3, -45, 5, data, "Bellingshausen-Amundsen Sea NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-bellam-temperature.png", False)
	saveRegionalPlot(4, -40, 2, data, "Ross Sea NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-ross-temperature.png", False)
	saveRegionalPlot(5, -40, 5, data, "West Pacific southern ocean sector NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-pacific-temperature.png", False)
	saveRegionalPlot(6, -40, 2, data, "Indian southern ocean sector NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-indian-temperature.png", False)
	saveRegionalPlot(7, -30, 2, data, "Southern ocean NCEP reanalysis surface air temperature 1979-2024", "ncep-surface-southern-temperature.png", False)

def appendToRegionalCsv(filename, north = True):
	
	if north:
		alldata = [allyear,allday,allokh,allber,allbea,allchu,alless,alllap,allkar,allbar,allgre,allcab,allcaa,allbaf,allhud]
	else:
		alldata = [allyear,allday,allwed,allbel,allros,allpac,allind,alltot]
	alldata = np.transpose(alldata)
	alldata = np.round(alldata, decimals=3)
	
	if north:
		format = "%.0f,  %3.0f,  %7.3f,  %7.3f,  %7.3f,  %7.3f,  %7.3f,  %7.3f,  %7.3f,  %7.3f,  %7.3f,  %7.3f, %7.3f,  %7.3f,  %7.3f" #'%.3f'  fmt="%-6s", delimiter=";"
	else:
		format = "%.0f,  %3.0f,  %7.3f,  %7.3f,  %7.3f,  %7.3f,  %7.3f,  %7.3f"
	
	appendToCsvFile(filename, alldata, format)

def loadYear925(year):
	filename = "air." + str(year) + ".nc"
	f = Dataset(filename, 'r', format="NETCDF4")	
	# read sea ice concentration, thickness and thickness uncertainty	
	data = f.variables['air'][:]#.squeeze()
	print(data.shape)	
	days = data.shape[0]
	arctictempsforyear = [year]
		
	for day in range(days): # days
		if(day == 59 and year%4 == 0): # skip leap years
			continue
		slice = data[day][1] #data[(73*day):(73*(day+1))][:]
		arctictemp = getArcticTemperature(slice)
		allyear.append(year)
		allday.append(day+1)
		arctictempsforyear.append(arctictemp)
		print(year,day,arctictemp)
	return arctictempsforyear

def loadYear(year):
	filename = "air.sig995." + str(year) + ".nc" #"airsurface" + str(year) + ".csv"
	f = Dataset(filename, 'r', format="NETCDF4")	
	data = f.variables['air'][:]#.squeeze()
	days = data.shape[0]
	
	print('days', days)
	arctictempsforyear = [year]
	for day in range(days): # days
		if(day == 59 and year%4 == 0): # skip leap years
			continue
		slice = data[day] #data[(73*day):(73*(day+1))][:]
		arctictemp = getArcticTemperature(slice)
		allyear.append(year)
		allday.append(day+1)
		arctictempsforyear.append(arctictemp)
		print(year,day,arctictemp)
	return arctictempsforyear


def getArcticTemperature(data):
	northpole = data[0]
	globalaveragetemp = 0
	arctictemp = 0
	weightdenominatorarctic = 0
	weightdenominator = 0
	numberofrows = data.shape[0]

	if(useWeights):
		oceanweights = np.loadtxt("coast-weights-" + ("" if north else "south-") + "safe.csv", delimiter=",", dtype=str)
	if regional:
		if north:
			regionweights = np.loadtxt("region-values-safe.csv", delimiter=",", dtype=str)
			tcab = dcab = tcaa = dcaa = tbea = dbea = tchu = dchu = tber = dber = tokh = dokh = tess = dess = tlap = dlap = tkar = dkar = tbar = dbar = tgre = dgre = tbaf = dbaf = thud = dhud = 0
		else:
			twed = dwed = tbel = dbel = tros = dros = tpac = dpac = tind = dind = ttot = dtot = 0
	if(data[0][0] != data[0][1] or data[0][0] != data[0][2]):
		print('hela!!!')
	if(data[numberofrows-1][0] != data[numberofrows-1][1] or data[numberofrows-1][0] != data[numberofrows-1][2]):
		print('helab!!!')	
	
	for i in range(numberofrows):
		row = data[i] if north else data[72-i]
		latitude = 90 - 2.5*i
		latituderadians = radians(latitude)
		weight = cos(latituderadians) if i > 0 else tan(radians(0.625))/2.0
		n = row.shape[0]
		temp = (row.sum())/n-273.15
		globalaveragetemp += temp*weight
		weightdenominator += weight
		if north and regional and latitude >= 50:
			latituderegionweights = regionweights[i,:]
			latituderegionweights = np.array([ii.lstrip() for ii in latituderegionweights]).astype(int)	
		if useWeights and ((north and latitude >= 50) or (not north and latitude >= 67.5)):
			latitudeoceanweights = oceanweights[i,:]
			latitudeoceanweights = np.array([ii.lstrip() for ii in latitudeoceanweights]).astype(float)	
		for j in range(n):
			obs = row[j]-273.15
			longitude = 2.5 * j
			if(north and not useWeights and isArcticOcean(latitude, longitude)):
				arctictemp += obs*weight
				weightdenominatorarctic += weight
			elif(useWeights and ((north and latitude >= 50) or (not north and latitude >= 67.5))):
				tileWeight = latitudeoceanweights[j]
				allweight = weight*tileWeight
				temp = obs*allweight
				if (north and isArcticOceanBis(latitude, longitude)) or (not north and latitude >= 67.5):
					arctictemp += temp
					weightdenominatorarctic += allweight
				if regional:
					if north:
						regionweight = latituderegionweights[j]
						if regionweight == RegionCode.cab:
							tcab += temp
							dcab += allweight
						elif regionweight == RegionCode.caa:										
							tcaa += temp
							dcaa += allweight
						elif regionweight == RegionCode.beaufort:
							tbea += temp
							dbea += allweight
						elif regionweight == RegionCode.chukchi:
							tchu += temp
							dchu += allweight
						elif regionweight == RegionCode.bering:
							tber += temp
							dber += allweight
						elif regionweight == RegionCode.okhotsk:
							tokh += temp
							dokh += allweight
						elif regionweight == RegionCode.ess:										
							tess += temp
							dess += allweight
						elif regionweight == RegionCode.laptev:										
							tlap += temp
							dlap += allweight
						elif regionweight == RegionCode.kara:										
							tkar += temp
							dkar += allweight
						elif regionweight == RegionCode.barents:										
							tbar += temp
							dbar += allweight
						elif regionweight == RegionCode.greenland:										
							tgre += temp
							dgre += allweight
						elif regionweight == RegionCode.baffin:										
							tbaf += temp
							dbaf += allweight
						elif regionweight == RegionCode.hudson:										
							thud += temp
							dhud += allweight
					else:
						wwed,wbel,wros,wpac,wind = getSouthRegionWeights(latitude, longitude)
						if wwed > 0:
							twed += wwed*temp
							dwed += wwed*allweight
							#wwwed += wwed*allweight
						if wbel > 0:
							tbel += wbel*temp
							dbel += wbel*allweight
							#wwbel += wbel*allweight
						if wros > 0:
							tros += wros*temp
							dros += wros*allweight
							#wwros += wros*allweight
						if wpac > 0:
							tpac += wpac*temp
							dpac += wpac*allweight
							#wwpac += wpac*allweight
						if wind > 0:
							tind += wind*temp
							dind += wind*allweight
							#wwind += wind*allweight
						ttot += temp
						dtot += allweight
		
	globalaveragetemp /= weightdenominator
	arctictemp /= weightdenominatorarctic
	if regional:
		if north:
			tcab /= dcab
			tcaa /= dcaa
			tbea /= dbea
			tchu /= dchu
			tber /= dber
			tokh /= dokh
			tess /= dess
			tlap /= dlap
			tkar /= dkar
			tbar /= dbar
			tgre /= dgre
			tbaf /= dbaf
			thud /= dhud
			
			allcab.append(tcab)
			allcaa.append(tcaa)
			allbea.append(tbea)
			allchu.append(tchu)
			allber.append(tber)
			allokh.append(tokh)
			alless.append(tess)
			alllap.append(tlap)
			allkar.append(tkar)
			allbar.append(tbar)
			allgre.append(tgre)
			allbaf.append(tbaf)
			allhud.append(thud)
		else:			
			twed /= dwed
			tbel /= dbel
			tros /= dros
			tpac /= dpac
			tind /= dind
			ttot /= dtot			
			
			allwed.append(twed)
			allbel.append(tbel)
			allros.append(tros)
			allpac.append(tpac)
			allind.append(tind)
			alltot.append(ttot)		
	return arctictemp
	
def getSouthRegionWeights(lat, long):
	wwed = wbel = wros = wpac = wind = 0
	if long < 20 or long >= 297.5:
		wwed = 1
	elif long == 20:
		wwed = 0.5
		wind = 0.5
	elif long > 20 and long < 90:
		wind = 1
	elif long == 90:
		wind = 0.5
		wpac = 0.5
	elif long > 90 and long < 160:
		wpac = 1
	elif long == 90:
		wpac = 0.5
		wros = 0.5
	elif long > 160 and long < 230:
		wros = 1
	elif long == 160:
		wros = 0.5
		wbel = 0.5
	elif long > 230 and long < 297.5:
		wbel = 1

	return wwed, wbel, wros, wpac, wind
	
def isArcticOcean(lat, long):
	if(lat >= 85):
		return True
	if(lat == 82.5):
		return (long <= 360-83) or (long >= 360-61 and long <= 360-50) or (long >= 360-22)
	if(lat == 80):
		return (long <= 360-100) or (long >= 360-15)
	if(lat == 77.5):
		return (long >= 48.6 and long <= 360-124.4) #or long >= 360-17.6
	if(lat == 75):
		return (long >= 48.6 and long <= 86) or (long >= 113 and long <= 360-124) or (long >= 360-79 and long <= 360-59)
	if(lat == 72.5):
		return (long >= 48.6 and long <= 68.54) or (long >= 129.54 and long <= 360-125.8) or (long >= 360-75.2 and long <= 360-56.2)
	if(lat == 70):
		return (long >= 48.6 and long <= 66.8) or (long >= 160.1 and long <= 360-162.9) or (long >= 360-142.5 and long <= 360-117.6) or (long >= 360-67.1 and long <= 360-55.2)
	if(lat == 67.5):
		return (long >= 360-174.6 and long <= 360-163.8) or (long >= 360-81.3 and long <= 360-72.8) or (long >= 360-63.3 and long <= 360-53.9)
	else:
		return False

def isArcticOceanBis(lat, long):
	if(lat >= 80):
		return True
	elif(lat >= 67.5):
		return (long >= 48.6 and long <= 315)
	else:
		return False


ccab = (174,228,153)
cbea = (137,36,138)
cchu = (63,211,73)
cber = (46,33,208)
cokh = (251,209,39)
cess = (121,48,75)
clap = (152,222,248)
ckar = (26,79,71)
cbar = (173,212,31)
cgre = (180,29,72)
cbaf = (103,158,100)
ccaa = (46,92,174)
chud = (248,175,226)
#north pole 389,638
#image size 771,1162

def swap(color):
	return (color[2], color[1], color[0])

def getRegionWeights():
	im = Image.open('region-mask-safe.png') #'2021-arctic-region-mask3.png') #'region-mask-safe.png') #'2021-arctic-region-mask3.png')
	imdata = im.getdata();
	imdatalist = list(imdata);
	imwidth, imheight = im.size
	pixelmatrix = [imdatalist[i * imwidth:(i + 1) * imwidth] for i in range(imheight)]

	cvim = cv2.imread('region-mask-safe.png')#'2021-arctic-region-mask3.png') #region-mask-safe.png
	polerow = 389
	polecol = 638
	factor = 10.8
	#258
	#380 pixels for 35.2 degrees, so pixels = 10.8 * degrees
	print(pixelmatrix[polerow][polecol])

	weights = np.loadtxt("region-values-safe.csv", delimiter=",", dtype=str)

	latitude = 92.5
	values = []
	i = 0
	while latitude > 50:
		latitudeRegions = weights[i,:]
		latitudeRegions = np.array([ii.lstrip() for ii in latitudeRegions]).astype(int)
			
		i += 1
		valueslat=[]
		latitude -= 2.5
		longitude = 0
		print('latitude',latitude)
		j = 0
		while longitude < 360:
			latitudeRegion = latitudeRegions[j]
			j += 1
			radius = factor*(90 - latitude)
			
			centerx = polerow + int(radius*sin(radians(longitude)))
			centery = polecol + int(radius*cos(radians(longitude)))
			
			latitudemin = latitude - 1.25
			latitudemax = latitude + (1.25 if latitude < 90 else 0)
			longitudemin = longitude - 1.25 + 45
			longitudemax = longitude + 1.25+ 45
			
			radiusmin = factor*(90 - latitudemax)
			radiusmax = factor*(90 - latitudemin)
			
			corner1x = polerow + int(radiusmin*sin(radians(longitudemin)))
			corner1y = polecol + int(radiusmin*cos(radians(longitudemin)))
			corner2x = polerow + int(radiusmax*sin(radians(longitudemin)))
			corner2y = polecol + int(radiusmax*cos(radians(longitudemin)))
			corner3x = polerow + int(radiusmax*sin(radians(longitudemax)))
			corner3y = polecol + int(radiusmax*cos(radians(longitudemax)))
			corner4x = polerow + int(radiusmin*sin(radians(longitudemax)))
			corner4y = polecol + int(radiusmin*cos(radians(longitudemax)))			
			
			mask = np.zeros((cvim.shape), dtype=np.uint8)
			pts = np.array([[[corner1x,corner1y],[corner2x,corner2y],[corner3x,corner3y],[corner4x,corner4y]]], dtype=np.int32)
			cv2.fillPoly(mask, pts, (255,255,255))
			
			coords = cvim[np.where((mask == (255,255,255)).all(axis=2))]
			pcab = countReg(cvim,coords, ccab)
			pcaa = countReg(cvim,coords, ccaa)
			pbea = countReg(cvim,coords, cbea)
			pchu = countReg(cvim,coords, cchu)
			pess = countReg(cvim,coords, cess)
			plap = countReg(cvim,coords, clap)
			pkar = countReg(cvim,coords, ckar)
			pbar = countReg(cvim,coords, cbar)
			pgre = countReg(cvim,coords, cgre)
			pbaf = countReg(cvim,coords, cbaf)
			phud = countReg(cvim,coords, chud)
			pber = countReg(cvim,coords, cber)
			pokh = countReg(cvim,coords, cokh)
			
			if longitude > 310:
				pess = 0
			if longitude > 285:
				pbea = 0
			if latitude == 50:
				pkar = 0
			
			plist = [pcab,pcaa,pbea,pchu,pess,plap,pkar,pbar,pgre,pbaf,phud,pber,pokh]
			argmax = np.argmax(plist)
			maximum = np.max(plist)
			
			if argmax == 0:
				region = RegionCode.cab
			elif argmax == 1:
				region = RegionCode.caa
			elif argmax == 2:
				region = RegionCode.beaufort
			elif argmax == 3:
				region = RegionCode.chukchi
			elif argmax == 4:
				region = RegionCode.ess
			elif argmax == 5:
				region = RegionCode.laptev
			elif argmax == 6:
				region = RegionCode.kara
			elif argmax == 7:
				region = RegionCode.barents
			elif argmax == 8:
				region = RegionCode.greenland
			elif argmax == 9:
				region = RegionCode.baffin
			elif argmax == 10:
				region = RegionCode.hudson
			elif argmax == 11:
				region = RegionCode.bering
			elif argmax == 12:
				region = RegionCode.okhotsk
			
			if latitudeRegion == RegionCode.cab:
				color = ccab
			elif latitudeRegion == RegionCode.caa:
				color = ccaa
			elif latitudeRegion == RegionCode.beaufort:
				color = cbea
			elif latitudeRegion == RegionCode.chukchi:
				color = cchu
			elif latitudeRegion == RegionCode.bering:
				color = cber
			elif latitudeRegion == RegionCode.okhotsk:
				color = cokh
			elif latitudeRegion == RegionCode.ess:
				color = cess
			elif latitudeRegion == RegionCode.laptev:
				color = clap
			elif latitudeRegion == RegionCode.kara:
				color = ckar
			elif latitudeRegion == RegionCode.barents:
				color = cbar
			elif latitudeRegion == RegionCode.greenland:
				color = cgre
			elif latitudeRegion == RegionCode.baffin:
				color = cbaf
			elif latitudeRegion == RegionCode.hudson:
				color = chud

			if maximum == 0:
				region = 0
			if latitudeRegion > 0:
				mask = np.zeros((cvim.shape), dtype=np.uint8)
				cv2.fillPoly(mask, pts, (255,255,255))
				rows,cols,xx = np.where((mask == (255,255,255)))#.all(axis=2)
				coords = zip(rows,cols)
				for coord in coords:
					coorda = cvim[coord[0]][coord[1]]
					if coorda[0] > 235 and coorda[1] > 235 and coorda[2] > 235:
						cvim[coord[0]][coord[1]] = swap(color)

			valueslat.append(region)
			
			longitude += 2.5
		values.append(valueslat)
	cv2.imwrite('ncep-regions.png', cvim)
		
def countReg(im,coords,pixel2):
	n=0
	for coord in coords:
		if(isClose(coord,pixel2)):
			n+=1
	return n

def isClose(pixel1,pixel2):
	thres = 20
	result = abs(pixel1[0]-pixel2[2])<thres and abs(pixel1[1]-pixel2[1])<thres and abs(pixel1[2]-pixel2[0])<thres
	return result
	
def reset():
	global allbea, allchu, alless, alllap, allkar, allbar, allgre, allbaf, allhud, allcaa, allcab, allber, allokh, alloth, alltotal, allyear, allmonth, allday, allwed, allbel, allros, allpac, allind, alltot
	allbea = []
	allchu = []
	alless = []
	alllap = []
	allkar = []
	allbar = []
	allgre = []
	allbaf = []
	allhud = []
	allcaa = []
	allcab = []
	allber = []
	allokh = []
	alloth = []
	
	allwed = []
	allbel = []
	allros = []
	allpac = []
	allind = []
	alltot = []
	
	alltotal = []
	allyear = []
	allmonth = []
	allday = []
		
def uploadToDropbox(filenames):
	if not putOnDropbox:
		return
	dropbox_access_token = config('DROPBOX_ACCESS_TOKEN')
	app_key = config('APP_KEY')
	app_secret = config('APP_SECRET')
	oauth2_refresh_token = config('OAUTH2_REFRESH_TOKEN')
	client = dropbox.Dropbox(oauth2_access_token=dropbox_access_token,app_key=app_key,app_secret=app_secret,oauth2_refresh_token=oauth2_refresh_token)
	print("[SUCCESS] dropbox account linked")
	
	for computer_path in filenames:
		print("[UPLOADING] {}".format(computer_path))
		dropbox_path= "/" + computer_path
		client.files_upload(open(computer_path, "rb").read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
		print("[UPLOADED] {}".format(computer_path))
		
def get_credentials(SCOPES):
	creds = None
	credentials_filename = "token.json"
	google_drive_credentials = config('GOOGLE_DRIVE_CREDENTIALS')
	with open(credentials_filename, "w") as local_file:
		local_file.write(google_drive_credentials)
	if os.path.exists(credentials_filename):
		print('gonna get credentials from file')
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	if not creds or not creds.valid:
		print('credentials invalid')
		if creds and creds.expired and creds.refresh_token:
			print('credentials try token refresh')
			creds.refresh(Request())
			with open(credentials_filename, 'w') as token:
				token.write(creds.to_json())
	return creds

def replace_file_in_google_drive(file_id,local_path,prefix=''):
	credentials = get_credentials(["https://www.googleapis.com/auth/drive.file"])
	drive_service = build('drive', 'v3', credentials=credentials)

	file_metadata = {'name': local_path}
	media = MediaFileUpload(prefix + local_path, mimetype='image/png')
	file = drive_service.files().update(fileId = file_id, media_body=media).execute()
	print(F'File ID: {file.get("id")}')

def uploadToGoogleDrive():
	replace_file_in_google_drive('1xDe25jOH7PreH2Pckio8zyk7dbVBPrhF', 'ncep-reanalysis-surface-temperature-over-arctic-ocean.png', '../ncep/')
	replace_file_in_google_drive('1i4yiDYMGpqh74H0LcxPhZo4vKlTmuIAE', 'ncep-reanalysis-temperature-925-mb-over-arctic-ocean.png', '../ncep/')	

	replace_file_in_google_drive('1blDkmo3naQ-Mwds6c4PXrdB1rpBjwp0D', 'ncep-surface-southern-temperature.png', '../ncep/')
	replace_file_in_google_drive('1Aid0yRQLKyTTRAGztsNvlkKCDlKoEdpm', 'ncep-surface-weddell-temperature.png', '../ncep/')
	replace_file_in_google_drive('1Uc7F7F5XxW_dXxZF5-AHuQqqdxnVw6SS', 'ncep-surface-bellam-temperature.png', '../ncep/')
	replace_file_in_google_drive('1VPkBB5Kt6l5kSbJHg8EuclQaKTVE9wep', 'ncep-surface-ross-temperature.png', '../ncep/')
	replace_file_in_google_drive('1GRl_J1cqYoVU4Wyv1T_geHFK3DOkPFZO', 'ncep-surface-pacific-temperature.png', '../ncep/')
	replace_file_in_google_drive('15lcvNny6qMv_hID6q5VfHSsLjmSfMTwa', 'ncep-surface-indian-temperature.png', '../ncep/')

	replace_file_in_google_drive('1x70ApJ6tylD1g9fGPx14QBQfOAFjP8AW', 'ncep-925mb-southern-temperature.png', '../ncep/')
	replace_file_in_google_drive('1DcrHOO3FToeRmikb2U2TAgnWPU-6zVq2', 'ncep-925mb-weddell-temperature.png', '../ncep/')
	replace_file_in_google_drive('16Du1mEzGmQ2pJpQH_qJakP8CRskRzjvy', 'ncep-925mb-bellam-temperature.png', '../ncep/')
	replace_file_in_google_drive('1OX5ODDfae0_CbtXO4cTFqJ-l7vk0-FY-', 'ncep-925mb-ross-temperature.png', '../ncep/')
	replace_file_in_google_drive('1jWREip9eUj3kk3huFnV6d8O2NlJo1OfG', 'ncep-925mb-pacific-temperature.png', '../ncep/')
	replace_file_in_google_drive('1Z9QnAy_h8SvtSUBzEvPLC0ThjzHy_Xv5', 'ncep-925mb-indian-temperature.png', '../ncep/')
	
	replace_file_in_google_drive('1-rcXa7MWM4mSA8OFIPkrxZbM0sYeRqOb', 'ncep-surface-cab-temperature.png', '../ncep/')
	replace_file_in_google_drive('1w03yWCO2cfanCNxexxaVpZRoHvNkPqrI', 'ncep-surface-caa-temperature.png', '../ncep/')
	replace_file_in_google_drive('10PPnDR7l5Ml5bGF2lA0Y6vrS0_oqONhB', 'ncep-surface-beaufort-temperature.png', '../ncep/')
	replace_file_in_google_drive('1tRBz-QN7P5XoCCrmaXOTTPhdwrKX4tpF', 'ncep-surface-chukchi-temperature.png', '../ncep/')
	replace_file_in_google_drive('1s2D8AT_CNEgZ4JDZ-eoM3Dj8KfD86jl9', 'ncep-surface-bering-temperature.png', '../ncep/')
	replace_file_in_google_drive('1k7bYeLHXrMw3ze11-fO-Xc39fu7S5Jv3', 'ncep-surface-okhotsk-temperature.png', '../ncep/')
	replace_file_in_google_drive('1VcqbUsxZv4T7I_uxxNgacPNlo0AgDyTn', 'ncep-surface-ess-temperature.png', '../ncep/')
	replace_file_in_google_drive('1dBBzuHznvrsn2qARZ8aChx9O-u9U3sXD', 'ncep-surface-laptev-temperature.png', '../ncep/')
	replace_file_in_google_drive('1Hz2691JotPlzMyChv3rwMroyPaKSDktI', 'ncep-surface-kara-temperature.png', '../ncep/')
	replace_file_in_google_drive('1CrGVPm4IBqqcFwDMuzaGuWx2pJB9GfPg', 'ncep-surface-barents-temperature.png', '../ncep/')
	replace_file_in_google_drive('1oZArPpz7MLOp7hxTLXnh-tUbJ_5KTkfY', 'ncep-surface-greenland-temperature.png', '../ncep/')
	replace_file_in_google_drive('1DkG8Oot6t4o1fc59ckqSnOFsL9wOV9tY', 'ncep-surface-baffin-temperature.png', '../ncep/')
	replace_file_in_google_drive('1PN2lXednpJ7kN4MyTotb_QbeK4QaoT3G', 'ncep-surface-hudson-temperature.png', '../ncep/')	
	
	replace_file_in_google_drive('1Ze3RFT0GuBj5lrHs6HOkleKhlHEyaU8l', 'ncep-925mb-cab-temperature.png', '../ncep/')
	replace_file_in_google_drive('19RYNfAyB6kp3Y2lkUSSHovKHgL4erhRS', 'ncep-925mb-caa-temperature.png', '../ncep/')
	replace_file_in_google_drive('1WWGzcqlin3_L5jZQPE8-poNNsWkjgUS8', 'ncep-925mb-beaufort-temperature.png', '../ncep/')
	replace_file_in_google_drive('13j_DoRTtiUsTvMo92A7Ze3bIyoERlLeB', 'ncep-925mb-chukchi-temperature.png', '../ncep/')
	replace_file_in_google_drive('1PfQDf2MEu7LhhtmN0gR1s5Xpb-GkxneK', 'ncep-925mb-bering-temperature.png', '../ncep/')
	replace_file_in_google_drive('1xfkWUkG6beLlk_bGoX_qD5_i6H3nwXeb', 'ncep-925mb-okhotsk-temperature.png', '../ncep/')
	replace_file_in_google_drive('1Eg9UD2w0Ngg_v3UpemRdlv6q2GFFGl9V', 'ncep-925mb-ess-temperature.png', '../ncep/')
	replace_file_in_google_drive('1NffxvUOtYiNfe0WqdlLSdLeU1Ga5LIOW', 'ncep-925mb-laptev-temperature.png', '../ncep/')
	replace_file_in_google_drive('1PAW94WSu1EUgWT4UQLi2NuZIdGVlxH2F', 'ncep-925mb-kara-temperature.png', '../ncep/')
	replace_file_in_google_drive('12woxxpQzLX_ru2eou-RgcB7g9rWYX0cL', 'ncep-925mb-barents-temperature.png', '../ncep/')
	replace_file_in_google_drive('1PJboQRKoxNO4mAhsy6taj1Q1MpNiDQKd', 'ncep-925mb-greenland-temperature.png', '../ncep/')
	replace_file_in_google_drive('1WR-raMTzVNVfv2hYdDIbXRPgEm06QVO5', 'ncep-925mb-baffin-temperature.png', '../ncep/')
	replace_file_in_google_drive('13buPe7v3nEv8mhEQvV0tkBSBdkT6IhAY', 'ncep-925mb-hudson-temperature.png', '../ncep/')	
	
def getLastSavedDay(filename):
	print('inside last saved day', filename)
	with open(filename, 'r') as f:
		lastline = f.readlines()[-1]
	splitted = lastline.split(",", 3)
	print('inside last saved day', ' last line ', lastline)
	return int(splitted[0]), int(splitted[1])
	
def appendToCsvFile(filenameshort, data, format):
	
	rows = data.shape[0]
	if rows == 0:
		return	

	firstyear = data[0][0]
	firstday = data[0][1]
	lastyear = data[rows-1][0]
	lastday = data[rows-1][1]
	print('inside append to csv', filenameshort, firstyear, firstday, lastyear, lastday)
	
	filename = filenameshort + '.csv'
	
	lastSavedYear,lastSavedDay = getLastSavedDay(filename)
	rowstoadd = int((365*lastyear + lastday) - (365*lastSavedYear + lastSavedDay))
	print('last saved day', lastSavedYear, lastSavedDay, ' and ', rowstoadd)

	if rowstoadd <= 0:
		print('nothing to add to csv file', lastSavedDay)
		return

	data = data[-rowstoadd:,:]
	doAppendToCsvFile(filenameshort, data, format)
	
def doAppendToCsvFile(filenameshort, data, format):

	filename = filenameshort + '.csv'
	tempname = filenameshort + "-temp.csv"
	tempmergedname = filenameshort + "-temp-merged.csv"
	
	np.savetxt(tempname, data, format)
	
	filenames = [filename, tempname]
	with open(tempmergedname, 'w') as outfile:
		for fname in filenames:
			with open(fname) as infile:
				outfile.write(infile.read())
	os.remove(tempname)
	os.remove(filename)
	os.rename(tempmergedname, filename)

def updateLastRowOfCsvFile(shortFilename, data, format):
	
	print('inside update last row', shortFilename)
	filename = shortFilename + '.csv'
	with open(filename, "r+") as file:

		# Move the pointer (similar to a cursor in a text editor) to the end of the file
		file.seek(0, os.SEEK_END)

		# This code means the following code skips the very last character in the file -
		# i.e. in the case the last line is null we delete the last line
		# and the penultimate one
		pos = file.tell() - 1
		foundNewlines = 0

		# Read each character in the file one at a time from the penultimate
		# character going backwards, searching for a newline character
		# If we find a new line, exit the search
		while pos > 0 and foundNewlines < 2:
			pos -= 1
			file.seek(pos, os.SEEK_SET)
			ch = file.read(1)
			if ch == "\r" or ch == "\n":
				if ch == "\r":
					print('found carriage return')
					pos += 1
				else:
					print('found newline')
				foundNewlines += 1

		# So long as we're not at the start of the file, delete all the characters ahead
		# of this position
		if pos > 0:
			file.seek(pos, os.SEEK_SET)
			file.truncate()
	
	tempname = shortFilename + '_temp.csv'
	tempmergedname = shortFilename + '_merged_temp.csv'
	np.savetxt(tempname, data, delimiter=",", fmt=format)

	filenames = [filename, tempname]
	with open(tempmergedname, 'w') as outfile:
		for fname in filenames:
			with open(fname) as infile:
				outfile.write(infile.read())
	os.remove(filename)
	os.rename(tempmergedname, filename)

allbea = []
allchu = []
alless = []
alllap = []
allkar = []
allbar = []
allgre = []
allbaf = []
allhud = []
allcaa = []
allcab = []
allber = []
allokh = []
alloth = []

allwed = []
allbel = []
allros = []
allpac = []
allind = []
alltot = []

alltotal = []
	
allyear = []
allmonth = []
allday = []

useWeights = True
regional = True

auto = True
north = True

if(auto):
	useWeights = True
	regional = True
	north = True

	downloadLatestFiles()

	arctictempsforyear925 = [] 
	arctictempsforyear925.append(loadYear925(2024))
	
	hemisphere = 'arctic' if north else 'antarctic'
	hemisphereshort = "" if north else "south-"
	
	format = ','.join(['%i'] + ['%7.3f']*(len(arctictempsforyear925[0])-1))
	doAppendToCsvFile('data/ncep-' + hemisphere + '-ocean-temperature-925-mb-1979-to-2023', arctictempsforyear925, format)
	#updateLastRowOfCsvFile('data/ncep-' + hemisphere + '-ocean-temperature-925-mb-1979-to-2023', arctictempsforyear925, format)
	
	filename925mb = "data/ncep-" + hemisphereshort + "925mb-regional" 		
	appendToRegionalCsv(filename925mb, north)

	uploadToDropbox([filename925mb + ".csv"])
	
	reset()
	
	arctictempsforyear = []
	arctictempsforyear.append(loadYear(2024))
	doAppendToCsvFile('data/ncep-' + hemisphere + '-ocean-surface-temperature-1979-to-2023', arctictempsforyear, format)
	#updateLastRowOfCsvFile('data/ncep-' + hemisphere + '-ocean-surface-temperature-1979-to-2023', arctictempsforyear, format)
	
	filenamesurface = "data/ncep-" + hemisphereshort + "surface-regional" 
	appendToRegionalCsv(filenamesurface, north)
	uploadToDropbox([filenamesurface + ".csv"])	
	
	time.sleep(5)
	
	createPlots()
	
	plotRegionalGraphs925mb(filename925mb + ".csv")
	plotRegionalGraphsSurface(filenamesurface + ".csv")
	
	reset()
	
	north = False
	
	filename925mb = "data/ncep-south-925mb-regional"
	loadYear925(2024)
	appendToRegionalCsv(filename925mb, north)
	uploadToDropbox([filename925mb + ".csv"])
	
	reset()
	
	filenamesurface = "data/ncep-south-surface-regional"
	loadYear(2024)
	appendToRegionalCsv(filenamesurface, north)
	uploadToDropbox([filenamesurface + ".csv"])
	
	time.sleep(5)
	
	plotRegionalGraphs925mbSouth(filename925mb + ".csv")
	plotRegionalGraphsSurfaceSouth(filenamesurface + ".csv")

	time.sleep(3)
	uploadToGoogleDrive()
	
	exit()

arctictemps = []
for year in range(2020,2023):
	arctictempsforyear = loadYear925(year)	
	arctictemps.append(arctictempsforyear)
np.savetxt("arctic-temp.csv", arctictemps, delimiter=",", fmt="%.3f")
