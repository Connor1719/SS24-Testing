import spiceypy as spice
import os
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Function to load SPICE kernels
def load_kern(name):
    path = os.path.join(os.getcwd(), "kernelzzz", name)
    return str(path)

# Load SPICE kernels
spice.furnsh(load_kern('naif0012.tls'))
spice.furnsh(load_kern('de405.bsp'))

# Define the time range for observations
currTime = datetime.now()
years = 5
days = 365 * years
times = [spice.str2et(str(currTime + timedelta(days=i))) for i in range(days)]

# Get Earth and Mars positions relative to the Sun
earth_positions, _ = spice.spkpos('EARTH', times, 'J2000', 'NONE', 'SUN')
mars_positions, _ = spice.spkpos('MARS', times, 'J2000', 'NONE', 'SUN')

# Calculate distances between Earth and Mars
distances = np.linalg.norm(np.array(earth_positions) - np.array(mars_positions), axis=1)

# Plot the distances
plt.figure(figsize=(10, 5))
plt.plot([currTime + timedelta(days=i) for i in range(days)], distances)
plt.title('Distance Between Earth and Mars Over {} Years'.format(years))
plt.xlabel('Date')
plt.ylabel('Distance (km)')
plt.grid(True)
plt.show()

# Clear loaded kernels
spice.kclear()