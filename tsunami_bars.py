import matplotlib.pyplot as plt
import os.path
import csv

dates = []

#####
# Get data from the CSV file
####
directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, 'Tsunami Data.csv') 
datafile = open(filename,'rb')

# Read data from the CSV file
datareader = csv.reader(datafile) 
headers = datareader.next() # read first row and store separately
for row in datareader:
    if float(row[5]) >= 2007 and float(row[5]) <= 2015:
        dates.append(float(row[5]))    
 
fig, ax = plt.subplots(1, 1)
ax.hist(dates, bins=range(2007, 2016))

# properly label the figure and show it for the world to see
ax.set_title('Tsunami Frequency')
ax.set_xlabel('Year')
ax.set_ylabel('Frequency')
 
plt.show()