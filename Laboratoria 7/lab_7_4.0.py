import sys
import math
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

vertex_shader = """
#version 330 core
layout (location = 0) in vec3 aPos;
uniform mat4 transform;
void main() {
    gl_Position = transform * vec4(aPos, 1.0);
}
"""

fragment_shader = """
#version 330 core
out vec4 FragColor;
uniform vec3 objectColor;
void main() {
    FragColor = vec4(objectColor, 1.0);
}
"""


def get_rotation_matrix(angle):
    s = math.sin(angle)
    c = math.cos(angle)
    return np.array([
        [c, -s, 0.0, 0.0],
        [s, c, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)


def get_translation_matrix(x, y):
    return np.array([
        [1.0, 0.0, 0.0, x],
        [0.0, 1.0, 0.0, y],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)


def main():
    if not glfwInit(): return

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    window = glfwCreateWindow(800, 600, "Lab 7 - Zadanie 4.0", None, None)
    glfwMakeContextCurrent(window)

    shader = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    vertices = np.array([
        -0.2, -0.2, 0.0,
        0.2, -0.2, 0.0,
        0.0, 0.2, 0.0
    ], dtype=np.float32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, None)
    glEnableVertexAttribArray(0)

    transform_loc = glGetUniformLocation(shader, "transform")
    color_loc = glGetUniformLocation(shader, "objectColor")

    while not glfwWindowShouldClose(window):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader)

        time = glfwGetTime()

        # Rysowanie 5 różnych obiektów
        for i in range(5):
            angle = time + i
            x_pos = 0.6 * math.cos(time + i * 1.2)
            y_pos = 0.6 * math.sin(time + i * 1.2)

            rot = get_rotation_matrix(angle)
            trans = get_translation_matrix(x_pos, y_pos)

            # Łączenie macierzy (Mnożenie Macierzy)
            model_matrix = np.matmul(trans, rot)

            glUniformMatrix4fv(transform_loc, 1, GL_TRUE, model_matrix)

            # Zmiana koloru dla każdego obiektu
            color = [0.2 * i, 0.5, 1.0 - 0.2 * i]
            glUniform3fv(color_loc, 1, color)

            glBindVertexArray(VAO)
            glDrawArrays(GL_TRIANGLES, 0, 3)

        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == "__main__":
    main()