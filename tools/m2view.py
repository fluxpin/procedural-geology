#!/usr/bin/python -tt

from __future__ import division

import math
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from midpoint2 import midpoint_displace

TERRAIN = []

# Altazimuth
R = 50.0
ALT = 45.0
AZ = 0.0
# Cartesian
X = 0.0
Y = 0.0
Z = 0.0

def colorize(alt):
    if alt < 0.25:
        glColor3f(0.0, 0.0, 1.0)
    elif alt > 0.75:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(alt, alt, alt)

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(X, Y, Z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glTranslatef(-len(TERRAIN) / 2.0, 0.0, -len(TERRAIN) / 2.0)
    for y in range(0, len(TERRAIN)):
        glBegin(GL_TRIANGLE_STRIP)
        for x in range(0, len(TERRAIN) + 1):
            colorize(TERRAIN[y][x])
            glVertex3f(x, TERRAIN[y][x] * 10.0, y)
            colorize(TERRAIN[y + 1][x])
            glVertex3f(x, TERRAIN[y + 1][x] * 10.0, y + 1.0)
        glEnd()

    glutSwapBuffers()

def altaz_to_cart():
    global X, Y, Z
    X = R * math.cos(math.radians(ALT)) * math.sin(math.radians(AZ))
    Y = R * math.sin(math.radians(ALT))
    Z = R * math.cos(math.radians(ALT)) * math.cos(math.radians(AZ))

def setup():
    global TERRAIN
    glEnable(GL_DEPTH_TEST)
    altaz_to_cart()
    TERRAIN = midpoint_displace(32, 1.0)

def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global R, ALT, AZ
    global TERRAIN

    if key == 'z' and R > 10.0:
        R -= 1.0
    elif key == 'Z' and R < 50.0:
        R += 1.0
    elif key == 'w' and ALT < 45.0:
        ALT += 1.0
    elif key == 's' and ALT > -45.0:
        ALT -= 1.0
    elif key == 'a' and AZ > -90.0:
        AZ -= 1.0
    elif key == 'd' and AZ < 90.0:
        AZ += 1.0
    elif key == 'r':
        TERRAIN = midpoint_displace(32, 1.0)

    altaz_to_cart()
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE)
    glutCreateWindow(sys.argv[0])
    setup()
    glutDisplayFunc(draw)
    glutReshapeFunc(resize)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == '__main__':
    main()
