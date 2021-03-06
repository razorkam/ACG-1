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

def create_surface(rows, cols, size, fun, gen_textures,gen_relief = False):

    normals_vec = np.zeros((rows * cols, 3), dtype=np.float32)

    vertices_list = []
    texcoords_list = []
    faces_list = []
    indices_list = []

    if not gen_relief:
        for z in range(0, rows):
            for x in range(0, cols):
                xx = -size / 2 + x * size / cols
                zz = -size / 2 + z * size / rows

                try:
                    yy = fun(xx, zz)
                    if yy < -size/2:
                        yy = -size / 2
                    if yy > size/2:
                        yy = size / 2
                except (ArithmeticError, ValueError):
                    yy = 0.0

                vertices_list.append([xx, yy, zz])
                if gen_textures:
                    texcoords_list.append([x / float(cols - 1), z / float(rows - 1)])
    else:
        buff1 = []
        vertices_list_twodimensional = []
        for z in range(0, rows):
            buff1.clear()
            for x in range(0, cols):
                xx = -size / 2 + x * size / cols
                zz = -size / 2 + z * size / rows
                yy = 0.0

                buff1.append([xx, yy, zz])
            vertices_list_twodimensional.append(buff1.copy())

        for i in range(0, 150):
            radius = randint(1,15)
            z = randint(0,rows-1)
            x = randint(0,cols-1)
            for iz in range(z - radius,z + radius):
                if iz < 0 or iz > rows-1 :
                    continue
                else:
                    for ix in range(x - radius, x + radius):
                        if ix < 0 or ix > cols-1:
                            continue
                        else:
                            if 2*radius ** 2 - ((z - iz) ** 2 + (x - ix) ** 2) > vertices_list_twodimensional[iz][ix][1]**(2):
                                vertices_list_twodimensional[iz][ix][1] = (2*radius ** 2 - ((z - iz) ** 2 + (x - ix) ** 2))**(1/2)
                            else: continue
        v = vertices_list_twodimensional.copy()
        vec_lines = []
        for ii in range(0,10):
            i = 2 * ii
            for z in range(0, rows-1):
                for x in range(0, cols-1):
                    xx = -size / 2 + x * size / cols
                    zz = -size / 2 + z * size / rows

                    if v[z][x][1] < i and v[z][x + 1][1] < i and v[z + 1][x][1] < i and v[z + 1][x + 1][1] < i or \
                            v[z][x][1] >= i and v[z][x + 1][1] >= i and v[z + 1][x][1] >= i and v[z + 1][x + 1][1] >= i:
                        continue
                    elif v[z][x][1] >= i and v[z][x + 1][1] < i and v[z + 1][x][1] < i and v[z + 1][x + 1][1] < i:
                        vec_lines.append([xx + 0.25, i, zz])
                        vec_lines.append([xx, i, zz + 0.25])
                    elif v[z][x][1] < i and v[z][x + 1][1] >= i and v[z + 1][x][1] < i and v[z + 1][x + 1][1] < i:
                        vec_lines.append([xx + 0.25, i, zz])
                        vec_lines.append([xx + 0.5, i, zz + 0.25])
                    elif v[z][x][1] < i and v[z][x + 1][1] < i and v[z + 1][x][1] >= i and v[z + 1][x + 1][1] < i:
                        vec_lines.append([xx + 0.25, i, zz + 0.5])
                        vec_lines.append([xx, i, zz + 0.25])
                    elif v[z][x][1] < i and v[z][x + 1][1] < i and v[z + 1][x][1] < i and v[z + 1][x + 1][1] >= i:
                        vec_lines.append([xx + 0.25, i, zz + 0.5])
                        vec_lines.append([xx + 0.5, i, zz + 0.25])

                    elif v[z][x][1] < i and v[z][x + 1][1] >= i and v[z + 1][x][1] >= i and v[z + 1][x + 1][1] >= i:
                        vec_lines.append([xx + 0.25, i, zz])
                        vec_lines.append([xx, i, zz + 0.25])
                    elif v[z][x][1] >= i and v[z][x + 1][1] < i and v[z + 1][x][1] >= i and v[z + 1][x + 1][1] >= i:
                        vec_lines.append([xx + 0.25, i, zz])
                        vec_lines.append([xx + 0.5, i, zz + 0.25])
                    elif v[z][x][1] >= i and v[z][x + 1][1] >= i and v[z + 1][x][1] < i and v[z + 1][x + 1][1] >= i:
                        vec_lines.append([xx + 0.25, i, zz + 0.5])
                        vec_lines.append([xx, i, zz + 0.25])
                    elif v[z][x][1] >= i and v[z][x + 1][1] >= i and v[z + 1][x][1] >= i and v[z + 1][x + 1][1] < i:
                        vec_lines.append([xx + 0.25, i, zz + 0.5])
                        vec_lines.append([xx + 0.5, i, zz + 0.25])

                    elif v[z][x][1] < i and v[z][x + 1][1] < i and v[z + 1][x][1] >= i and v[z + 1][x + 1][1] >= i or \
                         v[z][x][1] >= i and v[z][x + 1][1] >= i and v[z + 1][x][1] < i and v[z + 1][x + 1][1] < i:
                        vec_lines.append([xx, i, zz + 0.25])
                        vec_lines.append([xx + 0.5, i, zz + 0.25])
                    elif v[z][x][1] >= i and v[z][x + 1][1] < i and v[z + 1][x][1] >= i and v[z + 1][x + 1][1] < i or \
                            v[z][x][1] < i and v[z][x + 1][1] >= i and v[z + 1][x][1] < i and v[z + 1][x + 1][1] >= i:
                        vec_lines.append([xx + 0.25, i, zz])
                        vec_lines.append([xx + 0.25, i, zz + 0.5])

                    elif v[z][x][1] >= i and v[z][x + 1][1] < i and v[z + 1][x][1] < i and v[z + 1][x + 1][1] >= i or \
                            v[z][x][1] < i and v[z][x + 1][1] >= i and v[z + 1][x][1] >= i and v[z + 1][x + 1][1] < i:
                        vec_lines.append([xx, i, zz + 0.25])
                        vec_lines.append([xx + 0.25, i, zz])
                        vec_lines.append([xx + 0.5, i, zz + 0.25])
                        vec_lines.append([xx + 0.25, i, zz + 0.5])


        index_lines = [it for it in range(0,len(vec_lines))]
        vector_lines = np.array(vec_lines, dtype=np.float32)
        vector_line_indexes = np.array(index_lines, dtype=np.uint32)


        for z in range(0, rows):
            for x in range(0, cols):
                vertices_list.append(vertices_list_twodimensional[z][x])





    primRestart = rows * cols
    vertices_vec = np.array(vertices_list, dtype=np.float32)
    if gen_textures:
        texcoords_vec = np.array(texcoords_list, dtype=np.float32)

    for x in range(0, cols - 1):
        for z in range(0, rows - 1):
            offset = x * cols + z
            if z == 0:
                indices_list.append(offset)
                indices_list.append(offset + rows)
                indices_list.append(offset + 1)
                indices_list.append(offset + rows + 1)
            else:
                indices_list.append(offset + 1)
                indices_list.append(offset + rows + 1)
                if z == rows - 2:
                    indices_list.append(primRestart)

    indices_vec = np.array(indices_list, dtype=np.uint32)

    currFace = 1
    for i in range(0, indices_vec.size - 2):
        index0 = indices_vec[i]
        index1 = indices_vec[i + 1]
        index2 = indices_vec[i + 2]

        face = np.array([0, 0, 0], dtype=np.int32)
        if (index0 != primRestart) and (index1 != primRestart) and (index2 != primRestart):
            if currFace % 2 != 0:
                face[0] = indices_vec[i]
                face[1] = indices_vec[i + 1]
                face[2] = indices_vec[i + 2]
                currFace += 1
            else:
                face[0] = indices_vec[i]
                face[1] = indices_vec[i + 2]
                face[2] = indices_vec[i + 1]
                currFace += 1

            faces_list.append(face)

    faces = np.reshape(faces_list, newshape=(len(faces_list), 3))

    for i in range(0, faces.shape[0]):
        A = np.array([vertices_vec[faces[i, 0], 0], vertices_vec[faces[i, 0], 1], vertices_vec[faces[i, 0], 2]],
                     dtype=np.float32)
        B = np.array([vertices_vec[faces[i, 1], 0], vertices_vec[faces[i, 1], 1], vertices_vec[faces[i, 1], 2]],
                     dtype=np.float32)
        C = np.array([vertices_vec[faces[i, 2], 0], vertices_vec[faces[i, 2], 1], vertices_vec[faces[i, 2], 2]],
                     dtype=np.float32)

        edge1A = normalize(B - A)
        edge2A = normalize(C - A)

        face_normal = np.cross(edge1A, edge2A)

        normals_vec[faces[i, 0]] += face_normal
        normals_vec[faces[i, 1]] += face_normal
        normals_vec[faces[i, 2]] += face_normal

    for i in range(0, normals_vec.shape[0]):
        normals_vec[i] = normalize(normals_vec[i])

    vao = glGenVertexArrays(1)
    vbo_vertices = glGenBuffers(1)
    vbo_normals = glGenBuffers(1)
    if gen_textures:
        vbo_texcoords = glGenBuffers(1)
    vbo_indices = glGenBuffers(1)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices_vec), vertices_vec.flatten(), GL_STATIC_DRAW)  #
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, vbo_normals)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(normals_vec), normals_vec.flatten(), GL_STATIC_DRAW)  #
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo_indices)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(indices_vec), indices_vec.flatten(),
                 GL_STATIC_DRAW)

    if gen_textures:
        glBindBuffer(GL_ARRAY_BUFFER, vbo_texcoords)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(texcoords_vec), texcoords_vec.flatten(),
                     GL_STATIC_DRAW)  #
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(2)



    glEnable(GL_PRIMITIVE_RESTART)
    glPrimitiveRestartIndex(primRestart)

    # der_z_y = lambda x,y,z: z * math.cos(y)
    # der_y_z = lambda x,y,z: y * math.cos(z)
    # der_x_z = lambda x,y,z: x * math.cos(z)
    # der_z_x = lambda x,y,z: z * math.cos(x)
    # der_y_x = lambda x,y,z: y * math.cos(x)
    # der_x_y = lambda x,y,z: x * math.cos(y)
    # rot = lambda x,y,z: math.sqrt( (der_z_y(x,y,z) - der_y_z(x,y,z))**2 + (der_x_z(x,y,z) - der_z_x(x,y,z))**2 + (der_y_x(x,y,z) - der_x_y(x,y,z))**2 )
    #
    # # max and min of rot lengths
    # max_rot = 0
    # min_rot = 0
    # rott_lst = []
    # for i in vertices_list:
    #
    #     rott = rot(i[0], i[1], i[2])
    #     rott_lst.append(rott)


    glBindVertexArray(0)
    if gen_relief:
        return (vao, indices_vec.size, vector_lines,vector_line_indexes)
    else:
        return (vao, indices_vec.size)