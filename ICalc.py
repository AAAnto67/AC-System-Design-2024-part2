import numpy as np
from tkinter import *
import math as m
import StiffnessCalculations
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

root = Tk()

Offset = 50
RootChord = 4.26
HalfWingSpan = StiffnessCalculations.span/2
ScalingFactor = 1000

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

#Starting w Moments of Inertia

def CalcTruei(ListOfCoord):
    TopRectangle = [ListOfCoord[1][0] - ListOfCoord[0][0], min([ListOfCoord[0][1], ListOfCoord[1][1]]), min([ListOfCoord[0][1], ListOfCoord[1][1]])/2] #horizontal length, vertical length, Y centroid
    TopTriangle = [TopRectangle[0], (max([ListOfCoord[0][1], ListOfCoord[1][1]]) - TopRectangle[1]), (TopRectangle[1] + (max([ListOfCoord[0][1], ListOfCoord[1][1]]) - TopRectangle[1])/3)] #Horizontal  length, vertical length, Y centroid
    BotRectangle = [ListOfCoord[3][0] - ListOfCoord[2][0], max([ListOfCoord[2][1], ListOfCoord[3][1]]), max([ListOfCoord[2][1], ListOfCoord[3][1]])/2] #horizontal length, vertical length, Y centroid
    BotTriangle = [BotRectangle[0], (min([ListOfCoord[2][1], ListOfCoord[3][1]]) - BotRectangle[1]), (BotRectangle[1] + (min([ListOfCoord[2][1], ListOfCoord[3][1]]) - BotRectangle[1])/3)] #Horizontal  length, vertical length, Y centroid
    #IMPORTANT if the top or Bot rectangles are both ABOVE or BELOW the chord line the centroid WILL BE WRONGG!!!

    FinalCentroid = (TopRectangle[0]*TopRectangle[1]*TopRectangle[2] + TopTriangle[0]*TopTriangle[1]*TopTriangle[2] + BotRectangle[0]*BotRectangle[1]*BotRectangle[2] + BotTriangle[0]*BotTriangle[1]*BotTriangle[2])/(TopRectangle[0]*TopRectangle[1] + TopTriangle[0]*TopTriangle[1] + BotRectangle[0]*BotRectangle[1] + BotTriangle[0]*BotTriangle[1])

    ITopRectangle = (TopRectangle[0]*TopRectangle[1]**3)/12 + TopRectangle[0]*TopRectangle[1]*(TopRectangle[2] - FinalCentroid)**2
    ITopTriangle = (TopTriangle[0]*TopTriangle[1]**3)/36 + 0.5*TopTriangle[0]*TopTriangle[1]*(TopTriangle[2] - FinalCentroid)**2
    IBotRectangle = (BotRectangle[0]*BotRectangle[1]**3)/12 + BotRectangle[0]*BotRectangle[1]*(BotRectangle[2] - FinalCentroid)**2
    IBotTriangle = (BotTriangle[0]*BotTriangle[1]**3)/36 + 0.5*BotTriangle[0]*BotTriangle[1]*(BotTriangle[2] - FinalCentroid)**2

    return((ITopRectangle + ITopTriangle + IBotRectangle + IBotTriangle), (FinalCentroid))

def CalcString(StringX, ListOfSecondCoord, Angle, Stringheight):
    #print(StringX * m.tan(Angle))
    StringY = StringX * m.tan(Angle) + Stringheight
    #C.create_line(ScalingFactor*(StringX + ListOfSecondCoord[0][0])/RootChord + Offset, CanvasDimensions[1], ScalingFactor*(StringX + ListOfSecondCoord[0][0])/RootChord + Offset, -ScalingFactor*(StringY)/RootChord + CanvasDimensions[1]*0.5)
    return(StringY)

def CalcI(FrontSparX, BackSparX, HThickness, VThickness, StringNumTop, StringNumBot, StringArea):
    HThickness = HThickness/1000
    VThickness = VThickness/1000
    FrontSparTop = FinalAirfoilPoints[1][FindClosest(FinalAirfoilPoints[0], FrontSparX/RootChord)]*RootChord
    FrontSparBot = -FinalAirfoilPoints[2][FindClosest(FinalAirfoilPoints[0], FrontSparX/RootChord)]*RootChord
    BackSparTop = FinalAirfoilPoints[1][FindClosest(FinalAirfoilPoints[0], BackSparX/RootChord)]*RootChord
    BackSparBot = -FinalAirfoilPoints[2][FindClosest(FinalAirfoilPoints[0], BackSparX/RootChord)]*RootChord

    ListOfCoord = [FrontSparX, FrontSparTop], [BackSparX, BackSparTop], [BackSparX, -BackSparBot], [FrontSparX, -FrontSparBot]
    #TopAngle = m.atan(((max([ListOfCoord[0][1], ListOfCoord[1][1]]) - min([ListOfCoord[0][1], ListOfCoord[1][1]])))/(ListOfCoord[1][0] - ListOfCoord[0][0])) Old Calculation
    TopAngle = m.atan((ListOfCoord[1][1] - ListOfCoord[0][1])/(ListOfCoord[1][0] - ListOfCoord[0][0]))
    BotAngle = -m.atan((ListOfCoord[3][1] - ListOfCoord[2][1])/(ListOfCoord[1][0] - ListOfCoord[0][0]))
    ListOfSecondCoord = [FrontSparX + HThickness, FrontSparTop - VThickness*m.cos(abs(TopAngle))], [BackSparX - HThickness, BackSparTop - VThickness*m.cos(abs(TopAngle))], [BackSparX - HThickness, -BackSparBot + VThickness*m.cos(abs(BotAngle))], [FrontSparX + HThickness, -FrontSparBot + VThickness*m.cos(abs(BotAngle))]
    FinalCentroid = CalcTruei(ListOfCoord)[1]

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
    C.coords(FinalYCentroid, -10 + CanvasDimensions[0]*0.5, - FinalCentroid*100 + CanvasDimensions[1]*0.5, 
                                      10 + CanvasDimensions[0]*0.5, -FinalCentroid*100 + CanvasDimensions[1]*0.5)
    FinalI = CalcTruei(ListOfCoord)[0] - CalcTruei(ListOfSecondCoord)[0] + StringersTotalI

    Ixx.delete("1.0", END)
    Ixx.insert(END, FinalI)

    y = StiffnessCalculations.deformation('a.txt',86.10,0.3,resolutionTom,FrontSparX/RootChord,BackSparX/RootChord,HThickness,VThickness) #data, velocity, density, resolution, frontspar (ratio), backspar (ratio), spar thickness, top thickness
    XList = [round(resolutionTom * i, 3) for i in range(len(y[0]))]
    print(y[0])
    print(XList)
    print(len(y[0]), len(XList))
    ax.clear()
    ax.plot(XList, y[0])
    TomsCanvas.draw()

    ax2.clear()
    ax2.plot(XList, y[1])
    TomsCanvas2.draw()

    TorqueDeform.delete("1.0", END)
    TorqueDeform.insert(END, y[2])

CanvasDimensions = [1100, 200]
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

FinalYCentroid = C.create_line(0, 0, 0, 0,fill='purple')

#List of Inputs in the GUI

BottomHolder = Frame(root, bg = "gray", padx = 10, pady = 5)

VariableHolder = Frame(BottomHolder, bg = "gray", padx = 10, pady = 5)

Label(VariableHolder, text="Front Spar X pos (m)", bg="white").grid(row = 0, column = 0, sticky = W, padx = 2)
FrontSparXINPUT = Entry(VariableHolder, bd=3)
FrontSparXINPUT.insert(0, 1)
FrontSparXINPUT.grid(row = 0, column = 1, sticky = W, padx = 2)

Label(VariableHolder, text="Back Spar X pos (m)", bg="white").grid(row = 3, column = 0, sticky = W, padx = 2)
BackSparXINPUT = Entry(VariableHolder, bd=3)
BackSparXINPUT.insert(0, 2)
BackSparXINPUT.grid(row = 3, column = 1, sticky = W, padx = 2)

Label(VariableHolder, text="Horizontal thickness (mm)", bg="white").grid(row = 4, column = 0, sticky = W, padx = 2)
HThicknessINPUT = Entry(VariableHolder, bd=3)
HThicknessINPUT.insert(0, 2)
HThicknessINPUT.grid(row = 4, column = 1, sticky = W, padx = 2)

Label(VariableHolder, text="Vertical thickness (mm)", bg="white").grid(row = 5, column = 0, sticky = W, padx = 2)
VThicknessINPUT = Entry(VariableHolder, bd=3)
VThicknessINPUT.insert(0, 2)
VThicknessINPUT.grid(row = 5, column = 1, sticky = W, padx = 2)

Label(VariableHolder, text="Number of Top Stringers", bg="white").grid(row = 6, column = 0, sticky = W, padx = 2)
stringNumTopINPUT = Entry(VariableHolder, bd=3)
stringNumTopINPUT.insert(0, 5)
stringNumTopINPUT.grid(row = 6, column = 1, sticky = W, padx = 2)

Label(VariableHolder, text="Number of Bottom Stringers", bg="white").grid(row = 7, column = 0, sticky = W, padx = 2)
stringNumBotINPUT = Entry(VariableHolder, bd=3)
stringNumBotINPUT.insert(0, 6)
stringNumBotINPUT.grid(row = 7, column = 1, sticky = W, padx = 2)

Label(VariableHolder, text="Stringer Area (m2)", bg="white").grid(row = 8, column = 0, sticky = W, padx = 2)
stringAreaINPUT = Entry(VariableHolder, bd=3)
stringAreaINPUT.insert(0, 0.002)
stringAreaINPUT.grid(row = 8, column = 1, sticky = W, padx = 2)

ComputeButton = Button(VariableHolder, text="Compute", bg="red", command=lambda:CalcI(float(FrontSparXINPUT.get()), float(BackSparXINPUT.get()), float(HThicknessINPUT.get()), float(VThicknessINPUT.get()), int(stringNumTopINPUT.get()), int(stringNumBotINPUT.get()), float(stringAreaINPUT.get())))
ComputeButton.grid(row = 9, column = 0, sticky = W, padx = 20)

OutputHolder = Frame(BottomHolder, bg = "gray", padx = 10, pady = 5)

Ixx = Text(OutputHolder, height = 0.5, width = 10, bg = "light cyan", font =1 , padx=10, pady=5)
Label(OutputHolder, text="Ixx", bg="white").grid(row = 0, column = 0, sticky = W, padx = 0)
Ixx.grid(row=0, column=1, sticky=W)

TorqueDeform = Text(OutputHolder, height = 0.5, width = 10, bg = "light cyan", font =1 , padx=10, pady=5)
Label(OutputHolder, text="Tom's Deformation in Degrees", bg="white").grid(row = 1, column = 0, sticky = W, padx = 0)
TorqueDeform.grid(row=1, column=1, sticky=W)

fig, ax = plt.subplots()
TomsCanvas = FigureCanvasTkAgg(fig, master=root)
TomsCanvas.get_tk_widget().grid(row = 2, column = 0, sticky = W, padx = 0)

fig2, ax2 = plt.subplots()
TomsCanvas2 = FigureCanvasTkAgg(fig2, master=root)
TomsCanvas2.get_tk_widget().grid(row = 3, column = 0, sticky = W, padx = 0)

C.grid(row = 0, column = 0, sticky = W, padx = 2)
VariableHolder.grid(row = 0, column = 0, sticky = W, padx = 0)
OutputHolder.grid(row = 0, column = 1, sticky = W, padx = 0)
BottomHolder.grid(row = 1, column = 0, sticky = W, padx = 0)

root.mainloop()
