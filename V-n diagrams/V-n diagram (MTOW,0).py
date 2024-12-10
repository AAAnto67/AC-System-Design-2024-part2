import numpy as np 
import matplotlib.pyplot as plt

# MTOW + sea level
# CONSTANTS 
MTOW_lb = 17288
MTOW = 33819 * 9.80665
S = 75.632
M_TAS_C = 0.77
a_0 = np.sqrt(1.4 * 287.053 * (15 + 273))
a_C = np.sqrt(1.4 * 287.053 * (218.8))
V_TAS_C = M_TAS_C * a_C
rho_C = 0.38
rho_0 = 1.225 
C_Lf = 2.1 
C_L = 1.46

n_max = max(2.5, min(2.1 + (24000 / (MTOW_lb + 10000)), 3.8)) # 2.1 + 24000 / (MTOW_lb + 10000)
n_min = -1.0
V_s0 = np.sqrt( 2 * MTOW / (C_Lf * rho_0 * S )) #stall speed flaps extended 
V_s1 = np.sqrt( 2 * MTOW / (C_L * rho_0 * S ))#stall speed flaps retracted 
V_A = V_s1 * np.sqrt(n_max) #maneouvering speed
V_H = V_s1 * np.sqrt(np.abs(n_min))
V_C = V_TAS_C * np.sqrt (rho_C / rho_0) #design cruise speed (m/s) #MAY be equal to V_TAS_C
V_D = V_C / 0.8 #dive speed
M_EAS_C = M_TAS_C * np.sqrt (rho_C / rho_0)
M_D = M_EAS_C / 0.8 # not in diagram 
V_F1 = 1.6 * V_s1 #design wing flap speed #check manual in order 
#V_F2 = 1.8 * V_s1
#V_F3 = 1.8 * V_s0



#speed ranges
V_range = np.linspace(0, V_D, 500)
V_rangef = np.linspace(0, 98.8, 500)

# Positive load factors
n_positive = np.minimum((V_range / V_s1)**2, n_max)  # Parabolic up to n_max
n_positive_flaps = np.minimum((V_range / V_s0)**2, 2.0)  # Flaps down case (n <= 2)

# Negative load factors (linear decay from n_min to 0 between V_C and V_D)
n_negative = np.piecewise(V_range, 
                          [V_range <= V_H , (V_range > V_H) & (V_range <= V_C), (V_range > V_C) & (V_range <= V_D), V_range > V_D],
                          [lambda V: - (V / V_s1) ** 2,
                           lambda V: -1.0,  # Constant at -1.0 up to V_C
                           lambda V: n_min * (1 - (V - V_C) / (V_D - V_C)),
                           lambda V: 0])  # Zero beyond V_D



# Plot the V-n diagram
plt.figure(figsize=(10, 6))

# Positive region
plt.plot(V_range, n_positive, color="blue")
plt.plot(V_rangef, n_positive_flaps, color="cyan")
#plt.plot(V_range, n_positive, label="Positive Load Factor (Flaps Up)", color="blue")
#plt.plot(V_rangef, n_positive_flaps, label="Positive Load Factor (Flaps Down)", color="cyan")

# Negative region
plt.plot(V_range, n_negative, color="red")
#plt.plot(V_range, n_negative, label="Negative Load Factor", color="red")

# Mark critical points
plt.axhline(y=n_max, color="blue", linestyle=":")
plt.axhline(y=n_min, color="red", linestyle=":")
plt.axvline(x=V_s1, color="green", linestyle="--")
plt.axvline(x=V_A, color="orange", linestyle="--")
plt.axvline(x=V_C, color="purple", linestyle="--")
plt.axvline(x=V_D, color="brown", linestyle="-")
plt.axvline(x=V_F1, color="deeppink", linestyle="--") 
#plt.axvline(x=V_F2, color="yellow", linestyle="--",label=f"V_F2 = {V_F2} m/s") 
#plt.axvline(x=V_F3, color="pink", linestyle="--",label=f"V_F3 = {V_F3} m/s") 

#plt.axhline(y=n_max, color="blue", linestyle=":", label=f"n_max = {n_max:.2f}")
#plt.axhline(y=n_min, color="red", linestyle=":", label=f"n_min = {n_min:.2f}")
#plt.axvline(x=V_s1, color="green", linestyle="--", label=f"V_S1 = {V_s1:.2f} m/s")
#plt.axvline(x=V_A, color="orange", linestyle="--", label=f"V_A = {V_A:.2f} m/s")
#plt.axvline(x=V_C, color="purple", linestyle="--", label=f"V_C = {V_C:.2f} m/s")
#plt.axvline(x=V_D, color="brown", linestyle="-", label=f"V_D = {V_D:.2f} m/s")
#plt.axvline(x=V_F1, color="deeppink", linestyle="--",label=f"V_F1 = {V_F1:.2f} m/s") 



# Formatting the plot
#plt.title("V-n Diagram for Manoeuvres for MTOW at sea level")
plt.xlabel("Equivalent Airspeed (V) [m/s]")
plt.ylabel("Load Factor (n)")
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend(framealpha = 1)
plt.xlim(0, V_D * 1.1)  # Extend x-axis slightly beyond V_D
plt.ylim(n_min - 0.5, n_max + 0.5)  # Extend y-axis slightly beyond n_min and n_max

# Show the plot
plt.show()
