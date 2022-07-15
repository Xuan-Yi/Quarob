import numpy as np
from math import *

from Core.parameters import *

'''
body_len = 0.1185
shoulder_width = 0.0642
thigh_len = 0.0420
calf_len = 0.0417
feet_radius = 0.010
'''


def rotate_x(theta_x: float):   # theta_x: in degree
    t = theta_x*pi/180.0    # t: in radian
    x_rotate_matrix = np.array([
        [1, 0, 0],
        [0, cos(t), -sin(t)],
        [0, sin(t), cos(t)]
    ])
    return x_rotate_matrix


def rotate_y(theta_y: float):  # theta_y: in degree
    t = theta_y*pi/180.0    # t: in radian
    y_rotate_matrix = np.array([
        [cos(t), 0, sin(t)],
        [0, 1, 0],
        [-sin(t), 0, cos(t)]
    ])
    return y_rotate_matrix


def rotate_z(theta_z: float):  # theta_y: in degree
    t = theta_z*pi/180.0    # t: in radian
    z_rotate_matrix = np.array([
        [cos(t), -sin(t), 0],
        [sin(t), cos(t), 0],
        [0, 0, 1]
    ])
    return z_rotate_matrix


'''gyro_displacement = [0, 0, 0]  # x, y, z
gyro_angle = [45, 0, 0]  # roll, pitch, yaw in degree

angles = [
    0, -45, 0,
    0, 45, 0,
    0, -45, 0,
    0, 45, 0
]  # ankle angles in degree'''


class Kinetic:
    def __init__(self):
        self.angles = [0]*12    # angle of ankles
        self.gyro_displacement = [0, 0, 0]  # displacement of quarob
        self.gyro_angle = [0, 0, 0]  # rotation of quarob
        self.pts_pos = [0]*12    # coordinete of angles [(x, y, z)]*12
        self.parameter_change = False

    def __caculate_shoulder_pos(self):
        self.pts_pos[0] = np.array([shoulder_width/2, body_len/2, 0])
        self.pts_pos[3] = np.array([-shoulder_width/2, body_len/2, 0])
        self.pts_pos[6] = np.array([shoulder_width/2, -body_len/2, 0])
        self.pts_pos[9] = np.array([-shoulder_width/2, -body_len/2, 0])

    def __calculate_knee_feet_pos(self):
        # pos_arr[1] and pos_arr[2]
        pos1 = np.array([0, 0, -thigh_len])
        pos1 = np.matmul(pos1, rotate_x(-self.angles[1]))
        pos2 = np.array([0, calf_len, 0])
        pos2 = np.matmul(pos2, rotate_x(-self.angles[1]-self.angles[2]))
        pos2 += pos1
        pos1 = np.matmul(pos1, rotate_y(-self.angles[0]))
        pos2 = np.matmul(pos2, rotate_y(-self.angles[0]))
        self.pts_pos[1] = self.pts_pos[0]+pos1
        self.pts_pos[2] = self.pts_pos[0]+pos2
        # pos_arr[4] and pos_arr[5]
        pos4 = np.array([0, 0, -thigh_len])
        pos4 = np.matmul(pos4, rotate_x(self.angles[4]))
        pos5 = np.array([0, calf_len, 0])
        pos5 = np.matmul(pos5, rotate_x(self.angles[4]+self.angles[5]))
        pos5 += pos4
        pos4 = np.matmul(pos4, rotate_y(-self.angles[3]))
        pos5 = np.matmul(pos5, rotate_y(-self.angles[3]))
        self.pts_pos[4] = self.pts_pos[3]+pos4
        self.pts_pos[5] = self.pts_pos[3]+pos5
        # pos_arr[7]
        pos7 = np.array([0, 0, -thigh_len])
        pos7 = np.matmul(pos7, rotate_x(-self.angles[7]))
        pos8 = np.array([0, calf_len, 0])
        pos8 = np.matmul(pos8, rotate_x(-self.angles[7]-self.angles[8]))
        pos8 += pos7
        pos7 = np.matmul(pos7, rotate_y(self.angles[6]))
        pos8 = np.matmul(pos8, rotate_y(self.angles[6]))
        self.pts_pos[7] = self.pts_pos[6]+pos7
        self.pts_pos[8] = self.pts_pos[6]+pos8
        # pos_arr[10]
        pos10 = np.array([0, 0, -thigh_len])
        pos10 = np.matmul(pos10, rotate_x(self.angles[10]))
        pos11 = np.array([0, calf_len, 0])
        pos11 = np.matmul(pos11, rotate_x(self.angles[10]+self.angles[11]))
        pos11 += pos10
        pos10 = np.matmul(pos10, rotate_y(self.angles[9]))
        pos11 = np.matmul(pos11, rotate_y(self.angles[9]))
        self.pts_pos[10] = self.pts_pos[9]+pos10
        self.pts_pos[11] = self.pts_pos[9]+pos11

    def __calculate_gyro_effect(self):
        for i in range(12):
            pos = self.pts_pos[i]
            pos = np.matmul(pos, rotate_x(-self.gyro_angle[0]))
            pos = np.matmul(pos, rotate_y(-self.gyro_angle[1]))
            pos = np.matmul(pos, rotate_z(-self.gyro_angle[2]))
            self.pts_pos[i] = pos
            # miss displacement
            pos += self.gyro_displacement

    def set_ankle_angles(self, angles: list):
        if angles != self.angles:
            self.parameter_change = True
            self.angles = angles

    def set_gyro_parameters(self, displacement: list, rotation: list):
        if displacement != self.gyro_displacement or rotation != self.gyro_angle:
            self.parameter_change = True
            self.gyro_displacement = displacement
            self.gyro_angle = rotation

    def __update_ankles(self):
        if self.parameter_change:
            # Calculate position of knees before rotation and movement
            self.__caculate_shoulder_pos()
            self.__calculate_knee_feet_pos()
            # Calculate position of knees after rotation and movement
            self.__calculate_gyro_effect()
            self.parameter_change = False

    def getAnkle_pos(self):
        self.__update_ankles()
        return self.pts_pos

    def getCOM_pos(self):
        self.__update_ankles()
        # calculate COM
        points = self.pts_pos
        body_pos = (points[0]+points[3]+points[6]+points[9])/4.0
        servos_pos = (points[0]+points[3]+points[6]+points[9]) * \
            2+(points[1]+points[4]+points[7]+points[10])
        hips_pos = (points[0]+points[3]+points[6]+points[9])
        thighs_pos = (points[0]+points[1]+points[3]+points[4] +
                      points[6]+points[7]+points[9]+points[10])/2.0
        calfs_pos = points[2]+points[5]+points[8]+points[11]

        COM = (body_pos*body_weight+servos_pos*servo_weight+hips_pos *
               hip_weight+thighs_pos*thigh_weight+calfs_pos*calf_weight)/total_weight
        return COM
