
# MW 2023-03-20
# Python calculation of wave interference
# length unit: mm

import numpy as np
import matplotlib.pyplot as plt

# wave parameters
wavelength = 0.0005 # mm = 5000 Ångström, approx wavelength för green laser pointer
k = 2*np.pi/wavelength

# geometry parameters
d = 0.5 # separation between slits
D = 2000 # distance to detector screen
W = 20 # width of detector screen
points = 1000 # number of pixels of detector screen

#antal punktkällor per slit
N = 10
# source positions
xs = np.empty(N*2)

w = 0.05

#slit 1 points
for i in range(N):
    xs[i] = -d/2 - w/2 + i*w/(N-1)

#slit 2 points
for i in range(N):
    xs[N + i] = d/2 - w/2 + i*w/(N-1)

# compute time averaged intensity on a detector screen
screen = np.empty(points)
intensity = np.empty(points)

rs = np.empty(2*N)

for i in range(points):
    x = W*(i/(points-1)-0.5)
    screen[i] = x
    r = np.sqrt(D**2 + x**2)

    for j in range(len(xs)):
        rs[j] = np.sqrt(D**2 + (x-xs[j])**2)
    
    dubbelsumma = 0
    for j in range(0,len(xs) - 1):
        for h in range(j+1, len(xs)):
            dubbelsumma += np.cos(k*(rs[j]-rs[h]))

    intensity[i] = (len(xs)/2 + dubbelsumma)/r**2

#normalisera intensiteten
intensity = intensity/np.max(intensity)

plt.plot(screen,intensity)
plt.xlabel('x')
plt.ylabel('intensity')
plt.show()
