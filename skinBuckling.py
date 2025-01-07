import numpy as np

class SkinPanel:
    '''Defines skin panel of length a in the spanwise direction, width b in the chordwise direction, and thickness t.'''
    
    E = 72.4 * 10**9  # [Pa] Young's modulus
    nu = 0.33  # Poisson's ratio

    def __init__(self, a, b, t, sigma):
        self.a = a  # Spanwise length
        self.b = b  # Chordwise width
        self.t = t  # Thickness
        self.sigma = sigma  # Max compressive stress applied
        self.k_c = self.k_c(self.a/self.b)  # Buckling coefficient

    def criticalStress(self):
        '''Calculates the critical buckling stress for the skin panel.'''
        stress = (np.pi**2 * self.k_c * self.E /
                  (12 * (1 - self.nu**2)) *
                  (self.t / self.b)**2)
        return stress

    def marginOfSafety(self):
        '''Calculates the margin of safety for the skin panel.'''
        margin = self.criticalStress() / self.sigma
        print(f'stress critical:{self.criticalStress()}') 
        return margin

    def k_c(self, a_b):
        '''Calculates the buckling coefficient'''
        if a_b < 0.65:
            k = -10.42*a_b + 13.8
        elif a_b < 0.9:
            k = 4*a_b + 4.4
        elif a_b < 1.3:
            k = -2.5 * a_b + 10.25
        else:
            k = 7
        return k


def marginOfSafetyList(stringerPositions, ribPositions, compressiveStressesList, panelThickness, span):
    '''Returns a list of margins of safety for each panel.'''
    results = []
    for stringer_index in range(len(stringerPositions) - 1):  # Loop through stringers
        b = stringerPositions[stringer_index + 1] - stringerPositions[stringer_index]  # Chordwise width
        print(f'b: {b}')

        for rib_index in range(len(ribPositions) - 1):  # Loop through ribs
            a = ribPositions[rib_index + 1] - ribPositions[rib_index]  # Spanwise length
            print(f'a: {a}')
            # Get compressive stress at the rib position
            stress_index = round(ribPositions[rib_index] / span * len(compressiveStressesList))
            applied_stress = compressiveStressesList[stress_index]

            # Create a SkinPanel instance and compute margin of safety
            panel = SkinPanel(a, b, t=panelThickness, sigma=applied_stress)
            margin_of_safety = panel.marginOfSafety()
            results.append(margin_of_safety)
            print(f'applied stress: {applied_stress}')

    return results


# Usage
stringerPositions = [0.2,1.6,2.8]  # Chordwise positions of stringers [m]
ribPositions = [0,2,4,10,14]  # Spanwise positions of ribs [m]
compressiveStressesList = [np.float64(377797688.49549407), np.float64(377897010.1581396), np.float64(377941826.4478795), np.float64(377929893.7060434), np.float64(377858882.04235846), np.float64(377726371.789775), np.float64(377529849.7992033), np.float64(377266705.566191), np.float64(376934227.18113655), np.float64(376529597.0941719), np.float64(376049887.6853578), np.float64(375492056.630314), np.float64(374852942.0508572), np.float64(374129257.4396365), np.float64(373317586.34712946), np.float64(372468413.31576586), np.float64(371586942.73584485), np.float64(370677904.5217444), np.float64(369745298.2293626), np.float64(368792179.7223318), np.float64(367820676.64252937), np.float64(366832066.8266776), np.float64(365826864.10727674), np.float64(364804912.02578276), np.float64(363765486.02285475), np.float64(362707404.7100835), np.float64(361629150.8700938), np.float64(360529002.8774778), np.float64(359405177.2819378), np.float64(358255983.3475304), np.float64(357079972.65319645), np.float64(355875971.18641114), np.float64(354643056.0486143), np.float64(353380529.54788196), np.float64(352087890.72868884), np.float64(350764804.14328814), np.float64(349411065.6546117), np.float64(348026565.0448232), np.float64(346611245.1866526), np.float64(345165057.51631767), np.float64(343687913.5270661), np.float64(342179637.4249791), np.float64(340639955.4025958), np.float64(339068502.59768444), np.float64(337464830.93206257), np.float64(335828417.81567514), np.float64(334158675.7873893), np.float64(332454963.1697536), np.float64(330716595.82119), np.float64(300643552.0327433), np.float64(298632827.3483493), np.float64(296584782.9853021), np.float64(294498786.24687004), np.float64(292374224.30063593), np.float64(290210502.08999455), np.float64(288007040.00488704), np.float64(285763271.290641), np.float64(283478639.1719543), np.float64(281152593.6670879), np.float64(278784588.06517285), np.float64(276374075.03718054), np.float64(273920502.3485454), np.float64(271423308.45842856), np.float64(268881921.5171827), np.float64(266295760.82470593), np.float64(263664238.50792623), np.float64(260986761.39390677), np.float64(258262733.09684077), np.float64(255491556.33886456), np.float64(252672635.52649277), np.float64(249805379.6064816), np.float64(246889205.22717583), np.float64(243923540.115159), np.float64(240907825.44927478), np.float64(237841517.60326377), np.float64(234724090.03397816), np.float64(231555035.34157008), np.float64(228333867.51709822), np.float64(225060124.39443398), np.float64(221733370.32495818), np.float64(218353199.0952902), np.float64(214919237.1106753), np.float64(211431147.01165727), np.float64(207888631.97908142), np.float64(204291440.5001277), np.float64(200639371.58676937), np.float64(196932280.48978117), np.float64(193170084.95577192), np.float64(189352772.07951853), np.float64(185480405.80921635), np.float64(181553135.1669796), np.float64(177571203.02891397), np.float64(173534955.2383873), np.float64(169444850.50351834), np.float64(165301471.2204059), np.float64(161105535.31335187), np.float64(156857909.19301617), np.float64(152559621.94424996), np.float64(148211880.86740136), np.float64(143816088.3932803), np.float64(139373859.885193), np.float64(134887042.841919), np.float64(130357737.92141245), np.float64(125788321.97301906), np.float64(121181473.2865017), np.float64(116540199.2897771), np.float64(111867866.95048551), np.float64(107168235.01327173), np.float64(102445486.4689096), np.float64(97704263.60562772), np.float64(92949706.33782005), np.float64(88187494.15629229), np.float64(83423892.08445784), np.float64(78665801.06168434), np.float64(73920811.12200604), np.float64(69197254.71339145), np.float64(64504264.14466441), np.float64(59851834.25285787), np.float64(55250890.83710378), np.float64(50713365.46993595), np.float64(46252269.24718685), np.float64(41881737.66275324), np.float64(37617066.624978535), np.float64(33474747.18076925), np.float64(29472498.33246448), np.float64(25629296.82570032), np.float64(21965396.978316333), np.float64(18502339.24935622), np.float64(15262950.146019477), np.float64(12271331.590466425), np.float64(9552671.230083881), np.float64(7132351.668452462), np.float64(5034707.15756969), np.float64(3281528.7894682274), np.float64(1890874.34250526), np.float64(876634.8625176384), np.float64(247100.6620326497), np.float64(-17102.687563579086), np.float64(-8867.502181666337), np.float64(-3067.3373109389004), np.float64(0.0)]  # Compressive stresses at rib positions [Pa]
panelThickness = 0.010  # Panel thickness [m]
span = 13.75 # span [m]

print(marginOfSafetyList(stringerPositions, ribPositions, compressiveStressesList, panelThickness))
