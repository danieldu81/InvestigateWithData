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
ax.set_title('Global Occurrences of Landslides, Earthquakes Over 5.5 in Magnitude, Tsunamis, and Hurricanes From 2007-2016')
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
    if len(row[0]) == 10:
        entry = row[0]
        date = float(entry[-4:])
        if date >= 2007 and date <= 2016:
            latEarth.append(float(row[2])) 
            longEarth.append(float(row[3])) 
    
#####
# Transform data
#####
x, y = myMap(longEarth, latEarth) # convert to feet, the units of the map
    
###
# Plot data
###
ax.scatter(x, y, s=0.5, color='#FF0033', alpha=0.2)


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
    if row[3] is not "":
        entry = row[3]
        date = float(entry[6:10])
        if date >= 2007 and date <= 2016:
            latLand.append(float(row[len(row)-2]))
            longLand.append(float(row[len(row)-1]))
 
#####
# Transform data
#####
x, y = myMap(longLand, latLand) # convert to feet, the units of the map
    
###
# Plot data
###
ax.scatter(x, y, s=0.5, color='#00FFFF', alpha=0.2)

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
ax.scatter(x, y, s=0.5, c='#00FF66', alpha=0.2)

# get data from HURDAT file
def parse_hurdat(filename):
    hurdat = map(lambda x: [y.strip() for y in x],
                 [line.split(',') for line in open(filename)])
    hurdat = [(0, [0, 0, 0, 0, 0])] + zip(range(1, len(hurdat)+1), hurdat)
    # take only one sample coordinate from each hurricane
    data = filter(lambda x: len(hurdat[x[0]-1][1]) < 5, hurdat)
    coords = map(lambda x: (x[1][4], x[1][5]), data)
    # transform ('65N', '8.5W') => (+65, -8.5)
    lat = map(lambda x: float(x[0][:-1]) if x[0][-1] == 'N'
              else -1*float(x[0][:-1]), coords)
    lon = map(lambda x: float(x[1][:-1]) if x[1][-1] == 'E'
              else -1*float(x[1][:-1]), coords)
    return (lat, lon)

lat_a, lon_a = parse_hurdat('hurdat-atlantic.csv')
lat_p, lon_p = parse_hurdat('hurdat-pacific.csv')

# plot and show
x_a, y_a = myMap(lon_a, lat_a)
x_p, y_p =myMap(lon_p, lat_p)
ax.scatter(x_a+x_p, y_a+y_p, s=0.5, c='#ffff00')

fig.show()