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
myMap.drawmapboundary(fill_color='aqua') # background fill becomes ocean
myMap.fillcontinents(color='coral',lake_color='aqua', zorder=0) # fills in the land
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
filename = os.path.join(directory, 'Hurricane Data.csv') 
datafile = open(filename,'rb')

# Create empty lists to hold latitude and longitude data
latHurr = []
longHurr = []
# Read data from the CSV file
datareader = csv.reader(datafile) 
headers = datareader.next() # read first row and store separately
for row in datareader:
    if row[1] is not "UNNAMED" and row[1] is not "" and row[4] is not "" and row[5] is not "":
        latit = row[4]
        longit = row[5]
        latHurr.append(float(latit[:len(latit)-1]))    
        longHurr.append(float(longit[:len(longit)-1]))
    
#####
# Transform data
#####
x, y = myMap(longHurr, latHurr) # convert to feet, the units of the map
    
###
# Plot data
###
ax.scatter(x, y, s=5, c='#ffff00')
fig.show()