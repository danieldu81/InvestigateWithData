import basemap as bm  # since I installed and symlinked basemap sketchily
                      # you probably need 'import mpl_toolkits.basemap as bm'
import matplotlib.pyplot as plt

# setup map
fig, ax = plt.subplots(1,1, figsize=(16,8))
world = bm.Basemap(ax=ax, projection='cea', resolution='c', lat_0=0., lon_0=0.,
                   llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
world.drawcoastlines()
world.drawmapboundary(fill_color='aqua')
world.fillcontinents(color='coral', lake_color='aqua', zorder=0)
world.drawmeridians(range(-180,180,30), labels=[1,0,0,1], labelstyle='+/-')
world.drawparallels(range(-90,90,30), labels=[1,0,0,1], labelstyle='+/-')
ax.set_title('Hurry-Cains')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

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

lat_a, lon_a = parse_hurdat('hurdat-atlantic.dat')
lat_p, lon_p = parse_hurdat('hurdat-pacific.dat')

# plot and show
x_a, y_a = world(lon_a, lat_a)
x_p, y_p = world(lon_p, lat_p)
ax.scatter(x_a+x_p, y_a+y_p, s=5, c='#ffff00')
plt.show()
