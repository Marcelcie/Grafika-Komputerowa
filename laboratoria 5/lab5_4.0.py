import sys
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

theta = 0.0
phi = 0.0
R = 10.0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
left_mouse_button_pressed = 0

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.2, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.0, 0.0, 1.0, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.1, 0.1, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

def display():
    global theta, phi, R
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 2, 15, 0, 0, 0, 0, 1, 0)

    th_rad = theta * math.pi / 180.0
    ph_rad = phi * math.pi / 180.0

    x = R * math.cos(th_rad) * math.cos(ph_rad)
    y = R * math.sin(ph_rad)
    z = R * math.sin(th_rad) * math.cos(ph_rad)

    glLightfv(GL_LIGHT0, GL_POSITION, [x, y, z, 1.0])
    glLightfv(GL_LIGHT1, GL_POSITION, [-x, -y, z, 1.0])

    glPushMatrix()
    glDisable(GL_LIGHTING)
    glTranslatef(x, y, z)
    glColor3f(1.0, 1.0, 1.0)
    glutWireSphere(0.2, 10, 10)
    glEnable(GL_LIGHTING)
    glPopMatrix()

    glPushMatrix()
    glDisable(GL_LIGHTING)
    glTranslatef(-x, -y, z)
    glColor3f(0.0, 0.0, 1.0)
    glutWireSphere(0.2, 10, 10)
    glEnable(GL_LIGHTING)
    glPopMatrix()

    glutSolidTeapot(2.0)
    glutSwapBuffers()

def mouse(button, state, x, y):
    global left_mouse_button_pressed, mouse_x_pos_old, mouse_y_pos_old
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        left_mouse_button_pressed = 1
        mouse_x_pos_old = x
        mouse_y_pos_old = y
    elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        left_mouse_button_pressed = 0

def motion(x, y):
    global theta, phi, mouse_x_pos_old, mouse_y_pos_old
    if left_mouse_button_pressed:
        theta += (x - mouse_x_pos_old) * 0.5
        phi += (y - mouse_y_pos_old) * 0.5
        mouse_x_pos_old = x
        mouse_y_pos_old = y
    glutPostRedisplay()

def reshape(w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Lab 5 - 4.0")
    setup_lighting()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutIdleFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()