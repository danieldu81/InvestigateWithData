import matplotlib.pyplot as plt
import os.path
import csv
import numpy as np

y2007 = 0
y2008 = 0
y2009 = 0
y2010 = 0
y2011 = 0
y2012 = 0
y2013 = 0
y2014 = 0
y2015 = 0
y2016 = 0

def seven():
    y2007 += 1
    
def eight():
    y2008 += 1
    
def seven():
    y2007 += 1
    
def nine():
    y2009 += 1
    
def ten():
    y2010 += 1
    
def eleven():
    y2011 += 1
    
def twelve():
    y2012 += 1
    
def thirteen():
    y2013 += 1
    
def fourteen():
    y2014 += 1
    
def fifteen():
    y2015 += 1
    
def sixteen():
    y2016 += 1

dates = {2007: 'seven', 2008: 'eight', 2009: 'nine', 2010: 'ten', 2011: 'eleven', 2012: 'twelve', 2013: 'thirteen', 2014: 'fourteen', 2015: 'fifteen', 2016: 'sixteen'}

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
            dates[date]     
 
objects = ('2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',)
y_pos = np.arange(len(objects))
performance = [10,8,6,4,2,1]
 
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Usage')
plt.title('Programming language usage')
 
plt.show()