import matplotlib.pyplot as plt
import os.path
import csv

dates = []

#####
# Get data from the CSV file
####

directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, 'Landslide Data.csv') 
datafile = open(filename,'rb')

# Read data from the CSV file
datareader = csv.reader(datafile) 
headers = datareader.next() # read first row and store separately
for row in datareader:
    if row[3] is not "":
        entry = row[3]
        date = float(entry[6:10])
        if date >= 2007 and date <= 2016:
            dates.append(date)     
 
fig, ax = plt.subplots(1, 1)
ax.hist(dates, bins=range(2007, 2016))

# properly label the figure and show it for the world to see
ax.set_title('Landslide Frequency')
ax.set_xlabel('Year')
ax.set_ylabel('Frequency')
 
plt.show()