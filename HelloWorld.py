import numpy as np
import matplotlib.pyplot as plt

# Create 100 gaussian random points with mean 0 and variance 1
points = np.random.normal(0, 1, 100)

# Create a plot and plot the points
plt.figure()
plt.plot(points, '.')
plt.show()