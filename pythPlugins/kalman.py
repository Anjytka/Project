import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

tree = ET.parse('/Users/pavelmalinnikov/Downloads/1464857.gpx')
root = tree.getroot()

namespaces = {'ns':"http://www.topografix.com/GPX/1/1"}
# namespaces = {'ns':"http://www.topografix.com/GPX/1/0"}
points = root.findall(".//ns:trkpt", namespaces = namespaces)

if len(points) == 0:
    print 'Track loading failed'
    exit()

resultLng = []
resultLat = []

def update(mean1, var1, mean2, var2):
    new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
    new_var = 1 / (1 / var1 + 1 / var2)
    return [new_mean, new_var]

def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]


positions = [[float(p.get('lon')), float(p.get('lat'))] for p in points]


longitudes = [position[0] for position in positions]
latitudes = [position[1] for position in positions]

motion_sig = 1.
measurement_sig = 10.

lng = longitudes[0]
lat = latitudes[0]
sigLng = 1.
sigLat = 1.


for i in range(len(positions)):
    lng, sigLng = update(lng, sigLng, longitudes[i], measurement_sig)
    lng, sigLng = predict(lng, sigLng, 0, motion_sig)
    resultLng.append(lng)

    lat, sigLat = update(lat, sigLat, latitudes[i], measurement_sig)
    lat, sigLat = predict(lat, sigLat, 0, motion_sig)
    resultLat.append(lat)


kalman = [[resultLng[i], resultLat[i]] for i in range(len(positions))]

plt.plot(*zip(*positions), color = 'r')
plt.plot(*zip(*kalman), color = 'g')

plt.show()