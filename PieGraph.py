import matplotlib.pyplot as plt
import os.path
import csv

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
            
labels = ['Landslides', 'Earthquakes', 'Tsunamis', 'Hurricanes']

total = len(latEarth) + len(latLand) + len(latTsu) + len(lat_a) + len(lat_p)
sizes = [len(latLand), len(latEarth), len(latTsu), len(lat_a)+len(lat_p)]
colors = ['#00FFFF', '#FF0033', '#00FF66', '#FFFF00']
patches, texts = plt.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
plt.legend(patches, labels, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.title('Percentage of Each Geological Event Over Years 2007-2016')
plt.show()