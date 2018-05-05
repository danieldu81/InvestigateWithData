import matplotlib.pyplot as plt
import os.path
import csv
import matplotlib.patches as mpatches

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
for row in datareader:
    if row[3] is not "":
        entry = row[3]
        date = float(entry[6:10])
        if date >= 2007 and date <= 2015:
            latLand.append(float(row[len(row)-2])) #add latitude of landslide
            longLand.append(float(row[len(row)-1])) #add longitude of landslide

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
        if date >= 2007 and date <= 2015:
            latEarth.append(float(row[2])) #add latitude of earthquake
            longEarth.append(float(row[3])) #add longitude of earthquake
            
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
    if float(row[5]) >= 2007 and float(row[5]) <= 2015:
        latTsu.append(float(row[16])) #add latitude of tsunami 
        longTsu.append(float(row[17])) #add longitude of tsunami
        
# get data from HURDAT file
def parse_hurdat(filename):
    hurdat = map(lambda x: [y.strip() for y in x],
                 [line.split(',') for line in open(filename)])
    hurdat = [(0, [0, 0, 0, 0, 0])] + zip(range(1, len(hurdat)+1), hurdat)
    # take only one sample coordinate from each hurricane
    data = filter(lambda x: len(hurdat[x[0]-1][1]) < 5, hurdat)
    # take only proper hurricanes, not tropical storms
    data = filter(lambda x: x[1][3] == 'HU', data)
    coords = map(lambda x: (x[1][4], x[1][5]), data)
    # transform ('65N', '8.5W') => (+65, -8.5)
    lat = map(lambda x: float(x[0][:-1]) if x[0][-1] == 'N'
              else -1*float(x[0][:-1]), coords)
    lon = map(lambda x: float(x[1][:-1]) if x[1][-1] == 'E'
              else -1*float(x[1][:-1]), coords)
    return (lat, lon)

lat_a, lon_a = parse_hurdat('hurdat-atlantic.csv')
lat_p, lon_p = parse_hurdat('hurdat-pacific.csv')            
      
#set labels for the four categories  
labels = ['Landslides', 'Earthquakes', 'Tsunamis', 'Hurricanes']

total = len(latEarth) + len(latLand) + len(latTsu) + len(lat_a) + len(lat_p) #sum total number of geologic events
sizes = [len(latLand), len(latEarth), len(latTsu), len(lat_a)+len(lat_p)] #divide pie graph into percentages
colors = ['#00FFFF', '#FF0033', '#00FF66', '#FFFF00'] #colorize pie graph
patches = plt.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90) #display percentages
blue_patch = mpatches.Patch(color='#00FFFF', label='Landslides') #create legend
red_patch = mpatches.Patch(color='#FF0033', label='Earthquakes')
green_patch = mpatches.Patch(color='#00FF66', label='Tsunamis')
yellow_patch = mpatches.Patch(color='#FFFF00', label='Hurricanes')
plt.legend(handles=[blue_patch, red_patch, green_patch, yellow_patch], loc=2)
plt.axis('equal')
plt.tight_layout()
plt.title('Percentage of Each Geological Event Over Years 2007-2015')
plt.show()