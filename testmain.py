import spiceypy as spice
import os
from datetime import datetime, timedelta, timezone
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

DEBUG = False

def load_kern(name):
    print(f"{'[LOADING KERNEL]':<20}{name}")
    path = os.path.join(os.getcwd(), "kernelzzz")
    path = os.path.join(path, name)
    return str(path)

# test version
print(f"{'[VERSION]':<20}{spice.tkvrsn('TOOLKIT')}")
print(f"{'[DEBUG]':<20}{DEBUG}\n")

# leap second kernel
lsKP = load_kern('naif0012.tls')
# the ref data
ssKP = load_kern('de405.bsp')

#Load the leap second kernel
spice.furnsh(lsKP)
spice.furnsh(ssKP)

# all code between here unload at end
currTime = datetime.now()
ephTime = spice.str2et(str(currTime))
print('\n[START TIMES]')
print(f"{'[TIME UTC]':<20}{currTime}")
print(f"{'[EPHEMERIS TIME]':<20}{ephTime}")

# target frames for comparing earth to mars with equator j2000 ref
target = "EARTH"
observer = "MARS"
refrence = "J2000"

# params for times
years = 5
dis = 365 * years
if DEBUG:
    dis = 3

print(f"\n[GENERATING TIMES][{years} YEARS][DELTA][86400s]") if not DEBUG else print(f"\n[GENERATING TIMES][{dis} DAYS][DELTA][86400s]")

# making an array of all times
times = [spice.str2et(str(datetime.now() + timedelta(seconds = i * 86400))) for i in range(dis)]

# get earth position relative to mars
positions, lighttime = spice.spkpos(target, times, refrence, 'NONE', observer) 

print(*[f"{'[POSITION]':<15}{a}   {'[TIME]':<15}{b}" for a, b in zip(positions, lighttime)], sep='\n')

positions = positions.T 
fig = plt.figure(figsize=(9, 9))
ax  = fig.add_subplot(111, projection='3d')
ax.plot(positions[0], positions[1], positions[2])
plt.title(f'Earth Position Relative To Mars Across {years} Year(s)') if not DEBUG else plt.title(f'Earth Position Relative To Mars Across {dis} Day(s)')
plt.show()

spice.kclear()