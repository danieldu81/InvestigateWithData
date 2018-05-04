#imports for distance correlation
import numpy as np
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os.path
import csv

#####
# Get data from the CSV file - Earthquakes
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
# Get data from the CSV file - Landslides
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
# Get data from the CSV file - Tsnuami
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
# Get data from the CSV file - Hurricanes
####

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
#cmobine atlantic and pacific data
lat_a.extend(lat_p)
lon_a.extend(lon_p)

##
# Analysis - combine data for analysis
##
#full arrays
earthquakes = np.array((latEarth, longEarth))
landslides = np.array((latLand, longLand))
tsunamis = np.array((latTsu, longTsu))
hurrykanes = np.array((lat_a, lon_a))

partearth = [[],[]]
partland = [[],[]]
parttsu = [[],[]]
parthur = [[],[]]

refparts = {0:partearth, 1:partland, 2:parttsu, 3:parthur}

iter = [earthquakes, landslides, tsunamis, hurrykanes]
def cannibalize(a,b):
    for i,ar in enumerate(iter):
        for j, el in enumerate(ar[1]):
            if el<b and el>a:
                refparts[i][1].append(el)
                refparts[i][0].append(ar[0][j])

map(lambda pair: cannibalize(pair[0], pair[1]), [(65, 100), (120, 145), (-130, -118)])

#normalize length
mins = 95 #length of samllest cannibalized array
refpartnp = [] #array to house np arrays
for i in range(0,4):
    refparts[i] = [refparts[i][0][::len(refparts[i][0])/mins], refparts[i][1][::len(refparts[i][1])/mins]]
    #ensures that after the normalization (periodic sampling), all matrixes are the same size.
    refparts[i] = [refparts[i][0][:mins],refparts[i][1][:mins]]
    refpartnp.append(np.array(refparts[i]))

#get distance correlation between landslides and each of remaining matricies.

def distCor4(nparrays):
    '''utilizes python built-in map function to repeatedly call distCor2 between landslides and earthquakes, tsunamies, and hurricanes. then,
    prints an array of these coefficients.

    all arrays must have the same number of rows.
    '''
    coeffs = map(lambda pair: distCor2(pair[0], pair[1]), [(nparrays[1], nparrays[0]), (nparrays[1], nparrays[2]), (nparrays[1], nparrays[3])])
    return coeffs

def distCor2(X, Y):
    '''both arrays must have the same number of rows... that's basically it.'''

    assert X.shape[0]==Y.shape[0]

    centDist_X = centDist(X)
    centDist_Y = centDist(Y)
    distVar_X = distVar(X)
    distVar_Y = distVar(Y)
    distCov_XY_CD = distCov(centDist_X,centDist_Y)

    distCor2 = 0.0
    if distVar_X>0 and distVar_Y>0:
        distCor2 = distCov_XY_CD/np.sqrt(distVar_X*distVar_Y)

    return distCor2

def centDist(X):
    '''finds pairwise Euclidean distance matrix (D) between rows of inputted X
    and centers (statistically) each cell with column (c), row (r), and grand
    (g) means.'''

    D = squareform(pdist(X))
    cm = D.mean(axis=0)
    rm = D.mean(axis=1)
    gm = rm.mean()
    c = np.tile(cm,(D.shape[1],1))
    r = np.tile(rm,(D.shape[0],1)).transpose()
    g = np.tile(gm,D.shape)
    centDist = D + g - c - r

    return centDist

def distVar(X):
    '''finds the statistical distance variance of a matrix X.'''

    return np.sqrt(np.sum(X**2 / X.shape[0]**2))

def distCov(X,Y):
    '''finds the distance covariance between X and Y.'''
    rows = X.shape[0]
    prod = np.multiply(X,Y)
    distCov = np.sqrt(prod.sum())/rows

    return distCov

print 'distance correlations for landslides and [earthquakes, tsunamis, hurricanes]:'
print distCor4(refpartnp)
