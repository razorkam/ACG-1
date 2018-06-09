import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import (GL_ARRAY_BUFFER,
                       GL_FALSE, GL_FLOAT,
                       GL_STATIC_DRAW,GL_ELEMENT_ARRAY_BUFFER,
                       GL_PRIMITIVE_RESTART,glBindBuffer,
                       glBindVertexArray,glEnableVertexAttribArray,
                       glGenBuffers, glGenVertexArrays,
                       glVertexAttribPointer,glBufferData,
                       glEnable, glPrimitiveRestartIndex)
from light_math import normalize
from random import randint
import math

def create_grad(rows, cols, size):
    # y = 5*x + z*z
    vertices_list = []

    def der_x(x):
        return math.sin(x)

    def der_z(z):
        return math.cos(z)

    for z in range(0, 50):
        for x in range(0, 50):
            d_x = der_x(x)
            d_z = der_z(z)


            vertices_list.append([x, 0.0, z])
            vertices_list.append([x+d_x, 0.0, z+d_z])

    vertices_vec = np.array(vertices_list, dtype=np.float32)

    vao = glGenVertexArrays(1)
    vbo_vertices = glGenBuffers(1)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices_vec), vertices_vec.flatten(), GL_STATIC_DRAW)  #
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)








    glBindVertexArray(0)

    return (vao, len(vertices_list))