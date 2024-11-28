from Momentdiagram import *
import numpy as np


lamb = 0.316
E = 70E9
I_root = 0.0001

def I(y):
    I = I_root * (1-y*((1-lamb)/(halfspan)))**4 ###################
    return(I)



angle_list = []
displacement_list = []
angle = 0

for M, y in zip(M_list, y_list):
    angle_list.append(angle)
    angle += 1/(E*I(y)) * -M * dy
    
displacement = 0
for angle in angle_list:
    displacement_list.append(displacement)
    displacement += angle * dy

plt.plot(y_list, displacement_list)
plt.show()
