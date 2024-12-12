from XFLR5 import *
from matplotlib import pyplot as plt

def shear_diagram(V, rho, AoA, loadfactor):
    halfspan = 14
    dy = 0.01
    engine_weight = 1678.3 * 9.81
    y_engine = 4.8
    volume = 48.96
    wing_weight = 6748 * 9.81
    density = wing_weight / volume

    dist_list = []
    V_list = []
    y_list = []
    y = 0
    moment = 0
    area = lambda x: (4.18 - 0.207936 * x)**2 * 0.11
        
        
    while y <= halfspan:
        segment_lift = 0.5 * rho * V**2 * c(y) * cl(AoA, y)
        segment_weight = area(y) * density
        
        dist_list.append(loadfactor * (segment_lift - segment_weight)) 
        y_list.append(y)   
        y += dy

    V = 0
    for i in range(len(dist_list)):
        if y_list[len(dist_list)-1-i] >= 1.4:
            V += dist_list[len(dist_list)-1-i] * dy
        if y_list[len(dist_list)-1-i] < y_engine:
            V_list.insert(0, V + engine_weight)
        else:
            V_list.insert(0, V)
    return(y_list, V_list)

    """
    # Add labels and title
    plt.plot(y_list, V_list)

    plt.xlabel('y')
    plt.ylabel('Torsion')
    plt.title('Shear force diagram')
    

    # Add grid and legend
    plt.grid(True)

    # Show the plot
    plt.show()
    """
    # Show the plot
    plt.show()
