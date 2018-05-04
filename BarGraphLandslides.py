import matplotlib.pyplot as plt
import os.path
import csv
import numpy as np

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
            if date == 2007:
                
 
objects = ('2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',)
y_pos = np.arange(len(objects))
performance = [10,8,6,4,2,1]
 
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Usage')
plt.title('Programming language usage')
 
plt.show()