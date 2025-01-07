import math as m
import matplotlib.pyplot as plt

# List x (aspect_ratio)
x = [
    1.0229264102518605, 1.0386556077797888, 1.0622073569619204, 1.0975358753544742,
    1.138751883732883, 1.2079354824376531, 1.2918400426554513, 1.3768400642754188,
    1.4720700582382293, 1.5555988783262507, 1.6512784185157576, 1.7525712478583189,
    1.8423632980619713, 1.9630671308945913, 2.1029073190747907, 2.2383312188010818,
    2.4031948050050373, 2.5655315388362467, 2.7421718942506237, 2.909979672757186,
    3.0475681040167966, 3.222735468660515, 3.3993753767652146, 3.559494349211386,
    3.740549651150637, 3.9142462615720883, 4.102757321229333, 4.252901735158973,
    4.435430027868884, 4.623845363254972, 4.771512576186158, 4.934904960858168
]

# List y (k_s)
y = [
    14.963701469294161, 14.583976423378719, 14.095611834682499, 13.635304046035937,
    13.247796652097872, 12.811060692364709, 12.38084326494397, 12.024958192300812,
    11.702269391287203, 11.45696819328667, 11.189617998123218, 10.870495174770788,
    10.663223921306592, 10.440932932417581, 10.215637813877235, 10.04741750738481,
    9.90022519561987, 9.795087504062103, 9.7169846972867, 9.695957615391077,
    9.707973221164554, 9.632875000456416, 9.566788255870422, 9.542756587907535,
    9.512718029889767, 9.491690491578213, 9.479674885804735, 9.479674885804735,
    9.48267855904014, 9.48267855904014, 9.488686361926879, 9.488686361926879
]

#WARNING!! THESE ARE GUESSED!!
YoungModulus = 7e10
PoissonRatio = 0.6

def FindKs(AR):

def WebBuckle(RibPositionsList, halfwingspan, rootchord, taperratio, PlateThickness, PlateHeight):

    #First, to get the Ks along the wingspan! This requires the aspect ratio

    YList = [halfwingspan*i/141 for i in range(141)]
    KsList = []
    count = 0
    for i in range(141):
        while XList[i] >= RibPositionsList[count]:
            count += 1
        KsList.append(FindKs((RibPositionsList[count] - RibPositionsList[count - 1]) / (rootchord - (1 - taperratio) * rootchord * RibPositionsList[count]/halfwingspan)))
    

    plt.plot(YList, KsList)
    plt.show()


    #The Wing Loading is variable, so the shear force experienced at each point changes aswell!

    #Plate Thickness and Plate Height are variable along the wingspan, so our critical shear will be a function of the wingspan.

    #AverageShear = ()
    #ShearCrit = (m.pi**2 * Ks * YoungModulus)/12*(1 - PoissonRatio**2) * (PlateThickness/PlateHeight)**2

DummyRibPos = [0, 2, 5, 7, 9, 13.75]
WebBuckle(DummyRibPos, 13.75, 4.2, 0.3, 0, 0)
DummyRibPos = [0, 2, 5, 7, 9, 13.75]
WebBuckle(DummyRibPos, 13.75, 4.2, 0.3, 0, 0)
