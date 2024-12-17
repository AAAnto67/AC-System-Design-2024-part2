import numpy as np

class SkinPanel:
    '''Defines skin panel of length a in the spanwise direction, width b in the chordwise direction, and thickness t.'''
    k_c = 7  # Buckling coefficient
    E = 72.4 * 10**9  # [Pa] Young's modulus
    nu = 0.33  # Poisson's ratio

    def __init__(self, a, b, t, sigma):
        self.a = a  # Spanwise length
        self.b = b  # Chordwise width
        self.t = t  # Thickness
        self.sigma = sigma  # Max compressive stress applied

    def criticalStress(self):
        '''Calculates the critical buckling stress for the skin panel.'''
        stress = (np.pi**2 * self.k_c * self.E /
                  (12 * (1 - self.nu**2)) *
                  (self.t / self.b)**2)
        return stress

    def marginOfSafety(self):
        '''Calculates the margin of safety for the skin panel.'''
        margin = self.criticalStress() / self.sigma - 1
        return margin


def marginOfSafetyList(stringerPositions, ribPositions, compressiveStressesList, panelThickness, span):
    '''Returns a list of margins of safety for each panel.'''
    results = []
    for stringer_index in range(len(stringerPositions) - 1):  # Loop through stringers
        b = stringerPositions[stringer_index + 1] - stringerPositions[stringer_index]  # Chordwise width

        for rib_index in range(len(ribPositions) - 1):  # Loop through ribs
            a = ribPositions[rib_index + 1] - ribPositions[rib_index]  # Spanwise length

            # Get compressive stress at the rib position
            stress_index = int(ribPositions[rib_index] / span * len(compressiveStressesList))
            applied_stress = compressiveStressesList[stress_index]

            # Create a SkinPanel instance and compute margin of safety
            panel = SkinPanel(a, b, t=panelThickness, sigma=applied_stress)
            margin_of_safety = panel.marginOfSafety()
            results.append(margin_of_safety)

    return results


# Usage
stringerPositions = []  # Chordwise positions of stringers [m]
ribPositions = []  # Spanwise positions of ribs [m]
compressiveStressesList = []  # Compressive stresses at rib positions [Pa]
panelThickness = 0  # Panel thickness [m]
span = 13.75

print(marginOfSafetyList(stringerPositions, ribPositions, compressiveStressesList, panelThickness, span))
