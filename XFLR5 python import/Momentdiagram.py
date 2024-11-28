from XFLR5 import *
from matplotlib import pyplot as plt


halfspan = 13
dy = 0.1
rho = 0.5
V = 280
engine_weight = 1678.3 * 9.81
y_engine = 4.8
trust = 78500
r_engine = 1.7
engine_angle = 30
weight = 3374
volume = 12.47
density = weight / volume

V_list = []
y_list = []
M_list = []
y = 0
moment = 0
area = lambda x: (4.18 - 0.207936 * x)**2 * 0.11


while y <= halfspan:
    segment_lift = 0.5 * rho * V**2 * c(y) * cl(0, y)
    segment_weight = area(y) * density

    V_list.append(segment_lift - segment_weight) 
    y_list.append(y)   
    y += dy
    


for n in range(len(y_list)):
    y = y_list[n]  
    moment = 0

    for j in range(n, len(y_list)):
        arm = y_list[j] - y
        moment += arm * V_list[j] * dy

    if y < y_engine:
        moment += engine_weight * (y_engine - y) - trust * r_engine * np.sin(engine_angle)

    M_list.append(moment)

    
plt.plot(y_list, V_list)
plt.show()








