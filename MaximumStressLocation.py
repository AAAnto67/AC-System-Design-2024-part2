from Momentdiagram import moment
from XFLR5 import angle 
from StiffnessCalculations import span
import matplotlib.pyplot as plt

halfwingspan = span/2

def CalcMaxStress(I_list, y, M_list):
    return([(M_list[i] * y[i])/I_list[i] for i in range(len(I_list))])

def MaximumStressIndivid(I, y_max, M):
    sigma = M*y_max/I
    return (sigma)

def MaxStressMargin(halfwingspan, I_list, y_max, M_list):

    yieldstress = 450000000

    #list moment of inertia, span and moment
    span_list = [halfwingspan*(i/141) for i in range(len(I_list))]

    stress=[]
    margin_of_safety = []
    for M, y_max, I in zip(M_list, y_max, I_list): #change span_list to y_max
        maxstress= MaximumStressIndivid(I, y_max, M)
        safety_margin = yieldstress/maxstress
        stress.append(maxstress)
        margin_of_safety.append(safety_margin)

    """
    span_limit = 10.5

    span_list_limit = [value for value in span_list if value <= span_limit]
    print(len(span_list_limit))
    margin_of_safety_limit = margin_of_safety[:len(span_list_limit)]
    margin_of_safety_limit += [0 for i in range(141 - len(margin_of_safety_limit))]
    
    return(maxstress, margin_of_safety_limit)
    """
    return(maxstress, margin_of_safety)

