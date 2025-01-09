import math as m
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
from scipy import interpolate

# List for aspect_ratio
aspectlist = [
    1.0229264102518605, 1.0386556077797888, 1.0622073569619204, 1.0975358753544742,
    1.138751883732883, 1.2079354824376531, 1.2918400426554513, 1.3768400642754188,
    1.4720700582382293, 1.5555988783262507, 1.6512784185157576, 1.7525712478583189,
    1.8423632980619713, 1.9630671308945913, 2.1029073190747907, 2.2383312188010818,
    2.4031948050050373, 2.5655315388362467, 2.7421718942506237, 2.909979672757186,
    3.0475681040167966, 3.222735468660515, 3.3993753767652146, 3.559494349211386,
    3.740549651150637, 3.9142462615720883, 4.102757321229333, 4.252901735158973,
    4.435430027868884, 4.623845363254972, 4.771512576186158, 4.934904960858168
]

# List for k_s
k_slist = [
    14.963701469294161, 14.583976423378719, 14.095611834682499, 13.635304046035937,
    13.247796652097872, 12.811060692364709, 12.38084326494397, 12.024958192300812,
    11.702269391287203, 11.45696819328667, 11.189617998123218, 10.870495174770788,
    10.663223921306592, 10.440932932417581, 10.215637813877235, 10.04741750738481,
    9.90022519561987, 9.795087504062103, 9.7169846972867, 9.695957615391077,
    9.707973221164554, 9.632875000456416, 9.566788255870422, 9.542756587907535,
    9.512718029889767, 9.491690491578213, 9.479674885804735, 9.479674885804735,
    9.48267855904014, 9.48267855904014, 9.488686361926879, 9.488686361926879
]

#Interpolate the aspect_ratio and k_s list to get a continuous function for K_s as a function of aspect ratio.
K_s = sp.interpolate.interp1d(aspectlist, k_slist, kind='cubic', fill_value="extrapolate")

#WARNING!! THESE ARE GUESSED!!
YoungModulus = 7e10
PoissonRatio = 0.33
SafetyFactor = 1.5
Kv = 1000


def calculate_tau_cr(FrontRibPos, BackRibPos, SheetHeight, SheetThickness, rootchord, taperratio, halfwingspan):
    sheetlength, sheetheight, AspectRatio = calculate_sheet_properties(FrontRibPos, BackRibPos, SheetHeight, taperratio, halfwingspan)
    Ks = K_s(AspectRatio)
    if AspectRatio <= 0.99999:
        Ks = 9999
        print("AR Lower than 1")
    tau_cr = abs(m.pi**2 * Ks * YoungModulus / (12*(1 - PoissonRatio**2)) * (SheetThickness / sheetheight)**2)
    return tau_cr, AspectRatio


def calculate_sheet_properties(rib1position, rib2position, sheetheight, taperratio, halfwingspan):
    sheetlength = (rib2position - rib1position)
    sheetheight = (sheetheight - (1 - taperratio) * sheetheight * rib2position/halfwingspan)
    AspectRatio = sheetlength / sheetheight
    return sheetlength, sheetheight, AspectRatio


def calculate_tau_max(t_f, t_r, h_f, h_r, V):
    #Use the open section shear flow formula making the assumption that I_xy = 0 (tau = VQ/It)
    I_xx = (t_f * h_f**3 + t_r * h_r**3) / 12
    Q_max_front = t_f * h_f**2 / 8
    Q_max_rear = t_r * h_r**2 / 8

    tau_max_front = abs(V) * Q_max_front / (I_xx * t_f)
    tau_max_rear = abs(V) * Q_max_rear / (I_xx * t_r)
    #print(tau_max_front)
    #print(tau_max_rear)

    return(max(tau_max_front, tau_max_rear))


def WebBuckle(RibPositionsList, halfwingspan, rootchord, taperratio, Shear, FrontSparHeight, FrontSparThick, BackSparHeight, BackSparThick):
    YList = [halfwingspan*i/141 for i in range(141)] #List of y positions where tau will be evaluated
    TauCritFrontList = []
    TauCritBackList = []
    TauMaxList = []
    ARList = []

    count = 0
    for i in range(141):
        while YList[i] >= RibPositionsList[count]:
            count += 1
        #Calculate the sheet properties for the current position in the iteration
        #sheetlength, sheetheight, AspectRatio = calculate_sheet_properties(RibPositionsList[count - 1], RibPositionsList[count], rootchord, taperratio, halfwingspan)
        #ARList.append(AspectRatio)
        #Break if the aspect ratio is lower than 1. Ks values lower than 1 are not in the table.
        
        #Calculate the tau_cr value and append it to a list
        TauCritFront = calculate_tau_cr(RibPositionsList[count - 1], RibPositionsList[count], FrontSparHeight, FrontSparThick, rootchord, taperratio, halfwingspan)[0]
        TauCritBack = calculate_tau_cr(RibPositionsList[count - 1], RibPositionsList[count], BackSparHeight, BackSparThick, rootchord, taperratio, halfwingspan)[0]
        TauCritFrontList.append(TauCritFront)
        TauCritBackList.append(TauCritBack)
        ARList.append(calculate_tau_cr(RibPositionsList[count - 1], RibPositionsList[count], FrontSparHeight, FrontSparThick, rootchord, taperratio, halfwingspan)[1])
        #Calculate the tau_max value and append it to a list
        TauMax = calculate_tau_max(FrontSparThick, BackSparThick, FrontSparHeight, BackSparHeight, Shear[i])
        TauMaxList.append(TauMax)
    if min(TauCritFrontList) < min(TauCritBackList): FinalTauCritList = TauCritFrontList
    else: FinalTauCritList = TauCritBackList
    Margin = [FinalTauCritList[i] / TauMaxList[i] for i in range(len(FinalTauCritList))]
    """
    plt.plot(YList, Margin)
    plt.ylim(0, 6)
    plt.show()
    """
    return(Margin, ARList)

    
DummyRibPos = [0, 4, 8, 13.75]
shear = [np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-545280.8917960676), np.float64(-540860.5177951403), np.float64(-535919.8682577291), np.float64(-530528.5361930899), np.float64(-524772.7374889603), np.float64(-518750.05157008604), np.float64(-512550.15416973946), np.float64(-506250.33450961474), np.float64(-499915.7379402768), np.float64(-493599.60858160973), np.float64(-487343.53196326585), np.float64(-481177.6776651143), np.float64(-475121.0419576897), np.float64(-469181.6904426411), np.float64(-463357.0006931805), np.float64(-457633.90489453165), np.float64(-451990.29492487997), np.float64(-446403.58963728294), np.float64(-440854.4035945278), np.float64(-435326.4964873489), np.float64(-429806.70655910886), np.float64(-424284.8840304791), np.float64(-418753.8245241213), np.float64(-413209.20248936786), np.float64(-407649.5046269031), np.float64(-402075.96331344405), np.float64(-396492.4900264215), np.float64(-390905.3166293086), np.float64(-385320.79041471484), np.float64(-379744.4128877071), np.float64(-374180.8538270828), np.float64(-368633.9699397293), np.float64(-363106.8235149841), np.float64(-357601.7010789942), np.float64(-352120.13204907626), np.float64(-363127.0303880763), np.float64(-357694.22125872946), np.float64(-352285.1977103524), np.float64(-346898.82430083014), np.float64(-341534.0617282169), np.float64(-336190.0867951195), np.float64(-330866.2872198939), np.float64(-325562.25644784165), np.float64(-320277.7884624068), np.float64(-315012.8725963724), np.float64(-309767.6883430573), np.float64(-304542.6001675126), np.float64(-299338.1523177184), np.float64(-294155.05238247593), np.float64(-288994.03431731457), np.float64(-283855.77171192894), np.float64(-278740.8777579588), np.float64(-273649.90672530077), np.float64(-268583.3554384204), np.float64(-263541.6647526638), np.float64(-258525.22103056998), np.float64(-253534.35761818223), np.float64(-248569.35632136033), np.float64(-243630.45221970958), np.float64(-238717.8722650991), np.float64(-233831.85873992817), np.float64(-228972.66910406714), np.float64(-224140.57547148672), np.float64(-219335.8640868869), np.float64(-214558.83480232614), np.float64(-209809.80055385045), np.float64(-205089.08683812246), np.float64(-200397.03117911422), np.float64(-195733.9794321268), np.float64(-191100.27772661115), np.float64(-186496.27117903702), np.float64(-181922.30377176095), np.float64(-177378.71823189454), np.float64(-172865.8559101725), np.float64(-168384.05665982087), np.float64(-163933.6587154251), np.float64(-159514.99859311112), np.float64(-155128.41492466794), np.float64(-150774.25669803683), np.float64(-146452.88378640625), np.float64(-142164.66633248163), np.float64(-137909.98413275502), np.float64(-133689.22602177478), np.float64(-129502.7892564154), np.float64(-125351.07890014713), np.float64(-121234.50883559478), np.float64(-117153.51107155094), np.float64(-113108.53845158132), np.float64(-109100.06343928904), np.float64(-105128.57689575158), np.float64(-101194.58685695782), np.float64(-97298.61731124499), np.float64(-93441.2070139604), np.float64(-89622.9208815364), np.float64(-85844.37889693894), np.float64(-82106.25761570914), np.float64(-78409.28690197902), np.float64(-74754.24666448732), np.float64(-71141.96359259525), np.float64(-67573.30796991994), np.float64(-64049.208706612946), np.float64(-60570.69063376689), np.float64(-57138.87418898149), np.float64(-53754.96913739785), np.float64(-50420.268292732806), np.float64(-47136.14123831328), np.float64(-43904.084629986566), np.float64(-40725.9498180215), np.float64(-37603.98392256178), np.float64(-34540.80594311205), np.float64(-31539.382867607783), np.float64(-28603.00794263792), np.float64(-25735.311684230062), np.float64(-22940.26427760021), np.float64(-20222.149027283693), np.float64(-17585.534947757656), np.float64(-15036.02870074973), np.float64(-12583.133572213992), np.float64(-10240.700994158202), np.float64(-8026.614795566912), np.float64(-5960.1073774274355), np.float64(-4057.905230682666), np.float64(-2337.7174086432797), np.float64(-888.0750140061855), np.float64(74.22706081528386), np.float64(48.68486247806189), np.float64(23.946795971536186)]
#print(WebBuckle(DummyRibPos, 13.75, 4.2, 0.3, shear, 0.75, 0.01, 0.75, 0.01))

# TauAve = [1.5 * Kv * Shear[i]/((FrontSparHeight*FrontSparThick + BackSparHeight*BackSparThick)*(1 - (1 - taperratio)*i/141)**2) for i in range(141)]
#The Wing Loading is variable, so the shear force experienced at each point changes aswell!
#Plate Thickness and Plate Height are variable along the wingspan, so our critical shear will be a function of the wingspan.
#AverageShear = ()
#ShearCrit = (m.pi**2 * Ks * YoungModulus)/12*(1 - PoissonRatio**2) * (PlateThickness/P
#ShearCrit = (m.pi**2 * Ks * YoungModulus)/12*(1 - PoissonRatio**2) * (PlateThickness/PlateHeight)**2
