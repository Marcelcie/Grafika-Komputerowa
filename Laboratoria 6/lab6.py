from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import sys

texture_id = 0


def load_texture(filename):
    global texture_id

    try:
        image = Image.open(filename)
    except IOError:
        print(f"Błąd: Nie znaleziono pliku {filename}")
        return

    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    img_data = image.convert("RGBA").tobytes()
    width, height = image.size

    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_QUADS)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)


    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)


    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 0.0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, 0.0)

    glEnd()

    glutSwapBuffers()


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
    glutCreateWindow(b"Lab 6 - Teksturowanie 3.0")

    load_texture("tekstura.png")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glutMainLoop()


if __name__ == "__main__":
    main()