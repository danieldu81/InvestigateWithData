import matplotlib.pyplot as plt
import os.path
import csv

#create empty list to store each date added later
dates = []

#####
# Get data from the CSV file
####
directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, 'Earthquake Data.csv') 
datafile = open(filename,'rb')

# Read data from the CSV file
datareader = csv.reader(datafile) 
headers = datareader.next() # read first row and store separately
for row in datareader:
    if len(row[0]) == 10:
        entry = row[0]
        date = float(entry[-4:])
        if date >= 2007 and date <= 2015:
            dates.append(date) #add date to list if in range   

#plot histogram of frequency of tsunamis for each year
fig, ax = plt.subplots(1, 1)
ax.hist(dates, bins=range(2007, 2016))

# properly label the figure and show it for the world to see
ax.set_title('Earthquake Frequency From 2007-2015')
ax.set_xlabel('Year')
ax.set_ylabel('Frequency')
 
plt.show()