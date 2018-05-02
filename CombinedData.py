from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import os.path
import csv

fig, ax = plt.subplots(1,1, figsize=(16,8))

###
# Create the map object
###
myMap = Basemap(ax = ax, # Associate it with the SubplotAxes ax
            projection='cea', # cylindrical equal-area projection
            resolution='c', # coarse resolution coastlines
            lat_0=0.,lon_0=0., # center of map
            llcrnrlat=-90, urcrnrlat=90, # lower, upper latitude
            llcrnrlon=-180, urcrnrlon=180) # left, right longitude

###
# Put standard features on the map
###
myMap.drawcoastlines() # draw coastlines.
myMap.drawmapboundary(fill_color='#505050') # background fill becomes ocean
myMap.fillcontinents(color='#000000',lake_color='#505050', zorder=0) # fills in the land
myMap.drawmeridians(range(-180,180,30), labels=[1,0,0,1], labelstyle='+/-') #label left/bottom
myMap.drawparallels(range(-90,90,30), labels=[1,0,0,1], labelstyle='+/-')

###
# Label the map
###
ax.set_title('Global Occurrences of Landslides vs. Earthquakes Over 5.5 in Magnitude From 2007-2016')
ax.set_xlabel('\n\nDegrees Longitude')
ax.set_ylabel('Degrees Latitude\n\n')

#####
# Get data from the CSV file
####
directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, 'Earthquake Data.csv') 
datafile = open(filename,'rb')

# Create empty lists to hold latitude and longitude data
latEarth = []
longEarth = []
# Read data from the CSV file
datareader = csv.reader(datafile) 
headers = datareader.next() # read first row and store separately
for row in datareader:
    latEarth.append(float(row[2]))    
    longEarth.append(float(row[3])) 
    
#####
# Transform data
#####
x, y = myMap(longEarth, latEarth) # convert to feet, the units of the map
    
###
# Plot data
###
ax.scatter(x, y, s=1, color='#FF0033', alpha=0.2)


#####
# Get data from the CSV file
####
directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, 'Landslide Data.csv') 
datafile = open(filename,'rb')

# Create empty lists to hold latitude and longitude data
latLand = []
longLand = []
# Read data from the CSV file
datareader = csv.reader(datafile) 
headers = datareader.next() # read first row and store separately
c = 0
for row in datareader:
    if c%2==0:
        latLand.append(float(row[len(row)-2]))
        longLand.append(float(row[len(row)-1]))
    c+=1
 
#####
# Transform data
#####
x, y = myMap(longLand, latLand) # convert to feet, the units of the map
    
###
# Plot data
###
ax.scatter(x, y, s=1, color='#00FFFF', alpha=0.2)

#####
# Get data from the CSV file
####
directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, 'Tsunami Data.csv') 
datafile = open(filename,'rb')

# Create empty lists to hold latitude and longitude data
latTsu = []
longTsu = []
# Read data from the CSV file
datareader = csv.reader(datafile) 
headers = datareader.next() # read first row and store separately
for row in datareader:
    if float(row[5]) >= 2007 and float(row[5]) <= 2016:
        latTsu.append(float(row[16]))    
        longTsu.append(float(row[17])) 
    
#####
# Transform data
#####
x, y = myMap(longTsu, latTsu) # convert to feet, the units of the map
    
###
# Plot data
###
ax.scatter(x, y, s=1, c='#00FF66', alpha=0.2)

fig.show()