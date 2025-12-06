import sys
import random
import math
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
theta = 0.0
phi = 0.0
scale = 1.0
pix2angle = 1.0

N = 50
V_TAB = np.zeros((N, N, 6), dtype=np.float32)


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

            V_TAB[i, j, 0] = x_val
            V_TAB[i, j, 1] = y_val
            V_TAB[i, j, 2] = z_val
            V_TAB[i, j, 3] = random.random()
            V_TAB[i, j, 4] = random.random()
            V_TAB[i, j, 5] = random.random()


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
    global pix2angle
    if height == 0:
        height = 1
    if width == 0:
        width = 1

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, width, height)

    aspect_ratio = width / height
    pix2angle = 360.0 / width

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 10.0, -10.0)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 10.0, -10.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if action == GLFW_PRESS:
        if button == GLFW_MOUSE_BUTTON_LEFT:
            left_mouse_button_pressed = 1
        elif button == GLFW_MOUSE_BUTTON_RIGHT:
            right_mouse_button_pressed = 1
    elif action == GLFW_RELEASE:
        if button == GLFW_MOUSE_BUTTON_LEFT:
            left_mouse_button_pressed = 0
        elif button == GLFW_MOUSE_BUTTON_RIGHT:
            right_mouse_button_pressed = 0


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old
    global theta, phi, scale

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if right_mouse_button_pressed:
        scale += delta_x * 0.01


def render(time):
    global theta, phi, scale

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)
    glScalef(scale, scale, scale)

    axes()

    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):
            glColor3f(V_TAB[i, j, 3], V_TAB[i, j, 4], V_TAB[i, j, 5])
            glVertex3f(V_TAB[i, j, 0], V_TAB[i, j, 1], V_TAB[i, j, 2])

            glColor3f(V_TAB[i + 1, j, 3], V_TAB[i + 1, j, 4], V_TAB[i + 1, j, 5])
            glVertex3f(V_TAB[i + 1, j, 0], V_TAB[i + 1, j, 1], V_TAB[i + 1, j, 2])

            glColor3f(V_TAB[i, j + 1, 3], V_TAB[i, j + 1, 4], V_TAB[i, j + 1, 5])
            glVertex3f(V_TAB[i, j + 1, 0], V_TAB[i, j + 1, 1], V_TAB[i, j + 1, 2])

            glColor3f(V_TAB[i + 1, j, 3], V_TAB[i + 1, j, 4], V_TAB[i + 1, j, 5])
            glVertex3f(V_TAB[i + 1, j, 0], V_TAB[i + 1, j, 1], V_TAB[i + 1, j, 2])

            glColor3f(V_TAB[i + 1, j + 1, 3], V_TAB[i + 1, j + 1, 4], V_TAB[i + 1, j + 1, 5])
            glVertex3f(V_TAB[i + 1, j + 1, 0], V_TAB[i + 1, j + 1, 1], V_TAB[i + 1, j + 1, 2])

            glColor3f(V_TAB[i, j + 1, 3], V_TAB[i, j + 1, 4], V_TAB[i, j + 1, 5])
            glVertex3f(V_TAB[i, j + 1, 0], V_TAB[i, j + 1, 1], V_TAB[i, j + 1, 2])
    glEnd()

    glFlush()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Lab 4 - Zadanie 3.5", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)

    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)

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