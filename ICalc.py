import numpy as np
from tkinter import *
import math as m
import StiffnessCalculations
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import Displacement
import LoadCases
import ShearForceDiagram
import MaximumStressLocation
import Momentdiagram
import ColumnBuckling

root = Tk()
root.config(bg="gray")

ThrustToWeight = 0.42

Offset = 50
RootChord = 4.26
HalfWingSpan = StiffnessCalculations.span/2
ScalingFactor = 2000
CanvasDimensions = [2200, 400]

resolutionTom = 0.05

f = open("AirfoilCharacteristics.txt", "r")
f.readline()
CurrentLine = f.readline()
FinalAirfoilPoints = [0], [0], [0]
#Read the airfoil thingamajig
while CurrentLine != "\\n":
    CurrentLine = CurrentLine.split(" ")
    while "" in CurrentLine:
        CurrentLine.pop(CurrentLine.index(""))
    if float(CurrentLine[0]) == 1:
        FinalAirfoilPoints[0].append(1)
        FinalAirfoilPoints[1].append(float(CurrentLine[1]))
        break
    else:
        FinalAirfoilPoints[0].append(float(CurrentLine[0]))
        FinalAirfoilPoints[1].append(float(CurrentLine[1]))
    CurrentLine = f.readline()
f.readline()
f.readline()
CurrentLine = f.readline()
while CurrentLine != "\\n":
    CurrentLine = CurrentLine.split(" ")
    while "" in CurrentLine:
        CurrentLine.pop(CurrentLine.index(""))
    if float(CurrentLine[0]) == 1:
        FinalAirfoilPoints[2].append(float(CurrentLine[1]))
        break
    else:
        FinalAirfoilPoints[2].append(float(CurrentLine[1]))
    CurrentLine = f.readline()
f.close()

def FindClosest(List, value):
    difference = 1000
    differenceValue = 0
    for i in range (len(List)):
        if abs(abs(List[i]) - abs(value)) < difference:
            difference = abs(abs(List[i]) - abs(value))
            differenceValue = i
    return(differenceValue)

def CalcIndividualI(ListOfCoord, StringerPositionsTop, StringerPositionsBot, StringerArea, StringerNumTop, StringerNumBot):
    TopRectangle = [ListOfCoord[1][0] - ListOfCoord[0][0], min([ListOfCoord[0][1], ListOfCoord[1][1]]), min([ListOfCoord[0][1], ListOfCoord[1][1]])/2, (ListOfCoord[1][0] - ListOfCoord[0][0])/2 + ListOfCoord[0][0]] #horizontal length, vertical length, Y centroid, X Centroid
    TopTriangle = [TopRectangle[0], (max([ListOfCoord[0][1], ListOfCoord[1][1]]) - TopRectangle[1]), (TopRectangle[1] + (max([ListOfCoord[0][1], ListOfCoord[1][1]]) - TopRectangle[1])/3), -(ListOfCoord[0][1] - ListOfCoord[1][1])/abs(ListOfCoord[0][1] - ListOfCoord[1][1]) * TopRectangle[0]/6 + TopRectangle[3]] #Horizontal  length, vertical length, Y centroid, X centroid FUNNY CODE DONT ASK ME HOW IT WORKS HIHI :)))
    BotRectangle = [ListOfCoord[3][0] - ListOfCoord[2][0], max([ListOfCoord[2][1], ListOfCoord[3][1]]), max([ListOfCoord[2][1], ListOfCoord[3][1]])/2, (ListOfCoord[1][0] - ListOfCoord[0][0])/2 + ListOfCoord[0][0]] #horizontal length, vertical length, Y centroid, X centroid
    BotTriangle = [BotRectangle[0], (min([ListOfCoord[2][1], ListOfCoord[3][1]]) - BotRectangle[1]), (BotRectangle[1] + (min([ListOfCoord[2][1], ListOfCoord[3][1]]) - BotRectangle[1])/3), (ListOfCoord[0][1] - ListOfCoord[1][1])/abs(ListOfCoord[0][1] - ListOfCoord[1][1]) * TopRectangle[0]/6 + TopRectangle[3]] #Horizontal  length, vertical length, Y centroid, X centroid
    #IMPORTANT if the top or Bot rectangles are both ABOVE or BELOW the chord line the centroid WILL BE WRONGG!!!

    TopStringersContribution = 0
    BotStringersContribution = 0

    for i in range(len(StringerPositionsTop[0])):
        TopStringersContribution += StringerPositionsTop[0][i] * StringerArea
    for i in range(len(StringerPositionsBot[0])):
        BotStringersContribution += StringerPositionsBot[0][i] * StringerArea
    

    FinalYCentroid = (TopRectangle[0]*TopRectangle[1]*TopRectangle[2] + TopTriangle[0]*TopTriangle[1]*TopTriangle[2]*0.5 + BotRectangle[0]*BotRectangle[1]*BotRectangle[2] + BotTriangle[0]*BotTriangle[1]*BotTriangle[2]*0.5 + TopStringersContribution + BotStringersContribution)/(TopRectangle[0]*TopRectangle[1] + TopTriangle[0]*TopTriangle[1]*0.5 + BotRectangle[0]*BotRectangle[1] + BotTriangle[0]*BotTriangle[1]*0.5 + StringerArea*(StringerNumBot + StringerNumTop))
    #FinalYCentroid = (TopStringersContribution + BotStringersContribution)/(StringerArea*(StringerNumBot + StringerNumTop))
    FinalXCentroid = (TopRectangle[0]*TopRectangle[1]*TopRectangle[3] + TopTriangle[0]*TopTriangle[1]*TopTriangle[3]*0.5 + BotRectangle[0]*BotRectangle[1]*BotRectangle[3] + BotTriangle[0]*BotTriangle[1]*BotTriangle[3]*0.5)/(TopRectangle[0]*TopRectangle[1] + TopTriangle[0]*TopTriangle[1]*0.5 + BotRectangle[0]*BotRectangle[1] + BotTriangle[0]*BotTriangle[1]*0.5)

    ITopRectangle = (TopRectangle[0]*TopRectangle[1]**3)/12 + TopRectangle[0]*TopRectangle[1]*(TopRectangle[2] - FinalYCentroid)**2
    ITopTriangle = (TopTriangle[0]*TopTriangle[1]**3)/36 + 0.5*TopTriangle[0]*TopTriangle[1]*(TopTriangle[2] - FinalYCentroid)**2
    IBotRectangle = (BotRectangle[0]*BotRectangle[1]**3)/12 + BotRectangle[0]*BotRectangle[1]*(BotRectangle[2] - FinalYCentroid)**2
    IBotTriangle = (BotTriangle[0]*BotTriangle[1]**3)/36 + 0.5*BotTriangle[0]*BotTriangle[1]*(BotTriangle[2] - FinalYCentroid)**2

    return((ITopRectangle + ITopTriangle + IBotRectangle + IBotTriangle), (FinalYCentroid), FinalXCentroid)

def CalcString(StringX, ListOfSecondCoord, Angle, Stringheight):
    StringY = StringX * m.tan(Angle) + Stringheight
    #C.create_line(ScalingFactor*(StringX + ListOfSecondCoord[0][0])/RootChord + Offset, CanvasDimensions[1], ScalingFactor*(StringX + ListOfSecondCoord[0][0])/RootChord + Offset, -ScalingFactor*(StringY)/RootChord + CanvasDimensions[1]*0.5)
    return(StringY)

def Main(FrontSparX, BackSparX, HThickness, VThickness, StringNumTop, StringNumBot, StringArea, debug, StringerThicc, StringerLength, StringerHeight, TomPositions):
    HThickness = HThickness/1000
    VThickness = VThickness/1000
    FrontSparTop = FinalAirfoilPoints[1][FindClosest(FinalAirfoilPoints[0], FrontSparX/RootChord)]*RootChord
    FrontSparBot = -FinalAirfoilPoints[2][FindClosest(FinalAirfoilPoints[0], FrontSparX/RootChord)]*RootChord
    BackSparTop = FinalAirfoilPoints[1][FindClosest(FinalAirfoilPoints[0], BackSparX/RootChord)]*RootChord
    BackSparBot = -FinalAirfoilPoints[2][FindClosest(FinalAirfoilPoints[0], BackSparX/RootChord)]*RootChord

    #Calculating I
    ListOfCoord = [FrontSparX, FrontSparTop], [BackSparX, BackSparTop], [BackSparX, -BackSparBot], [FrontSparX, -FrontSparBot]
    TopAngle = m.atan((ListOfCoord[1][1] - ListOfCoord[0][1])/(ListOfCoord[1][0] - ListOfCoord[0][0]))
    BotAngle = -m.atan((ListOfCoord[3][1] - ListOfCoord[2][1])/(ListOfCoord[1][0] - ListOfCoord[0][0]))
    ListOfSecondCoord = [FrontSparX + HThickness, FrontSparTop - VThickness*m.cos(abs(TopAngle))], [BackSparX - HThickness, BackSparTop - VThickness*m.cos(abs(TopAngle))], [BackSparX - HThickness, -BackSparBot + VThickness*m.cos(abs(BotAngle))], [FrontSparX + HThickness, -FrontSparBot + VThickness*m.cos(abs(BotAngle))]
    StringerPositionsTop = [CalcString((ListOfSecondCoord[1][0] - ListOfSecondCoord[0][0])/(StringNumTop - 1)*i, ListOfSecondCoord, TopAngle, ListOfSecondCoord[0][1]) for i in range(StringNumTop)], [FrontSparX + (BackSparX - FrontSparX) * i/(StringNumTop - 1) for i in range(StringNumTop)] #1st list is the Y pos of each stringer, 2nd list is the X pos of each stringer (FOR THE TOP ONES)
    StringerPositionsBot = [CalcString((ListOfSecondCoord[1][0] - ListOfSecondCoord[0][0])/(StringNumBot - 1)*i, ListOfSecondCoord, BotAngle, ListOfSecondCoord[3][1]) for i in range(StringNumBot)], [FrontSparX + (BackSparX - FrontSparX) * i/(StringNumBot - 1) for i in range(StringNumBot)] #same thing as the list before but for the bottom stringers
    
    FinalYCentroid = CalcIndividualI(ListOfCoord, StringerPositionsTop, StringerPositionsBot, StringArea, StringNumTop, StringNumBot)[1]
    FinalXCentroid = CalcIndividualI(ListOfCoord, StringerPositionsTop, StringerPositionsBot, StringArea, StringNumTop, StringNumBot)[2]

    StringersTotalI = 0
    for i in range(StringNumTop):
        StringersTotalI += (CalcString((ListOfSecondCoord[1][0] - ListOfSecondCoord[0][0])/(StringNumTop - 1)*i, ListOfSecondCoord, TopAngle, ListOfSecondCoord[0][1]))**2 * StringArea
    for i in range(StringNumBot):
        StringersTotalI += (CalcString((ListOfSecondCoord[1][0] - ListOfSecondCoord[0][0])/(StringNumBot - 1)*i, ListOfSecondCoord, BotAngle, ListOfSecondCoord[3][1]))**2 * StringArea

    #Rendering everything
    C.coords(Box, ListOfCoord[0][0]*ScalingFactor/RootChord + Offset, -ListOfCoord[0][1]*ScalingFactor/RootChord + CanvasDimensions[1]*0.5, 
                    ListOfCoord[1][0]*ScalingFactor/RootChord + Offset, -ListOfCoord[1][1]*ScalingFactor/RootChord + CanvasDimensions[1]*0.5, 
                    ListOfCoord[2][0]*ScalingFactor/RootChord + Offset, -ListOfCoord[2][1]*ScalingFactor/RootChord + CanvasDimensions[1]*0.5, 
                    ListOfCoord[3][0]*ScalingFactor/RootChord + Offset, -ListOfCoord[3][1]*ScalingFactor/RootChord + CanvasDimensions[1]*0.5)
    C.coords(InsideBox, ListOfSecondCoord[0][0]*ScalingFactor/RootChord + Offset, -ListOfSecondCoord[0][1]*ScalingFactor/RootChord + CanvasDimensions[1]*0.5, 
                    ListOfSecondCoord[1][0]*ScalingFactor/RootChord + Offset, -ListOfSecondCoord[1][1]*ScalingFactor/RootChord + CanvasDimensions[1]*0.5, 
                    ListOfSecondCoord[2][0]*ScalingFactor/RootChord + Offset, -ListOfSecondCoord[2][1]*ScalingFactor/RootChord + CanvasDimensions[1]*0.5, 
                    ListOfSecondCoord[3][0]*ScalingFactor/RootChord + Offset, -ListOfSecondCoord[3][1]*ScalingFactor/RootChord + CanvasDimensions[1]*0.5)
    C.coords(FinalYCentroidLine, Offset + FinalXCentroid * ScalingFactor/RootChord - 10, - FinalYCentroid*ScalingFactor/RootChord + CanvasDimensions[1]*0.5, 
                                      Offset + FinalXCentroid * ScalingFactor/RootChord + 10, -FinalYCentroid*ScalingFactor/RootChord + CanvasDimensions[1]*0.5)
    C.coords(FinalXCentroidLine, Offset + FinalXCentroid * ScalingFactor/RootChord,-10 - FinalYCentroid*ScalingFactor/RootChord + CanvasDimensions[1]*0.5, 
                                      Offset + FinalXCentroid * ScalingFactor/RootChord,10 -FinalYCentroid*ScalingFactor/RootChord + CanvasDimensions[1]*0.5)

    FinalI = CalcIndividualI(ListOfCoord, StringerPositionsTop, StringerPositionsBot, StringArea, StringNumTop, StringNumBot)[0] - CalcIndividualI(ListOfSecondCoord, StringerPositionsTop, StringerPositionsBot, StringArea, StringNumTop, StringNumBot)[0] + StringersTotalI

    ax.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    ax6.clear()

    if debug == 0 or debug == 1:

        LargestTorque = 0
        LargestBending = 0
        TorqueCrit = 0
        BendCrit = 0

        if debug == 0:
            for i in range(len(LoadCases.WeightsList)):
                TorqueList = StiffnessCalculations.deformation(LoadCases.AoAList[i],LoadCases.LoadFactorsList[i], LoadCases.SpeedFactorsList[i],LoadCases.DensitiesList[i], LoadCases.WeightsList[i] * ThrustToWeight,resolutionTom,FrontSparX/RootChord,BackSparX/RootChord,HThickness,VThickness, FinalXCentroid, FinalYCentroid) #data, velocity, density, engine thrust, resolution, frontspar (ratio), backspar (ratio), spar thickness, top thickness
                DeformList = Displacement.CalcDisplace(FinalI, LoadCases.WeightsList[i], LoadCases.SpeedFactorsList[i], LoadCases.DensitiesList[i], LoadCases.AoAList[i], LoadCases.LoadFactorsList[i])
                XList = [round(resolutionTom * i, 3) for i in range(len(TorqueList[0]))], [HalfWingSpan * i/len(DeformList[0]) for i in range(len(DeformList[0]))]

                ax.plot(XList[0], TorqueList[0])
                ax2.plot(XList[0], TorqueList[1])
                ax3.plot(XList[1], DeformList[1])
                ax4.plot(XList[1], DeformList[0])

                print(i)

                if TorqueList[1][-1] < LargestTorque:
                    LargestTorque = TorqueList[1][-1]
                    TorqueCrit = i + 1
                if DeformList[0][-1] < LargestBending:
                    LargestBending = DeformList[0][-1]
                    BendCrit = i + 1
        if debug == 1:
            TorqueList = StiffnessCalculations.deformation(LoadCases.AoAList[56],LoadCases.LoadFactorsList[56],LoadCases.SpeedFactorsList[56],LoadCases.DensitiesList[56], LoadCases.WeightsList[56] * ThrustToWeight,resolutionTom,FrontSparX/RootChord,BackSparX/RootChord,HThickness,VThickness, FinalXCentroid, FinalYCentroid) #data, velocity, density, engine thrust, resolution, frontspar (ratio), backspar (ratio), spar thickness, top thickness
            DeformList = Displacement.CalcDisplace(FinalI, LoadCases.WeightsList[56], LoadCases.SpeedFactorsList[56], LoadCases.DensitiesList[56], LoadCases.AoAList[56], LoadCases.LoadFactorsList[56])
            XList = [round(resolutionTom * i, 3) for i in range(len(TorqueList[0]))], [HalfWingSpan * i/len(DeformList[0]) for i in range(len(DeformList[0]))]
            ax.plot(XList[0], TorqueList[0])
            ax2.plot(XList[0], TorqueList[1])
            ax3.plot(XList[1], DeformList[1])
            ax4.plot(XList[1], DeformList[0])
            TorqueList = StiffnessCalculations.deformation(LoadCases.AoAList[27],LoadCases.LoadFactorsList[27],LoadCases.SpeedFactorsList[27],LoadCases.DensitiesList[27], LoadCases.WeightsList[27] * ThrustToWeight,resolutionTom,FrontSparX/RootChord,BackSparX/RootChord,HThickness,VThickness, FinalXCentroid, FinalYCentroid) #data, velocity, density, engine thrust, resolution, frontspar (ratio), backspar (ratio), spar thickness, top thickness
            DeformList = Displacement.CalcDisplace(FinalI, LoadCases.WeightsList[27], LoadCases.SpeedFactorsList[27], LoadCases.DensitiesList[27], LoadCases.AoAList[27], LoadCases.LoadFactorsList[27])
            XList = [round(resolutionTom * i, 3) for i in range(len(TorqueList[0]))], [HalfWingSpan * i/len(DeformList[0]) for i in range(len(DeformList[0]))]
            ax.plot(XList[0], TorqueList[0])
            ax2.plot(XList[0], TorqueList[1])
            ax3.plot(XList[1], DeformList[1])
            ax4.plot(XList[1], DeformList[0])
            LargestTorque = TorqueList[1][-1]
            LargestBending = DeformList[0][-1]

        TorqueDeform.delete("1.0", END)
        TorqueDeform.insert(END, LargestTorque)

        DeflectionDeform.delete("1.0", END)
        DeflectionDeform.insert(END, LargestBending)

        print(TorqueCrit, LargestTorque)
        print(BendCrit, LargestBending)

        ax.set_title("Rate of Angular Deformation")
        ax.set_xlabel("distance from root chord")
        #ax.set_ylabel("ooo")

        ax2.set_title("Twist Angle")
        ax2.set_xlabel("distance from root chord")
        ax2.set_ylabel("Angle (deg)")

        ax3.set_title("Wing Loading")
        ax3.set_xlabel("distance from root chord")
        #ax3.set_ylabel("Wing Loading (N)")

        ax4.set_title("Vertical Deflection")
        ax4.set_xlabel("distance from root chord")
        ax4.set_ylabel("Deflection (m)")
    

    if debug == 2:
        TomsPositionsList = [] #list that will allow us
        DecipherPositionsString = []
        #Deciphering the TomsPositions variable
        for i in range(len(TomPositions)):

            if TomPositions[i].isnumeric() or TomPositions[i] == ".":
                DecipherPositionsString.append(TomPositions[i])
            elif DecipherPositionsString != []:
                TomsPositionsList.append(float("".join(DecipherPositionsString)))
                DecipherPositionsString = []
        if DecipherPositionsString != []: TomsPositionsList.append(float("".join(DecipherPositionsString)))

        ShearListTop = ShearForceDiagram.shear_diagram(LoadCases.SpeedFactorsList[56], LoadCases.DensitiesList[56], LoadCases.AoAList[56], LoadCases.LoadFactorsList[56])[1] #Top refers to the conditions of maximum upwards wing loading
        XList = [HalfWingSpan * i/141 for i in range(141)]
        ShearListBot = ShearForceDiagram.shear_diagram(LoadCases.SpeedFactorsList[27], LoadCases.DensitiesList[27], LoadCases.AoAList[27], LoadCases.LoadFactorsList[27])[1] #Bot refers to the conditions of minimum wing loading
        MomentListTop = Momentdiagram.moment(LoadCases.SpeedFactorsList[56], LoadCases.DensitiesList[56], LoadCases.AoAList[56], LoadCases.LoadFactorsList[56])[0]
        MomentListBot = Momentdiagram.moment(LoadCases.SpeedFactorsList[27], LoadCases.DensitiesList[27], LoadCases.AoAList[27], LoadCases.LoadFactorsList[27])[0]
        ListOfMaxStressCandidatesTop = [(abs(ListOfCoord[i][1]) - abs(FinalYCentroid)) for i in range(2)], [(ListOfCoord[0][1] - ListOfCoord[3][1]), (ListOfCoord[1][1] - ListOfCoord[2][1])] #1st is dist from centroid, 2nd is length of stringer
        ListOfMaxStressCandidatesBot = [(abs(ListOfCoord[i + 2][1]) - abs(FinalYCentroid)) for i in range(2)], [(ListOfCoord[0][1] - ListOfCoord[3][1]), (ListOfCoord[1][1] - ListOfCoord[2][1])]
        PleunsFunnyTopList = [(ListOfMaxStressCandidatesTop[0][ListOfMaxStressCandidatesTop[0].index(max(ListOfMaxStressCandidatesTop[0]))]) * (1 - (((1 - 0.316) * i/10)/HalfWingSpan)) for i in range(141)], [(ListOfMaxStressCandidatesTop[1][ListOfMaxStressCandidatesTop[0].index(max(ListOfMaxStressCandidatesTop[0]))]) * (1 - (((1 - 0.316) * i/10)/HalfWingSpan)) for i in range(141)]
        PleunsFunnyBotList = [(ListOfMaxStressCandidatesBot[0][ListOfMaxStressCandidatesBot[0].index(max(ListOfMaxStressCandidatesBot[0]))]) * (1 - (((1 - 0.316) * i/10)/HalfWingSpan)) for i in range(141)], [(ListOfMaxStressCandidatesBot[1][ListOfMaxStressCandidatesBot[0].index(max(ListOfMaxStressCandidatesBot[0]))]) * (1 - (((1 - 0.316) * i/10)/HalfWingSpan)) for i in range(141)] #have fun figuring out wtf this does :)
        #Calculating I and J in terms of spanwise location
        JList = [StiffnessCalculations.TorsionalConstant(FrontSparX, BackSparX, HThickness, VThickness, i/100) for i in range(0, 1401)]
        IList = [FinalI * (1 - (((1 - 0.316) * i/10)/HalfWingSpan))**4 for i in range(141)]

        if PleunsFunnyTopList[0][0] > PleunsFunnyBotList[0][0]: PleunsFinalFunList = PleunsFunnyTopList
        else: PleunsFinalFunList = PleunsFunnyBotList
        MaxStressTop = MaximumStressLocation.CalcMaxStress(IList, PleunsFinalFunList[0], MomentListTop)
        MaxStressBot = MaximumStressLocation.CalcMaxStress(IList, PleunsFinalFunList[0], MomentListBot)

        print(PleunsFinalFunList[0])

        MaxCompressiveStressTop = MaximumStressLocation.CalcMaxStress(IList, PleunsFunnyTopList[0], MomentListTop)
        MaxCompressiveStressBot = MaximumStressLocation.CalcMaxStress(IList, PleunsFunnyBotList[0], MomentListBot)#These are compressive stress only, for TOMM

        if max([abs(MaxCompressiveStressTop[i]) for i in range(len(MaxCompressiveStressTop))]) > max([abs(MaxCompressiveStressBot[i]) for i in range(len(MaxCompressiveStressBot))]): FinalMaxCompressiveStress = MaxCompressiveStressTop
        else: FinalMaxCompressiveStress = MaxCompressiveStressBot

        TomsMassiveList = ColumnBuckling.BigBuckling(FinalMaxCompressiveStress, XList, TomsPositionsList, StringerHeight, StringerLength, StringerThicc) #This list contains the six mini lists from Tom's script

        #plotting shear diagram
        ax.plot(XList, ShearListTop)
        ax.plot(XList, ShearListBot)

        #plotting moment diagram
        ax2.plot(XList, [MaxStressTop[i]/10e6 for i in range(len(MaxStressTop))])
        ax2.plot(XList, [MaxStressBot[i]/10e6 for i in range(len(MaxStressBot))])

        #plotting I

    

        ax5.plot(TomsMassiveList[0], [TomsMassiveList[1][i]/10e6 for i in range(len(TomsMassiveList[1]))], label="Maximum Allowable Stress [MPa]")
        ax5.plot(TomsMassiveList[2], [TomsMassiveList[3][i]/10e6 for i in range(len(TomsMassiveList[3]))], label="Maximum Compressive Stress [MPa]")
        ax6.plot(TomsMassiveList[4], TomsMassiveList[5])

        ax.set_title("Shear Diagram")
        ax.set_xlabel("Spanwise distance from root chord [m]")
        ax.set_ylabel("Shear [N]")

        ax2.set_title("Maximum Stress")
        ax2.set_xlabel("Spanwise distance from root chord [m]")
        ax2.set_ylabel("Max Stress [MPa]")

        ax3.set_title("???????????")
        ax3.set_xlabel("Spanwise distance from root chord [m]")
        ax3.set_ylabel("I [m^4]")

        ax4.set_title("Maximum Allowable Stress [Pa]")
        ax4.set_xlabel("Spanwise distance from root chord [m]")
        ax4.set_ylabel("stress [Pa]")

        ax5.set_title("Maximum Stresses [Pa]")
        ax5.set_xlabel("Spanwise distance from root chord [m]")
        ax5.set_ylabel("stress [Pa]")
        ax5.legend()

        ax6.set_title("Margin")
        ax6.set_xlabel("Spanwise distance from root chord [m]")
        ax6.set_ylabel("Margin")
        ax6.set_ylim((0, 1))
    

    """
    ax4.plot([i/100 for i in range(1401)], IList)
    ax4.set_title("Change in Moment of Inertia")
    ax4.set_xlabel("distance from root chord")
    ax4.set_ylabel("Moment of Inertia [m^4]")

    ax3.plot([i/100 for i in range(1401)], JList)
    ax3.set_title("Change in Torsional Constant")
    ax3.set_xlabel("distance from root chord")
    ax3.set_ylabel("Torsional Constant [m^4]")
    """

    GraphCanvas1.draw()
    GraphCanvas2.draw()
    GraphCanvas3.draw()
    GraphCanvas4.draw()
    GraphCanvas5.draw()
    GraphCanvas6.draw()

    #plt.show()


FinalI = 0
C = Canvas(root, bg="white", height=CanvasDimensions[1], width=CanvasDimensions[0])

Box = C.create_polygon(0, 0, 0, 0, 0, 0, 0, 0, fill="green", outline="green")
InsideBox = C.create_polygon(0, 0, 0, 0, 0, 0, 0, 0, fill="white", outline="green")

#Drawing the airfoil
for i in range(0, len(FinalAirfoilPoints[0]) - 1):
    C.create_line(ScalingFactor*FinalAirfoilPoints[0][i] + Offset, -ScalingFactor*FinalAirfoilPoints[1][i] + CanvasDimensions[1]*0.5, ScalingFactor*FinalAirfoilPoints[0][i + 1] + Offset, -ScalingFactor*FinalAirfoilPoints[1][i + 1] + CanvasDimensions[1]*0.5, fill="red")
    C.create_line(ScalingFactor*FinalAirfoilPoints[0][i] + Offset, -ScalingFactor*FinalAirfoilPoints[2][i] + CanvasDimensions[1]*0.5, ScalingFactor*FinalAirfoilPoints[0][i + 1] + Offset, -ScalingFactor*FinalAirfoilPoints[2][i + 1] + CanvasDimensions[1]*0.5, fill="red")

#axis
line = C.create_line(0, CanvasDimensions[1]*0.5, CanvasDimensions[0], CanvasDimensions[1]*0.5, fill='blue')
line = C.create_line(Offset, 0, Offset, CanvasDimensions[1], fill='blue')

"""TopRectangleYCentroid = C.create_line(0 + CanvasDimensions[0]*0.5, - TopRectangle[2]*100 + CanvasDimensions[1]*0.5, 
                                      10 + CanvasDimensions[0]*0.5, -TopRectangle[2]*100 + CanvasDimensions[1]*0.5,fill='green')
TopTriangleYCentroid = C.create_line(0 + CanvasDimensions[0]*0.5, - TopTriangle[2]*100 + CanvasDimensions[1]*0.5, 
                                      10 + CanvasDimensions[0]*0.5, -TopTriangle[2]*100 + CanvasDimensions[1]*0.5,fill='green')
BotRectangleYCentroid = C.create_line(0 + CanvasDimensions[0]*0.5, - BotRectangle[2]*100 + CanvasDimensions[1]*0.5, 
                                      10 + CanvasDimensions[0]*0.5, -BotRectangle[2]*100 + CanvasDimensions[1]*0.5,fill='green')
BotTriangleYCentroid = C.create_line(0 + CanvasDimensions[0]*0.5, - BotTriangle[2]*100 + CanvasDimensions[1]*0.5, 
                                      10 + CanvasDimensions[0]*0.5, -BotTriangle[2]*100 + CanvasDimensions[1]*0.5,fill='green')"""

FinalXCentroidLine = C.create_line(0, 0, 0, 0,fill='purple', width=4)
FinalYCentroidLine = C.create_line(0, 0, 0, 0,fill='purple', width=4)

#List of Inputs in the GUI

#BottomHolder holds everything except the airfoil

BottomHolder = Frame(root, bg = "gray", padx = 10, pady = 5)
GraphsHolder = Frame(BottomHolder, bg = "light gray", padx = 0, pady = 0)
VariableHolder = Frame(BottomHolder, bg = "light gray", padx = 10, pady = 5)

ComputeButton = Button(VariableHolder, text="Compute", bg="red", font = 2, command=lambda:Main(float(FrontSparXINPUT.get()), float(BackSparXINPUT.get()), float(HThicknessINPUT.get()), float(VThicknessINPUT.get()), int(stringNumTopINPUT.get()), int(stringNumBotINPUT.get()), float(stringAreaINPUT.get()), 0, float(stringThickINPUT.get())/1000, float(stringHINPUT.get())/1000, float(stringVINPUT.get())/1000, stringPosINPUT.get()))
ComputeButton.grid(row = 0, column = 5, sticky = W, padx=10)
DebugButton = Button(VariableHolder, text="Quick Compute", bg="green", font = 2, command=lambda:Main(float(FrontSparXINPUT.get()), float(BackSparXINPUT.get()), float(HThicknessINPUT.get()), float(VThicknessINPUT.get()), int(stringNumTopINPUT.get()), int(stringNumBotINPUT.get()), float(stringAreaINPUT.get()), 1, float(stringThickINPUT.get())/1000, float(stringHINPUT.get())/1000, float(stringVINPUT.get())/1000, stringPosINPUT.get()))
DebugButton.grid(row = 1, column = 5, sticky = W, padx=10)
BuckleButton = Button(VariableHolder, text="Compute Buckle", bg="yellow", font = 2, command=lambda:Main(float(FrontSparXINPUT.get()), float(BackSparXINPUT.get()), float(HThicknessINPUT.get()), float(VThicknessINPUT.get()), int(stringNumTopINPUT.get()), int(stringNumBotINPUT.get()), float(stringAreaINPUT.get()), 2, float(stringThickINPUT.get())/1000, float(stringHINPUT.get())/1000, float(stringVINPUT.get())/1000, stringPosINPUT.get()))
BuckleButton.grid(row = 2, column = 5, sticky = W, padx=10)

Label(VariableHolder, text="Front Spar X pos (m)", bg="white", font = 2).grid(row = 0, column = 0, sticky = W, padx = 2, pady=5)
FrontSparXINPUT = Entry(VariableHolder, bd=3, font=2)
FrontSparXINPUT.insert(0, 1)
FrontSparXINPUT.grid(row = 0, column = 1, sticky = W, padx = 2, pady=5)

Label(VariableHolder, text="Back Spar X pos (m)", bg="white", font = 2).grid(row = 1, column = 0, sticky = W, padx = 2, pady=5)
BackSparXINPUT = Entry(VariableHolder, bd=3, font=2)
BackSparXINPUT.insert(0, 2)
BackSparXINPUT.grid(row = 1, column = 1, sticky = W, padx = 2, pady=5)

Label(VariableHolder, text="Horizontal thickness (mm)", bg="white", font = 2).grid(row = 2, column = 0, sticky = W, padx = 2, pady=5)
HThicknessINPUT = Entry(VariableHolder, bd=3, font=2)
HThicknessINPUT.insert(0, 10)
HThicknessINPUT.grid(row = 2, column = 1, sticky = W, padx = 2, pady=5)

Label(VariableHolder, text="Vertical thickness (mm)", bg="white", font = 2).grid(row = 3, column = 0, sticky = W, padx = 2, pady=5)
VThicknessINPUT = Entry(VariableHolder, bd=3, font=2)
VThicknessINPUT.insert(0, 10)
VThicknessINPUT.grid(row = 3, column = 1, sticky = W, padx = 2, pady=5)

Label(VariableHolder, text="Number of Top Stringers", bg="white", font = 2).grid(row = 4, column = 0, sticky = W, padx = 2, pady=5)
stringNumTopINPUT = Entry(VariableHolder, bd=3, font=2)
stringNumTopINPUT.insert(0, 3)
stringNumTopINPUT.grid(row = 4, column = 1, sticky = W, padx = 2, pady=5)

Label(VariableHolder, text="Number of Bottom Stringers", bg="white", font = 2).grid(row = 5, column = 0, sticky = W, padx = 2, pady=5)
stringNumBotINPUT = Entry(VariableHolder, bd=3, font=2)
stringNumBotINPUT.insert(0, 5)
stringNumBotINPUT.grid(row = 5, column = 1, sticky = W, padx = 2, pady=5)

Label(VariableHolder, text="Stringer Area (m2)", bg="white", font = 2).grid(row = 6, column = 0, sticky = W, padx = 2, pady=5)
stringAreaINPUT = Entry(VariableHolder, bd=3, font=2)
stringAreaINPUT.insert(0, 0.002)
stringAreaINPUT.grid(row = 6, column = 1, sticky = W, padx = 2, pady=5)

Label(VariableHolder, text="Stringer Thickness (mm)", bg="white", font = 2).grid(row = 0, column = 2, sticky = W, padx = 2, pady=5)
stringThickINPUT = Entry(VariableHolder, bd=3, font=2)
stringThickINPUT.insert(0, 10)
stringThickINPUT.grid(row = 0, column = 3, sticky = W, padx = 2, pady=5)

Label(VariableHolder, text="Stringer Horizontal Length (mm)", bg="white", font = 2).grid(row = 1, column = 2, sticky = W, padx = 2, pady=5)
stringHINPUT = Entry(VariableHolder, bd=3, font=2)
stringHINPUT.insert(0, 40)
stringHINPUT.grid(row = 1, column = 3, sticky = W, padx = 2, pady=5)

Label(VariableHolder, text="Stringer Vertical Length (mm)", bg="white", font = 2).grid(row = 2, column = 2, sticky = W, padx = 2, pady=5)
stringVINPUT = Entry(VariableHolder, bd=3, font=2)
stringVINPUT.insert(0, 40)
stringVINPUT.grid(row = 2, column = 3, sticky = W, padx = 2, pady=5)

Label(VariableHolder, text="Stringer Positioning", bg="white", font = 2).grid(row = 7, column = 0, sticky = W, padx = 2, pady=5)
stringPosINPUT = Entry(VariableHolder, bd=3, font=2, width=70)
stringPosINPUT.insert(0, "0, 0.6, 1.3, 2.0, 2.8, 3.6, 4.5, 5.5, 6.7, 8.0, 9.5, 11, 13.75")
stringPosINPUT.grid(row = 7, column = 1, sticky = W, padx = 2, pady=5, columnspan=3)

"""
Label(VariableHolder, text="Stringer Thickness (mm)", bg="white", font = 2).grid(row = 2, column = 2, sticky = W, padx = 2)
stringThickINPUT = Entry(VariableHolder, bd=3, font=2)
stringThickINPUT.insert(0, 0.002)
stringThickINPUT.grid(row = 2, column = 3, sticky = W, padx = 2)
"""

TorqueDeform = Text(VariableHolder, height = 0.5, width = 10, bg = "light cyan", font =2 , padx=10, pady=5)
Label(VariableHolder, text="Torque in Degrees", bg="white", font=2).grid(row = 10, column = 0, sticky = W, padx = 0)
TorqueDeform.grid(row=10, column=1, sticky=W)

DeflectionDeform = Text(VariableHolder, height = 0.5, width = 10, bg = "light cyan", font =2 , padx=10, pady=5)
Label(VariableHolder, text="Downwards Deflection", bg="white", font=2).grid(row = 11, column = 0, sticky = W, padx = 0)
DeflectionDeform.grid(row=11, column=1, sticky=W)

fig, ax = plt.subplots()
GraphCanvas1 = FigureCanvasTkAgg(fig, master=GraphsHolder)
GraphCanvas1.get_tk_widget().grid(row = 2, column = 0, sticky = W, padx = 2)

fig, ax2 = plt.subplots()
GraphCanvas2 = FigureCanvasTkAgg(fig, master=GraphsHolder)
GraphCanvas2.get_tk_widget().grid(row = 2, column = 1, sticky = W, padx = 2)

fig, ax3 = plt.subplots()
GraphCanvas3 = FigureCanvasTkAgg(fig, master=GraphsHolder)
GraphCanvas3.get_tk_widget().grid(row = 2, column = 2, sticky = W, padx = 2)

fig, ax4 = plt.subplots()
GraphCanvas4 = FigureCanvasTkAgg(fig, master=GraphsHolder)
GraphCanvas4.get_tk_widget().grid(row = 3, column = 0, sticky = W, padx = 2)

fig, ax5 = plt.subplots()
GraphCanvas5 = FigureCanvasTkAgg(fig, master=GraphsHolder)
GraphCanvas5.get_tk_widget().grid(row = 3, column = 1, sticky = W, padx = 2)

fig, ax6 = plt.subplots()
GraphCanvas6 = FigureCanvasTkAgg(fig, master=GraphsHolder)
GraphCanvas6.get_tk_widget().grid(row = 3, column = 2, sticky = W, padx = 2)

C.grid(row = 0, column = 0, sticky = W, padx = 2)
VariableHolder.grid(row = 0, column = 0, sticky = W, pady=5)
BottomHolder.grid(row = 1, column = 0, sticky = W, padx = 0)
GraphsHolder.grid(row = 2, column  =0, padx = 0, pady = 0, columnspan=100)

root.mainloop()
