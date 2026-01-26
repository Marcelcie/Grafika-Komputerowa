import sys
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
R = 10.0
pix2angle = 1.0

N = 50
V_TAB = np.zeros((N, N, 3), dtype=np.float32)

def calculate_egg_vertices():
    u_values = np.linspace(0.0, 1.0, N)
    v_values = np.linspace(0.0, 1.0, N)
    for i in range(N):
        u = u_values[i]
        for j in range(N):
            v = v_values[j]
            x_z_factor = (-90.0 * u**5 + 225.0 * u**4 - 270.0 * u**3 + 180.0 * u**2 - 45.0 * u)
            x_val = x_z_factor * math.cos(math.pi * v)
            y_val = 160.0 * u**4 - 320.0 * u**3 + 160.0 * u**2 - 5.0
            z_val = x_z_factor * math.sin(math.pi * v)
            V_TAB[i, j, 0] = x_val
            V_TAB[i, j, 1] = y_val
            V_TAB[i, j, 2] = z_val

def startup():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    calculate_egg_vertices()

def update_viewport(window, width, height):
    global pix2angle
    if height == 0: height = 1
    glViewport(0, 0, width, height)
    aspect_ratio = width / height
    pix2angle = 360.0 / width
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70.0, aspect_ratio, 0.1, 300.0)
    glMatrixMode(GL_MODELVIEW)

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
    global mouse_x_pos_old, mouse_y_pos_old, theta, phi, R
    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if right_mouse_button_pressed:
        R += delta_y * 0.1
        if R < 0.1: R = 0.1

def render(time):
    global theta, phi, R
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    th_rad = theta * math.pi / 180.0
    ph_rad = phi * math.pi / 180.0

    x_eye = R * math.cos(th_rad) * math.cos(ph_rad)
    y_eye = R * math.sin(ph_rad)
    z_eye = R * math.sin(th_rad) * math.cos(ph_rad)

    up_y = 1.0
    if (90 < (phi % 360) < 270) or (-270 < (phi % 360) < -90):
        up_y = -1.0

    gluLookAt(x_eye, y_eye, z_eye, 0.0, 0.0, 0.0, 0.0, up_y, 0.0)

    glPointSize(2.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(N):
        for j in range(N):
            glVertex3f(V_TAB[i, j, 0], V_TAB[i, j, 1], V_TAB[i, j, 2])
    glEnd()
    glFlush()

def main():
    if not glfwInit(): sys.exit(-1)
    window = glfwCreateWindow(600, 600, "Lab 4 - Zadanie 3.5", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    startup()
    update_viewport(None, 600, 600)
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    glfwTerminate()

if __name__ == '__main__':
    main()