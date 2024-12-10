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
engine_angle = ma.radians(24) 
engine_hor_dist = 4.8
engine_x_ratio = 0.1 # this is the chordwise position of the engine. 
engine_y = 1.7
engine_weight = 16461.2 

#chord length is defined as c(y) = ay + b, with a = chord_a, and b = chord_b

chord_a = -2 * (1 - taper_ratio) * root_chord / span
chord_b = root_chord

def TorsionalConstant(front_spar_location,rear_spar_location,spar_t,skin_t,y):    

    chord = chord_a*y + chord_b
    delta_spar_location = rear_spar_location - front_spar_location

    spar_thickness = spar_t * chord / root_chord
    top_thickness = skin_t * chord / root_chord

    #the spar height is found using a separate function.
    front_spar_height = af.get_thickness(front_spar_location) * chord
    rear_spar_height = af.get_thickness(rear_spar_location) * chord
    delta_spar_height = af.get_thickness(front_spar_location) - af.get_thickness(rear_spar_location)

    #we define the enclosed area and the line integral
    enclosed_area = (front_spar_height + rear_spar_height)/2 * chord * (delta_spar_location)
    line_integral = front_spar_height * (1/spar_thickness) + rear_spar_height * (1/spar_thickness) + chord*ma.sqrt(spar_top_difference_ratio**2 + delta_spar_location**2) * (1/top_thickness) + chord*ma.sqrt((delta_spar_height - spar_top_difference_ratio)**2 + delta_spar_location**2) * (1/top_thickness)

    J = 4 * enclosed_area**2 / line_integral
    return(J)

def Torsion(alpha,load_factor,velocity,density,engine_thrust,resolution,centroid_x,centroid_y):
    
    #the torsion will be calculated in small quantaties based on the moment coefficient in the given location.
    #the torsion of all the parts will then be added together.

    Torsion_y = []
    Lift_torsion = []
    Moment_torsion = []

    i = 0
    while i < span/2:
        LocalTorsion = 0
        Lift_T = 0
        Moment_T = 0

        engine_chord = (chord_a*engine_hor_dist + chord_b)
        
        #engine contribution to the torsion
        if i <= engine_hor_dist:
            LocalTorsion += engine_thrust * (engine_y + centroid_y / root_chord * engine_chord) * ma.cos(engine_angle) * load_factor

        if i <= engine_hor_dist:
            LocalTorsion += -1 * (centroid_x / root_chord - engine_x_ratio) * engine_chord * engine_weight
        
        #lift contribution to the torsion
        k = i
        while k < span/2:
            cl = xl.cl(alpha,k)
            chord = chord_a*k + chord_b
            shear_centre_location = (centroid_x / root_chord * chord)
            load_location = 0.25 * chord
            S = chord * resolution
            L = cl*0.5*density*velocity**2*S
            LocalTorsion += L * (shear_centre_location - load_location) * load_factor
            Lift_T += L * (shear_centre_location - load_location) * load_factor
            k += resolution

        #moment contribution to the torsion
        j = i
        while j < span/2:
            cm = xl.cm(alpha,j)
            chord = chord_a*j + chord_b
            S = chord*resolution
            M = cm*chord*0.5*density*velocity**2*S
            LocalTorsion += M * load_factor
            Moment_T += M * load_factor
            j += resolution

        Torsion_y.append(round(LocalTorsion,3))
        Lift_torsion.append(round(Lift_T,3))
        Moment_torsion.append(round(Moment_T,3))

        i += resolution
    
    x = np.linspace(0,i-resolution,len(Torsion_y))

    return(x,Torsion_y,Lift_torsion,Moment_torsion)

#xtab = Torsion('a.txt',86.10,0.3,78500,0.1)[0]
#ytab = Torsion('a.txt',86.10,0.3,78500,0.1)[1]

def deformation(alpha,load_factor,velocity,density,engine_thrust,resolution,front_spar_location,rear_spar_location,spar_thickness,top_thickness,centroid_x,centroid_y):
    G = 28 * 10**9

    torsionf = Torsion(alpha,load_factor,velocity,density,engine_thrust,resolution,centroid_x,centroid_y)
    ytab = torsionf[0]
    torsion = torsionf[1]

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







