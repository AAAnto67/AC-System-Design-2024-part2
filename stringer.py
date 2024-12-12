class StringerL:
    '''L stringer. Origin of cartesian coordinates at the bottom left corner where the two plates intersect.'''
    def __init__(self, thickness, base, height):
        self.t = thickness
        self.b = base
        self.h = height

        # GEOMETRIC PROPERTIES

        # vertical section
        self.A_1 = self.h * self.t
        self.x_dilda_1 = self.t / 2
        self.y_dilda_1 = self.h / 2

        # horizontal section
        self.A_2 = (self.b - self.t) * self.t
        self.x_dilda_2 = self.t + (self.b - self.t) / 2
        self.y_dilda_2 = self.t / 2



    def centroid(self):

        '''returns a tuple of (X,y) coordinates of the l stringer with respecto to bottom left corner of L oreinted L stringer'''
        total_area = self.A_1 + self.A_2

        x_centroid = (self.x_dilda_1 * self.A_1 + self.x_dilda_2 * self.A_2) / total_area
        y_centroid = (self.y_dilda_1 * self.A_1 + self.y_dilda_2 * self.A_2) / total_area

        return (x_centroid, y_centroid)

    def momentsOfAreas(self):
        '''returns second moments of areas about the pair of orthogonal axis. X-axis parallel to base of the L stringer and y axis parallel to the height.'''
        t = self.t
        b = self.b
        h = self.h

        x_bar, y_bar = self.centroid()

        # vertical section
        I_x_1 = 1/12 * t * h**3
        I_y_1 = 1/12 * h * t**3

        # horizontal section
        I_x_2 = 1/12 * (b - t) * t**3
        I_y_2 = 1/12 * t * (b - t)**3

        # overall moments of inertia
        I_xx = I_x_1 + self.A_1 * (self.y_dilda_1 - y_bar)**2 + I_x_2 + self.A_2 * (self.y_dilda_2 - y_bar)**2 
        I_yy = I_y_1 + self.A_1 * (self.x_dilda_1 - x_bar)**2 + I_y_2 + self.A_2 * (self.x_dilda_2 - x_bar)**2
        I_xy = self.A_1 * (self.y_dilda_1 - y_bar) * (self.x_dilda_1 - x_bar) + self.A_2 * (self.y_dilda_2 - y_bar) * (self.x_dilda_2 - x_bar) 

        return I_xx, I_yy, I_xy