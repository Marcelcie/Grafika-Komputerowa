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
V_TAB = np.zeros((N, N, 6), dtype=np.float32)

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light0_diffuse = [0.8, 0.8, 0.0, 1.0]
light0_ambient = [0.1, 0.1, 0.1, 1.0]
light0_specular = [1.0, 1.0, 1.0, 1.0]
light0_position = [0.0, 0.0, 10.0, 1.0]

light1_diffuse = [0.0, 0.0, 1.0, 1.0]
light1_ambient = [0.0, 0.0, 0.1, 1.0]
light1_specular = [1.0, 1.0, 1.0, 1.0]
light1_position = [-10.0, 0.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


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


def startup():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light0_ambient)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light0_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light0_position)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    calculate_egg_vertices()


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0);
    glVertex3f(-5.0, 0.0, 0.0);
    glVertex3f(5.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0);
    glVertex3f(0.0, -5.0, 0.0);
    glVertex3f(0.0, 5.0, 0.0)
    glColor3f(0.0, 0.0, 1.0);
    glVertex3f(0.0, 0.0, -5.0);
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()


def update_viewport(window, width, height):
    global pix2angle
    if height == 0: height = 1
    if width == 0: width = 1
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, width, height)
    aspect_ratio = width / height
    pix2angle = 360.0 / width
    gluPerspective(70.0, aspect_ratio, 0.1, 300.0)
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
    global mouse_x_pos_old, mouse_y_pos_old
    global theta, phi, R
    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos
    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
    if right_mouse_button_pressed:
        R += delta_y * 0.1
        if R < 0.1: R = 0.1


def keyboard_key_callback(window, key, scancode, action, mods):
    global light0_diffuse
    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_1 and light0_diffuse[0] > 0.1:
            light0_diffuse[0] -= 0.1
        elif key == GLFW_KEY_2 and light0_diffuse[0] < 1.0:
            light0_diffuse[0] += 0.1
        elif key == GLFW_KEY_3 and light0_diffuse[1] > 0.1:
            light0_diffuse[1] -= 0.1
        elif key == GLFW_KEY_4 and light0_diffuse[1] < 1.0:
            light0_diffuse[1] += 0.1
        print(f"R={light0_diffuse[0]:.1f}, G={light0_diffuse[1]:.1f}")


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
    if (phi > 90.0 and phi < 270.0) or (phi < -90.0 and phi > -270.0):
        up_y = -1.0
    gluLookAt(x_eye, y_eye, z_eye, 0.0, 0.0, 0.0, 0.0, up_y, 0.0)

    glLightfv(GL_LIGHT0, GL_DIFFUSE, light0_diffuse)

    axes()

    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):
            glVertex3f(V_TAB[i, j, 0], V_TAB[i, j, 1], V_TAB[i, j, 2])
            glVertex3f(V_TAB[i + 1, j, 0], V_TAB[i + 1, j, 1], V_TAB[i + 1, j, 2])
            glVertex3f(V_TAB[i, j + 1, 0], V_TAB[i, j + 1, 1], V_TAB[i, j + 1, 2])
            glVertex3f(V_TAB[i + 1, j, 0], V_TAB[i + 1, j, 1], V_TAB[i + 1, j, 2])
            glVertex3f(V_TAB[i + 1, j + 1, 0], V_TAB[i + 1, j + 1, 1], V_TAB[i + 1, j + 1, 2])
            glVertex3f(V_TAB[i, j + 1, 0], V_TAB[i, j + 1, 1], V_TAB[i, j + 1, 2])
    glEnd()
    glFlush()


def main():
    if not glfwInit(): sys.exit(-1)
    window = glfwCreateWindow(400, 400, "Lab 5 - Zadanie 3.5", None, None)
    if not window: glfwTerminate(); sys.exit(-1)
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetKeyCallback(window, keyboard_key_callback)
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