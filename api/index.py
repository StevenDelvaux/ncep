import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from flask import Flask, request, jsonify, send_file 

class Region:
	slater = "slater"
	cab = "cab"
	beaufort = "beaufort"
	chukchi = "chukchi"
	ess = "ess"
	laptev = "laptev"
	kara = "kara"
	barents = "barents"
	greenland = "greenland"
	baffin = "baffin"
	hudson = "hudson"
	caa = "caa"
	bering = "bering"
	okhotsk = "okhotsk"
	southern = "southern"
	weddell = "weddell"
	bellamu = "bellamu"
	ross = "ross"
	pacific = "pacific"
	indian = "indian"

app = Flask(__name__)
@app.route("/")
def hello():
	return "Generate an air temperature graph for a given region and year"

@app.get("/plot-surface-temperature")
def plotSurfaceTemperatureGraph():
	return plotTemperatureGraph(True)
	
@app.get("/plot-925mb-temperature")
def plot925mbTemperatureGraph():
	return plotTemperatureGraph(False)
	
def plotTemperatureGraph(isSurface):
	yearString = request.args.get('year')
	region = request.args.get('region')

	if not yearString.isdigit():
		return "Invalid year", 400
	year = int(yearString)	
	if year < 1979 or year > 2024:
		return "Year must be between 1979 and 2024", 400
	
	arcticRegions = [Region.slater, Region.cab, Region.beaufort, Region.chukchi, Region.ess, Region.laptev, Region.kara, Region.barents, Region.greenland, Region.baffin, Region.hudson, Region.caa, Region.bering, Region.okhotsk]
	antarcticRegions = [Region.southern, Region.weddell, Region.bellamu, Region.ross, Region.pacific, Region.indian]
	
	if region in arcticRegions:
		north = True
	elif region in antarcticRegions:
		north = False
	else:
		return "Unknown region name", 400
		
	if region == Region.slater:
		return createSlaterPlot(year, isSurface)
		
	hemisphereshort = "" if north else "south-"	
	filenameCsv = "data/ncep-" + hemisphereshort + ('surface' if isSurface else '925mb') + "-regional.csv" 
	data = np.loadtxt(filenameCsv, delimiter=",", dtype=str)
	
	plotRegionalDataDictionary = { 
		Region.beaufort: { "index": 4, "surfacemin": -40, "surfacemax": 12, "925min": -40, "925max": 20, "name": "Beaufort Sea"},
		Region.chukchi:  { "index": 5, "surfacemin": -40, "surfacemax": 12, "925min": -40, "925max": 20, "name": "Chukchi Sea"},
		Region.ess:      { "index": 6, "surfacemin": -40, "surfacemax": 12, "925min": -35, "925max": 20, "name": "East Siberian Sea"},
		Region.laptev:   { "index": 7, "surfacemin": -40, "surfacemax": 14, "925min": -35, "925max": 20, "name": "Laptev Sea"},
		Region.kara:     { "index": 8, "surfacemin": -40, "surfacemax": 12, "925min": -35, "925max": 20, "name": "Kara Sea"},
		Region.barents:  { "index": 9, "surfacemin": -25, "surfacemax": 12, "925min": -25, "925max": 20, "name": "Barents Sea"},
		Region.greenland:{ "index": 10,"surfacemin": -15, "surfacemax": 10, "925min": -20, "925max": 15, "name": "Greenland Sea"},
		Region.cab:      { "index": 11,"surfacemin": -40, "surfacemax": 5,  "925min": -35, "925max": 10, "name": "Central Arctic Basin"},
		Region.caa:      { "index": 12,"surfacemin": -40, "surfacemax": 13, "925min": -40, "925max": 15, "name": "Canadian Arctic Archipelago"},
		Region.baffin:   { "index": 13,"surfacemin": -25, "surfacemax": 12, "925min": -25, "925max": 15, "name": "Baffin Bay"},
		Region.hudson:   { "index": 14,"surfacemin": -40, "surfacemax": 15, "925min": -35, "925max": 20, "name": "Hudson Bay"},
		Region.bering:   { "index": 3, "surfacemin": -15, "surfacemax": 13, "925min": -20, "925max": 15, "name": "Bering Sea"},
		Region.okhotsk:  { "index": 2, "surfacemin": -25, "surfacemax": 18, "925min": -25, "925max": 20, "name": "Sea of Okhotsk"},
		Region.weddell:  { "index": 2, "surfacemin": -40, "surfacemax": 2,  "925min": -30, "925max": 2,  "name": "Weddell Sea"},
		Region.bellamu:  { "index": 3, "surfacemin": -45, "surfacemax": 5,  "925min": -40, "925max": 3,  "name": "Bellingshausen-Amundsen Sea"},
		Region.ross:     { "index": 4, "surfacemin": -40, "surfacemax": 2,  "925min": -35, "925max": 2,  "name": "Ross Sea"},
		Region.pacific:  { "index": 5, "surfacemin": -40, "surfacemax": 5,  "925min": -35, "925max": 5,  "name": "West Pacific southern ocean"},
		Region.indian:   { "index": 6, "surfacemin": -40, "surfacemax": 2,  "925min": -30, "925max": 2,  "name": "Indian southern ocean"},
		Region.southern: { "index": 7, "surfacemin": -30, "surfacemax": 2,  "925min": -30, "925max": 2,  "name": "Southern ocean"}
	}
	plotData = plotRegionalDataDictionary.get(region)
	
	if isSurface:
		return createRegionalPlot(plotData.get("index"), plotData.get("surfacemin"), plotData.get("surfacemax"), data, year, plotData.get("name") + " NCEP reanalysis surface air temperature", north)
	else:
		return createRegionalPlot(plotData.get("index"), plotData.get("925min"), plotData.get("925max"), data, year, plotData.get("name") + " NCEP reanalysis 925mb temperature", north)

def printRegionalTemperature(data, ax, ymin, ymax, year, name, north=True):
	dates = np.arange(1,366)
	
	baseline = np.sum(data[1:30,:],axis=0)/30
	tens = np.sum(data[31:44,:],axis=0)/12	
	
	ax.plot(dates, baseline, label='1980-2009 avg', linestyle='dashed', color=(0,0,0));
	ax.plot(dates, tens, label='2010-2023 avg',  color=(0,0,0));
	ax.plot(dates, data[year-1979,:], label=str(year), color=(1.0,0,0), linewidth=2);
	
	ax.set_ylabel("Temperature (°C)")
	ax.set_title(name)
	ax.legend(ncol=1, loc=(8 if north else 3), prop={'size': 8})
	ax.axis([0, 365, ymin, ymax])
	ax.grid(True);
	
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	ax.set_xticks([0,31,59,90,120,151,181,212,243,273,304,334,365], ['', '', '', '', '', '', '', '', '', '', '', '', ''])
	ax.xaxis.set_minor_locator(ticker.FixedLocator([15.5,45,74.4,105,135.5,166,196.5,227.5,258,288.5,319,349.5]))
	ax.xaxis.set_minor_formatter(ticker.FixedFormatter(months))
	ax.tick_params(which='minor', length=0)	

def createSlaterPlot(year, isSurface):
	csvFileName = 'data/ncep-arctic-ocean-' + ('surface-temperature' if isSurface else 'temperature-925-mb') + '-1979-to-2023.csv'		
	with open(csvFileName, 'r') as f:
		data = f.readlines()
	fig, axs = plt.subplots(figsize=(8, 5))	
	
	lines = np.array(data[1:])
	matrix = np.array([np.pad(i.lstrip().split(","), (0,366 - len(i.lstrip().split(","))), 'constant', constant_values=(np.nan,)) for i in lines]).astype(float)
	matrix = matrix[:,1:]
		
	if isSurface:
		printRegionalTemperature(matrix, axs, -40, 5, year, "NCEP reanalysis surface temperature over Arctic Ocean (°C)")
	else:
		printRegionalTemperature(matrix, axs, -30, 10, year, "NCEP reanalysis 925 mb temperature over Arctic Ocean (°C)")
		
	filename = "/tmp/plot.png"
	fig.savefig(filename)
	return send_file(filename, mimetype='image/png')

def createRegionalPlot(col, ymin, ymax, data, year, name, north = True):
	print('inside createRegionalPlot', name)
	fig, axs = plt.subplots(figsize=(8, 5))
	
	regional = data[1:,col]
	regional = np.array([i.lstrip() for i in regional]).astype(float)
	padded = np.pad(regional, (0, 365*45 - regional.shape[0]), 'constant', constant_values=(np.nan,))
	matrix = padded.reshape((45,365))
	
	printRegionalTemperature(matrix, axs, ymin, ymax, year, name, north)
	filename = "/tmp/plot.png"
	fig.savefig(filename)
	return send_file(filename, mimetype='image/png')