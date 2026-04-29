
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

# source positions
x1 = d/2
x2 = -d/2

# compute time averaged intensity on a detector screen
screen = np.empty(points)
intensity = np.empty(points)
for i in range(points):
    x = W*(i/(points-1)-0.5)
    screen[i] = x
    r = np.sqrt(D**2 + x**2)
    r1 = np.sqrt(D**2 + (x-x1)**2)
    r2 = np.sqrt(D**2 + (x-x2)**2)
    intensity[i] = (1 + np.cos(k*(r1-r2)))/r**2

plt.plot(screen,intensity)
plt.xlabel('x')
plt.ylabel('intensity')
plt.show()


def calculate_delta_x(wavelength, D, d):
    deltax = (wavelength*D)/d
    print(f"delta x är {deltax}")

calculate_delta_x(wavelength, D, d)


def calculate_delta_maxima(screen, intensity):
    peaks = []

    for i in range(1, len(intensity)-1):
        if intensity[i] > intensity[i-1] and intensity[i] > intensity[i+1]:
            peaks.append(screen[i])

    delta_maxima_sum = 0
    peaks = [p for p in peaks if p > 0]
    
    for i in range(0, len(peaks)-1):
        delta_maxima_sum += abs(peaks[i+1] - peaks[i])
    
    delta_maxima = delta_maxima_sum/(len(peaks)-1)
    
    print(f"delta maxima är {delta_maxima}")
    return delta_maxima

calculate_delta_maxima(screen, intensity)