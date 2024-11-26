# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from numpy.polynomial.polynomial import Polynomial

# %% [markdown]
# GET THCINESS TO CHORD RATIO AS A FUNCTION OF CHORDWISE POSITION

# %%
# Datapoints whitcomb integral supercritical
x_c = np.array([
    0.0, 0.0075, 0.0125, 0.0250, 0.0375, 0.0500, 0.0750, 0.1000, 0.1250, 0.1500,
    0.1750, 0.2000, 0.2500, 0.3000, 0.3500, 0.4000, 0.4500, 0.5000, 0.5500, 0.5750,
    0.6000, 0.6250, 0.6500, 0.6750, 0.7000, 0.7250, 0.7500, 0.7750, 0.8000, 0.8250,
    0.8500, 0.8750, 0.9000, 0.9250, 0.9500, 0.9750, 1.0000
])
y_u = np.array([
    0.0, 0.0176, 0.0215, 0.0276, 0.0316, 0.0347, 0.0394, 0.0428, 0.0455, 0.0476,
    0.0493, 0.0507, 0.0528, 0.0540, 0.0547, 0.0550, 0.0548, 0.0543, 0.0533, 0.0527,
    0.0519, 0.0511, 0.0501, 0.0489, 0.0476, 0.0460, 0.0442, 0.0422, 0.0398, 0.0370,
    0.0337, 0.0300, 0.0255, 0.0204, 0.0144, 0.0074, -0.0008
])

# Data: x/c and y_l (lower surface)
y_l = np.array([
    0.0, -0.0176, -0.0216, -0.0281, -0.0324, -0.0358, -0.0408, -0.0444, -0.0472,
    -0.0493, -0.0510, -0.0522, -0.0540, -0.0548, -0.0549, -0.0541, -0.0524, -0.0497,
    -0.0455, -0.0426, -0.0389, -0.0342, -0.0282, -0.0215, -0.0149, -0.0090, -0.0036,
    0.0012, 0.0053, 0.0088, 0.0114, 0.0132, 0.0138, 0.0131, 0.0106, 0.0060, -0.0013
])

# %%
# Compute t/c
t_c = y_u - y_l

# Fit a cubic spline
spline = CubicSpline(x_c, t_c)

# Fit a polynomial (4th degree)
coeffs = np.polyfit(x_c, t_c, deg=4)
poly_fit = np.poly1d(coeffs)

# Plotting
x_fine = np.linspace(0, 1, 500)
t_c_spline = spline(x_fine)
t_c_poly = poly_fit(x_fine)

# %%
plt.figure(figsize=(10, 6))
plt.plot(x_c, t_c, 'o', label="Original Data", markersize=8)
plt.plot(x_fine, t_c_spline, '-', label="Cubic Spline Fit")
#plt.plot(x_fine, t_c_poly, '--', label="Polynomial Fit (4th Degree)")
plt.xlabel("$x/c$", fontsize=14)
plt.ylabel("$t/c$", fontsize=14)
plt.title("Thickness-to-Chord Ratio Distribution", fontsize=16)
plt.legend()
plt.grid(True)
#plt.show()

# %%
# Plot the airfoil shape
plt.figure(figsize=(10, 6))
plt.plot(x_c, y_u, label="Upper Surface", color="blue")
plt.plot(x_c, y_l, label="Lower Surface", color="red")
plt.fill_between(x_c, y_u, y_l, color='lightgray', alpha=0.5)
plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
plt.xlabel("$x/c$", fontsize=14)
plt.ylabel("$y/c$", fontsize=14)
plt.title("Whitcomb Integral Supercritical Airfoil Shape", fontsize=16)
plt.legend()
plt.grid(True)
plt.axis('equal')  # Ensures correct aspect ratio
#plt.show()

# %%
def get_thickness(x_c):
    return spline(x_c)


# %%
get_thickness(0.5)

# %%



