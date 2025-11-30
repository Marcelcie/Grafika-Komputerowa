import sys
import math
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 50
V_TAB = np.zeros((N, N, 3), dtype=np.float32)


def calculate_egg_vertices():
    u_values = np.linspace(0.0, 1.0, N)
    v_values = np.linspace(0.0, 1.0, N)

    for i in range(N):
        u = u_values[i]
        for j in range(N):
            v = v_values[j]

            x_z_factor = (-90.0 * u ** 5 + 225.0 * u ** 4 - 270.0 * u ** 3 + 180.0 * u ** 2 - 45.0 * u)
            x_val = x_z_factor * math.cos(math.pi * v)
            y_val = 160.0 * u ** 4 - 320.0 * u ** 3 + 160.0 * u ** 2 - 5.0
            z_val = x_z_factor * math.sin(math.pi * v)

            V_TAB[i, j] = [x_val, y_val, z_val]


def startup():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    calculate_egg_vertices()


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()


def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, width, height)

    aspect_ratio = width / height

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 10.0, -10.0)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 10.0, -10.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    angle = time * 180.0 / math.pi
    glRotatef(angle, 1.0, 1.0, 1.0)

    axes()

    glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_LINES)
    for i in range(N):
        for j in range(N):
            if i < N - 1:
                glVertex3f(V_TAB[i, j, 0], V_TAB[i, j, 1], V_TAB[i, j, 2])
                glVertex3f(V_TAB[i + 1, j, 0], V_TAB[i + 1, j, 1], V_TAB[i + 1, j, 2])

            if j < N - 1:
                glVertex3f(V_TAB[i, j, 0], V_TAB[i, j, 1], V_TAB[i, j, 2])
                glVertex3f(V_TAB[i, j + 1, 0], V_TAB[i, j + 1, 1], V_TAB[i, j + 1, 2])
    glEnd()

    glFlush()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Lab 3 - Zadanie 3.5", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    update_viewport(None, 400, 400)

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()


if __name__ == '__main__':
    main()