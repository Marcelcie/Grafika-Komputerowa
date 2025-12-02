import sys
import random
from glfw.GLFW import *
from OpenGL.GL import *

CURRENT_TASK = 0.0

def startup():
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, width, height)
    aspectRatio = width / height
    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_rect(x, y, a, b, d=0.0):
    deformed_a = a * (1.0 + d)
    deformed_b = b * (1.0 + d)

    x1, y1 = x, y
    x2, y2 = x, y + deformed_b
    x3, y3 = x + deformed_a, y + deformed_b
    x4, y4 = x + deformed_a, y

    if d > 0.0:
        random_r = random.random()
        random_g = random.random()
        random_b = random.random()
        glColor3f(random_r, random_g, random_b)
    else:
        glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glVertex2f(x3, y3)
    glVertex2f(x4, y4)
    glVertex2f(x1, y1)
    glEnd()

def render(time):
    global CURRENT_TASK

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    if CURRENT_TASK == 3.0:
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex2f(0.0, 50.0)
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(-50.0, -50.0)
        glColor3f(0.0, 0.0, 1.0)
        glVertex2f(50.0, -50.0)
        glEnd()

    elif CURRENT_TASK == 3.5:
        draw_rect(-50.0, -50.0, 100.0, 100.0, d=0.0)
        draw_rect(10.0, 60.0, 30.0, 20.0, d=0.0)

    elif CURRENT_TASK == 4.0:
        draw_rect(-90.0, 10.0, 50.0, 50.0, d=0.3)
        deform_factor_1 = random.uniform(0.0, 0.5)
        draw_rect(-50.0, -80.0, 40.0, 40.0, d=deform_factor_1)
        deform_factor_2 = random.uniform(0.0, 0.8)
        draw_rect(30.0, -40.0, 30.0, 60.0, d=deform_factor_2)

    glFlush()

def main():
    global CURRENT_TASK

    while CURRENT_TASK not in [3.0, 3.5, 4.0]:
        try:
            choice = input("Wybierz zadanie do wyświetlenia (3.0, 3.5, 4.0): ")
            CURRENT_TASK = float(choice)
            if CURRENT_TASK not in [3.0, 3.5, 4.0]:
                print("Nieprawidłowy wybór. Wprowadź 3.0, 3.5 lub 4.0.")
        except ValueError:
            print("Wprowadź liczbę (np. 3.0).")

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, f"Laboratorium 2 - Zadanie {CURRENT_TASK}", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSwapInterval(1)

    glfwSetFramebufferSizeCallback(window, update_viewport)
    update_viewport(None, 400, 400)

    startup()

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()

if __name__ == '__main__':
    main()