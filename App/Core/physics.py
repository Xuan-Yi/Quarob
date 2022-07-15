import time
import numpy as np

from Core.parameters import *
from Core.kinetic import Kinetic

# Quarob Physical Simulation Engine
g = 9.80665 # m/s^2

class QPhySE:
    def __init__(self,init_enkle_angles:list = [0]*12):
        self.kinetic_calc = Kinetic()   # kinetic calculator
        # body
        self.gyro_pos = [0,0,0]
        self.gyro_rot = [0,0,0]
        self.kinetic_calc.set_gyro_parameters(self.gyro_pos,self.gyro_rot)
        # points
        self.angles = init_enkle_angles
        self.kinetic_calc.set_ankle_angles(self.angles)
        self.pts= self.kinetic_calc.getAnkle_pos(self.angles)   # cosition of points(enkles)
        for pt in self.pts:
            pt.v = np.zeros(3)
            pt.a = np.zeros(3)
        # COM
        self.COM = self.kinetic_calc.getCOM_pos()
        # timer
        self.t = time.time()    # init time

    def setNewPointPositions(self,new_enkle_angles:list = [0]*12):
        new_angles= new_enkle_angles
        
        # calculate velocity
        new_pts = self.kinetic_calc.getAnkle_pos(self.angles)
    