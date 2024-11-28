import math as ma
import scipy as sp
import numpy as np
import airfoil as af
import XFLR5 as xl
import matplotlib.pyplot as plt

#with the spar top difference, I'm referring to the height difference between the tops of the spars.
spar_top_difference_ratio = 0.0507 - 0.0476

taper_ratio = 0.316
root_chord = 4.18
span = 27.5

#the engine will create a point torque on the wing
engine_angle = ma.radians(29.4) 
engine_hor_dist = 4.8
engine_vert_dist = 1.7

#chord length is defined as c(y) = ay + b, with a = chord_a, and b = chord_b

chord_a = -2 * (1 - taper_ratio) * root_chord / span
chord_b = root_chord

def TorsionalConstant(front_spar_location,rear_spar_location,spar_thickness,top_thickness,y):    

    chord = chord_a*y + chord_b
    delta_spar_location = rear_spar_location - front_spar_location

    #the spar height is found using a separate function.
    front_spar_height = af.get_thickness(front_spar_location) * chord
    rear_spar_height = af.get_thickness(rear_spar_location) * chord
    delta_spar_height = af.get_thickness(front_spar_location) - af.get_thickness(rear_spar_location)

    #we define the enclosed area and the line integral
    enclosed_area = (front_spar_height + rear_spar_height)/2 * chord * (delta_spar_location)
    line_integral = front_spar_height * (1/spar_thickness) + rear_spar_height * (1/spar_thickness) + chord*ma.sqrt(spar_top_difference_ratio**2 + delta_spar_location**2) * (1/top_thickness) + chord*ma.sqrt((delta_spar_height - spar_top_difference_ratio)**2 + delta_spar_location**2) * (1/top_thickness)

    J = 4 * enclosed_area**2 / line_integral
    return(J)

def Torsion(data,velocity,density,engine_thrust,resolution):
    
    #the torsion will be calculated in small quantaties based on the moment coefficient in the given location.
    #the torsion of all the parts will then be added together.

    Torsion_y = []
    
    cmy = xl.cmdist(data)

    i = 0
    while i < span/2:
        LocalTorsion = 0
        if i <= engine_hor_dist:
            LocalTorsion += engine_thrust * engine_vert_dist * ma.cos(engine_angle)
        j = i
        while j < span/2:
            cm = cmy(j+resolution/2)
            chord = chord_a*i + chord_b
            S = chord*resolution
            M = cm*chord*0.5*density*velocity**2*S
            LocalTorsion += M
            j += resolution
        Torsion_y.append(round(LocalTorsion,3))
        i += resolution
    
    x = np.linspace(0,i-resolution,len(Torsion_y))

    return(x,Torsion_y)

#xtab = Torsion('a.txt',86.10,0.3,78500,0.1)[0]
#ytab = Torsion('a.txt',86.10,0.3,78500,0.1)[1]

def deformation(data,velocity,density,engine_thrust,resolution,front_spar_location,rear_spar_location,spar_thickness,top_thickness):
    G = 28 * 10**9
    ytab = Torsion(data,velocity,density,engine_thrust,resolution)[0]
    torsion = Torsion(data,velocity,density,engine_thrust,resolution)[1]

    diffdeformation = []
    for i in range(len(ytab)):
        diffdeformation.append(torsion[i] / G / TorsionalConstant(front_spar_location,rear_spar_location,spar_thickness,top_thickness,ytab[i]) * 180 / 3.1415)

    #print(len(diffdeformation))

    totaldeformation = []
    for i in range(len(ytab)):
        localdeformation = 0
        j = 0
        while j <= i:
            localdeformation += diffdeformation[int(j)] * resolution
            j += 1
        totaldeformation.append(localdeformation)
    
    tipdeformation = totaldeformation[-1] 

    return(diffdeformation,totaldeformation,tipdeformation)

#y = deformation('a.txt',86.10,0.3,0.05,0.2,0.7,0.01,0.01)

#print("the deformation at the tip is " + str(y[2]) + " degrees.")



