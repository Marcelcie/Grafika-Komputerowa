import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

light_x = 0.0

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_DEPTH_TEST)

    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    light_position = [0.0, 3.0, 5.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.2, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.0, 0.0, 1.0, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    mat_ambient = [0.2, 0.1, 0.1, 1.0]
    mat_diffuse = [0.8, 0.2, 0.2, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [50.0]

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 2, 5, 0, 0, 0, 0, 1, 0)
    glutSolidTeapot(1.2)
    glutSwapBuffers()
    glLightfv(GL_LIGHT0, GL_POSITION, [light_x, 0.0, 10.0, 1.0])
    glLightfv(GL_LIGHT1, GL_POSITION, [light_x, 0.0, 0.0, 1.0])

def keys(key, x, y):
    global light_x
    if key == b'[': light_x -= 0.5  # Światło w lewo
    if key == b']': light_x += 0.5  # Światło w prawo
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
    glutCreateWindow(b"Lab 5 - Oswietlenie Phonga 3.0")
    glutKeyboardFunc(keys)
    setup_lighting()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(display)

    glutMainLoop()


if __name__ == "__main__":
    main()
