from XFLR5 import *
from matplotlib import pyplot as plt


halfspan = 14
samples = 100
step = halfspan/samples
rho = 0.5
V = 120
Wengine = 1678.3 * 9.81
yengine = 4.8

Llist = []
ylist = []
Mlist = []
i = 0
moment = 0

while i <= halfspan:
    if abs(i - yengine)<step:
        Llist.append(0.5 * rho * V**2 * c(i) * step * cl(2, i) - Wengine)

    else:
        Llist.append(0.5 * rho * V**2 * c(i) * step * cl(2, i))
        
    ylist.append(i)
    i += step

k=0
n=0
while k <= halfspan:
    for j in range(len(ylist) - n):
        moment += ylist[j + n] * Llist[j + n]
    Mlist.append(moment)
    moment = 0
    k += step
    n += 1

plt.plot(ylist, Mlist)
plt.show()







