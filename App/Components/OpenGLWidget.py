from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from Core.parameters import *
from Core.kinetic import Kinetic

body_edges = [(0, 3), (3, 9), (9, 6), (6, 0)]
body_polygan = [0, 3, 9, 6]
limbs = [
    (0, 1), (1, 2),     # front right
    (3, 4), (4, 5),     # front left
    (6, 7), (7, 8),     # back right
    (9, 10), (10, 11)   # back left
]
foot = [2, 5, 8, 11]


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, perspective: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.perspective = perspective  # 3D, Look Down
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(0)
        # posture
        self.Quarob_pos = [0]*3  # (0,0,0)
        self.Quarob_rot = [0]*3  # (0,0,0)
        self.Quarob_servo_rot = [0]*12  # angles = 0
        # kinetic object
        self.kinetic = Kinetic()
        self.k = 0

    def initializeGL(self):
        # opengl
        glutInit()
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        # Do NOT enable light source or the color will be covered.

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(.1, 0, 0, 1)
        # paint
        self.__paint_ground()
        self.__paint_Quarob()
        glFlush()

    def __paint_Quarob(self):
        # test
        self.k += 1
        angles = [(self.k % 150)-75]*12
        angles[0] = 0
        angles[3] = 0
        angles[6] = 0
        angles[9] = 0
        pos = [0, 0, (self.k % 1000)/1000.0]
        rot = [0, 0, (self.k % 1000)/1000*30-15]
        self.setPosture(pos, rot, angles)
        if self.k%100 == 0:
            print(f'COM: {self.kinetic.getCOM_pos()}')
        # get points
        points = self.kinetic.getAnkle_pos()
        # paint
        leg_color = (1, 1, 1, 1)
        body_color = (.7, .7, .7, .1)
        feet_color = (1, 0, 0, .5)
        COM_color = (0, 0, 1, .7)

        glColor4fv(leg_color)
        glLineWidth(4)
        glBegin(GL_LINES)
        for edge in (body_edges+limbs):
            for vertex in edge:
                glVertex3fv(points[vertex])
        glEnd()
        glColor4fv(body_color)
        glBegin(GL_QUADS)
        for vertex in body_polygan:
            glVertex3fv(points[vertex])
        glEnd()
        glColor4fv(feet_color)
        glPointSize(2*feet_radius)
        glEnable(GL_POINT_SMOOTH)
        glBegin(GL_POINTS)
        for vertex in foot:
            glVertex3fv(points[vertex])
        glEnd()
        glDisable(GL_POINT_SMOOTH)
        glColor4fv(COM_color)
        glPointSize(12)
        glEnable(GL_POINT_SMOOTH)
        glBegin(GL_POINTS)
        COM = self.kinetic.getCOM_pos()
        glVertex3fv(COM)
        glEnd()
        glDisable(GL_POINT_SMOOTH)

    def __paint_ground(self):
        ground_size = (60, 60)  # (x,y) in cm
        ground_range_x = [self.Quarob_pos[0]-ground_size[0] /
                          2.0, self.Quarob_pos[0]+ground_size[0]/2.0]
        ground_range_y = [self.Quarob_pos[1]-ground_size[1] /
                          2.0, self.Quarob_pos[1]+ground_size[1]/2.0]
        ground_color = (0, .9, .9, .3)
        glColor4fv(ground_color)
        glLineWidth(.5)
        glBegin(GL_LINES)
        # lines horizontal to x
        for x in range(int(ground_range_x[0]), int(ground_range_x[1])):
            for y in ground_range_y:
                glVertex3fv([x/10, y/10, 0])
        # lines horizontal to y
        for y in range(int(ground_range_y[0]), int(ground_range_y[1])):
            for x in ground_range_x:
                glVertex3fv([x/10, y/10, 0])
        glEnd()

    def resizeGL(self, w, h):
        self.GL_size = (w, h)
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, w/h, .5, 50)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # camera
        Quarob_pos = np.array(self.Quarob_pos)
        if self.perspective == 'Look Down':  # Look Down
            camera_pos = Quarob_pos+np.array([0, 0, thigh_len+calf_len])*16
            target_pos = Quarob_pos
            up_vec = np.array([0, 1, 0])
        else:   # 3D
            camera_pos = Quarob_pos+np.array(
                [shoulder_width, body_len, thigh_len+calf_len])*6
            camera_pos[2] = camera_pos[2]-Quarob_pos[2]
            target_pos = Quarob_pos
            up_vec = Quarob_pos + np.cross((target_pos - camera_pos),
                                           np.array([camera_pos[1], -camera_pos[0], 0]))

        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
                  target_pos[0], target_pos[1], target_pos[2],
                  up_vec[0], up_vec[1], up_vec[2])

    def setPerspective(self, perspective: str):
        self.perspective = perspective
        # Change camera perspective
        self.makeCurrent()  # change to current canvas
        self.resizeGL(self.GL_size[0], self.GL_size[1])

    def setPosture(self, pos: list, rot: list, servo_angles: list):
        self.Quarob_pos = pos
        self.Quarob_rot = rot
        self.Quarob_servo_rot = servo_angles
        # calculate points
        self.kinetic.set_gyro_parameters(pos, rot)
        self.kinetic.set_ankle_angles(servo_angles)
        # Change camera perspective
        self.makeCurrent()  # change to current canvas
        self.resizeGL(self.GL_size[0], self.GL_size[1])
