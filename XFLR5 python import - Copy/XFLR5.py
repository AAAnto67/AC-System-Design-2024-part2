import scipy as sp 
from scipy import interpolate
import numpy as np


#function that returns a function of the cl along the wingspan
def cldist(data):

    # Read all lines and store them as a list
    with open(data, "r") as file:
        wingloading = file.readlines()

    #create empty lists for y position and cm
    y = []
    cldata = []

    #loop over line 21 up until 59 and ad the corresponding values for y and cl in the correct list
    for i in range(38):
        y.append(float(wingloading[21+i].split()[0].strip(',')))
        cldata.append(float(wingloading[21+i].split()[3].strip(',')))

    #interpolate the y and cldata list with cubic interpolation and return function
    cl = sp.interpolate.interp1d(y,cldata,kind='cubic',fill_value="extrapolate") 
    file.close()
    return(cl)


#function that returns a function of the cm along the wingspan
def cmdist(data):

    # Read all lines and store them as a list
    with open(data, "r") as file:   
        moment = file.readlines()

    #create empty lists for y position and cm
    y = []
    cmdata = []

    #loop over line 21 up until 59 and ad the corresponding values for y and cm in the correct list
    for i in range(38):
        y.append(float(moment[21+i].split()[0].strip(',')))
        cmdata.append(float(moment[21+i].split()[6].strip(',')))

    #interpolate the y and cmdata list with cubic interpolation and return function
    cm = sp.interpolate.interp1d(y,cmdata,kind='cubic',fill_value="extrapolate") 
    return(cm)


#function that returns a function of the c along the wingspan
#chord = cr - |y| * (cr - ct)/(b/2)
def c(y):
    if abs(y) > 13.7265:
        c = 0
    else:  
        c = 4.18 - abs(y) * 0.2083 
    return(c)


#Open 'MainWing_a=0.00_v=10.00ms.txt' as FXLR0
with open('MainWing_a=0.00_v=10.00ms.txt', "r") as file:   
        XFLR0 = file.readlines()
file.close


#open 'MainWing_a=10.00_v=10.00ms.txt' as FXLR10
with open('MainWing_a=10.00_v=10.00ms.txt', "r") as file:   
        XFLR10 = file.readlines()
file.close

#Store lift coefficient for the whole wing at 0 and 10 deg
CL0 = float(XFLR0[9].split()[2].strip(','))
CL10 = float(XFLR10[9].split()[2].strip(','))

#Store spanwise lift coefficient at 0 and 10 deg
cl0 = cldist('MainWing_a=0.00_v=10.00ms.txt')
cl10 = cldist('MainWing_a=10.00_v=10.00ms.txt')

#Store spanwise moment coefficient at 0 and 10 deg
cm0 = cmdist('MainWing_a=0.00_v=10.00ms.txt') 
cm10 = cmdist('MainWing_a=10.00_v=10.00ms.txt') 


#Define a function that calculates the total wing CL at any angle of attack
def CL(alpha):
    CLd = (alpha / 10) * (CL10 - CL0) + CL0
    return(CLd)


#Define a function that calculates the section cl for any angle of attack and position
def cl(alpha, y):
    cld = cl0(y) + ((CL(alpha) - CL0) / (CL10 - CL0)) * cl10(y) - cl0(y) 
    return(cld) 

#Results of this python code:
#   section:
#       cl(alpha, y) -----> section cl at (alpha, y)
#       cl0(y)       -----> section cl at (0, y)
#       cl10(y)      -----> section cl at (10, y)
#       cm0(y)       -----> section cm at (0, y)
#       cm10(y)      -----> section cm at (10, y)
#
#   wing:
#       CL(alpha)    -----> wing    CL at alpha
#       CL0          -----> wing    CL at alpha = 0
#       CL10         -----> wing    CL at alpha = 10



