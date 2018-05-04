import matplotlib.pyplot as plt
import numpy as np
import re

# parse the hurdat files!
def parse_hurdat(filename):
    hurdat = map(lambda line: [field.strip() for field in line],
                 [line.split(',') for line in open(filename)])

    # determine indices at which a hurricane record starts and ends
    records = filter(lambda x: x[1][0][:2] in ['AL', 'EP'],
                     zip(range(len(hurdat)), hurdat))
    indices = map(lambda tup: (tup[0]+1, tup[0]+int(tup[1][2])+1), records)

    # for each storm record, figure out if it's a hurricane proper (not TS)
    status = map(lambda pair: (int(hurdat[pair[0]][0][:4]),
             map(lambda data: data[3], hurdat[pair[0]:pair[1]])), indices)
    return map(lambda h: h[0], filter(lambda s: 'HU' in s[1], status))

# get a list of all hurricane years and plot as a histogram
hc = parse_hurdat('hurdat-atlantic.csv') + parse_hurdat('hurdat-pacific.csv')
fig, ax = plt.subplots(1, 1)
ax.hist(hc)

# properly label the figure and show it for the world to see
ax.set_title('Hurricane Frequency')
ax.set_xlabel('Year')
ax.set_ylabel('Frequency')
plt.show()
