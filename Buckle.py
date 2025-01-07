import math as m
import matplotlib.pyplot as plt

#WARNING!! THESE ARE GUESSED!!
YoungModulus = 7e10
Ks = 0
PoissonRatio = 0.6

def WebBuckle(RibPositionsList, halfwingspan, rootchord, taperratio, PlateThickness, PlateHeight):

    #First, to get the Ks along the wingspan! This requires the aspect ratio

    XList = [halfwingspan*i/141 for i in range(141)]
    print(len(XList))
    ARList = []
    count = 0
    for i in range(141):
        while XList[i] >= RibPositionsList[count]:
            print(count, XList[i], RibPositionsList[count])
            count += 1
        ARList.append((RibPositionsList[count] - RibPositionsList[count - 1]) / (rootchord - (1 - taperratio) * rootchord * RibPositionsList[count]/halfwingspan))
        
    plt.plot(XList, ARList)
    plt.show()


    #The Wing Loading is variable, so the shear force experienced at each point changes aswell!

    #Plate Thickness and Plate Height are variable along the wingspan, so our critical shear will be a function of the wingspan.

    #AverageShear = ()
    #ShearCrit = (m.pi**2 * Ks * YoungModulus)/12*(1 - PoissonRatio**2) * (PlateThickness/PlateHeight)**2

DummyRibPos = [0, 2, 5, 7, 9, 13.75]
WebBuckle(DummyRibPos, 13.75, 4.2, 0.3, 0, 0)