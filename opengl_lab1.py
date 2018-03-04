# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 12:11:48 2018

@author: vsan
"""

import glfw
import math
import numpy as np
from PIL import Image
from OpenGL.GL import (GL_ARRAY_BUFFER, GL_COLOR_BUFFER_BIT,
                       GL_FALSE, GL_FLOAT, GL_FRAGMENT_SHADER, GL_RENDERER, GL_SHADING_LANGUAGE_VERSION,
                       GL_UNSIGNED_INT,
                       GL_STATIC_DRAW, GL_TRIANGLES, GL_TRUE, GL_VENDOR, GL_VERSION, GL_ELEMENT_ARRAY_BUFFER,
                       GL_TEXTURE_BASE_LEVEL, GL_VERTEX_SHADER,
                       GL_DEPTH_TEST, GL_DEPTH_BUFFER_BIT, GL_FRONT_AND_BACK, GL_FILL, GL_LINE, GL_UNPACK_ALIGNMENT,
                       GL_TEXTURE_MAX_LEVEL,
                       GL_NO_ERROR, GL_INVALID_ENUM, GL_INVALID_VALUE, GL_INVALID_OPERATION, GL_STACK_OVERFLOW,
                       GL_TEXTURE_2D, GL_TEXTURE0, GL_TEXTURE1,
                       GL_STACK_UNDERFLOW, GL_OUT_OF_MEMORY, GL_TABLE_TOO_LARGE, GL_PRIMITIVE_RESTART,
                       GL_TRIANGLE_STRIP, GL_RGB, GL_UNSIGNED_BYTE,
                       glAttachShader, glBindBuffer, glBindVertexArray, glDrawElements,
                       glBufferData, glClear, glClearColor, glDrawArrays, glEnableVertexAttribArray,
                       glGenBuffers, glGenVertexArrays, glGetAttribLocation, glDeleteVertexArrays,
                       glGetString, glGetUniformLocation, glUseProgram, glDeleteBuffers,
                       glVertexAttribPointer, glViewport, glPolygonMode, glUniformMatrix4fv,glUniform3fv, glBindTexture,
                       glTexImage2D,
                       glEnable, glGetError, glPrimitiveRestartIndex, glDisable, glGenTextures, glPixelStorei,
                       glTexParameteri, glActiveTexture, glUniform1i)

from OpenGL.arrays import ArrayDatatype
from math import sin, sqrt

from shader_program import ShaderProgram
from camera import Camera
from light_math import (projectionMatrixTransposed, identityM4x4, translateM4x4, scaleM4x4,
                        rotateXM4x4, rotateYM4x4, rotateZM4x4, projectionMatrix, normalize)

width = 1024
height = 1024
lastX = float(width) / 2.0
lastY = float(height) / 2.0
filling = True
keys = np.zeros(1024)
firstMouse = True
captureMouse = True;
capturedMouseJustNow = False
camera = Camera(a_pos=np.array([0.0, 50.0, 50.0], dtype=np.float32))

from inspect import getframeinfo, stack


def check_gl_errors():
    caller = getframeinfo(stack()[1][0])
    gl_error = glGetError()

    if (gl_error == GL_NO_ERROR):
        return

    if (gl_error == GL_INVALID_ENUM):
        print("%s:%d - GL_INVALID_ENUM" % (caller.filename, caller.lineno))

    if (gl_error == GL_INVALID_VALUE):
        print("%s:%d - GL_INVALID_VALUE" % (caller.filename, caller.lineno))

    if (gl_error == GL_INVALID_OPERATION):
        print("%s:%d - GL_INVALID_OPERATION" % (caller.filename, caller.lineno))

    if (gl_error == GL_STACK_OVERFLOW):
        print("%s:%d - GL_STACK_OVERFLOW" % (caller.filename, caller.lineno))

    if (gl_error == GL_STACK_UNDERFLOW):
        print("%s:%d - GL_STACK_UNDERFLOW" % (caller.filename, caller.lineno))

    if (gl_error == GL_OUT_OF_MEMORY):
        print("%s:%d - GL_OUT_OF_MEMORY" % (caller.filename, caller.lineno))

    if (gl_error == GL_TABLE_TOO_LARGE):
        print("%s:%d - GL_TABLE_TOO_LARGE" % (caller.filename, caller.lineno))


def read_texture(filename):
    try:
        image = Image.open(filename)
    except IOError as ex:
        print('IOError: failed to open texture file %s' % filename)
        return -1
    print('opened file: size=', image.size, 'format=', image.format)
    imageData = np.array(list(image.getdata()), np.uint8)

    textureID = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, imageData)

    image.close()
    return textureID


def bindTexture(unit, textureID):
    glActiveTexture(GL_TEXTURE0 + unit)
    glBindTexture(GL_TEXTURE_2D, textureID)


def key_callback(window, key, scancode, action, mods):
    global keys
    global filling

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, 1)
    if key == glfw.KEY_SPACE and action == glfw.PRESS:

        if (filling):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            filling = False
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            filling = True
    else:
        if action == glfw.PRESS:
            keys[key] = 1
        elif action == glfw.RELEASE:
            keys[key] = 0


def mouseclick_callback(window, button, action, mods):
    global captureMouse
    global capturedMouseJustNow

    if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.RELEASE:
        captureMouse = not captureMouse

    if captureMouse:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        capturedMouseJustNow = True
    else:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)


def mousemove_callback(window, xpos, ypos):
    global firstMouse
    global lastX
    global lastY
    global camera

    if firstMouse:
        lastX = float(xpos)
        lastY = float(ypos)
        firstMouse = False

    xoffset = float(xpos) - lastX
    yoffset = lastY - float(ypos)

    lastX = float(xpos)
    lastY = float(ypos)

    if captureMouse:
        camera.process_mouse(xoffset, yoffset, True)


def doCameraMovement(camera=Camera(), delta_time=0.0):
    if (keys[glfw.KEY_W] == 1):
        camera.process_keyboard("forward", delta_time)
    if (keys[glfw.KEY_A] == 1):
        camera.process_keyboard("left", delta_time)
    if (keys[glfw.KEY_S] == 1):
        camera.process_keyboard("backward", delta_time)
    if (keys[glfw.KEY_D] == 1):
        camera.process_keyboard("right", delta_time)


def create_surface(rows, cols, size, fun, gen_textures):

    normals_vec = np.zeros((rows * cols, 3), dtype=np.float32)

    vertices_list = []
    texcoords_list = []
    faces_list = []
    indices_list = []

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

    if gen_textures:
        glBindBuffer(GL_ARRAY_BUFFER, vbo_texcoords)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(texcoords_vec), texcoords_vec.flatten(),
                     GL_STATIC_DRAW)  #
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(2)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo_indices)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(indices_vec), indices_vec.flatten(),
                 GL_STATIC_DRAW);

    glEnable(GL_PRIMITIVE_RESTART)
    glPrimitiveRestartIndex(primRestart)

    glBindVertexArray(0)

    return (vao, indices_vec.size)




def main():
    global width
    global height
    global camera

    width = 1024
    height = 1024

    delta_time = 0.0
    last_frame = 0.0

    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
    window = glfw.create_window(width, height, "opengl_lab1", None, None)

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mousemove_callback)
    glfw.set_mouse_button_callback(window, mouseclick_callback)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    fun1 = lambda x, z: math.sin(x+z)
    fun2 = lambda x, z: math.exp(-x*x - z*z)
    fun3 = lambda x, z: (x**2 + z**2) / (x*z)
    heightmap_dummy_fun = lambda x, z: 0.0

    surface_size = 50

    (fun_vao1, ind_fun1) = create_surface(100, 100, surface_size, fun1, False)
    (fun_vao2, ind_fun2) = create_surface(100, 100, surface_size, fun2, False)
    (fun_vao3, ind_fun3) = create_surface(100, 100, surface_size, fun3, False)
    (heightmap_vao, ind_hm) = create_surface(100,100, surface_size, heightmap_dummy_fun, True)

    fun_shader_sources = [(GL_VERTEX_SHADER, "shaders/functions.vert"), (GL_FRAGMENT_SHADER, "shaders/functions.frag")]

    fun_program = ShaderProgram(fun_shader_sources)

    hm_shader_sources = [(GL_VERTEX_SHADER, "shaders/heightmap.vert"), (GL_FRAGMENT_SHADER, "shaders/heightmap.frag")]
    # hm_shader_sources = [(GL_VERTEX_SHADER, "shaders/functions.vert"), (GL_FRAGMENT_SHADER, "shaders/functions.frag")]

    hm_program = ShaderProgram(hm_shader_sources)

    hm_texture = read_texture("1.jpg")

    check_gl_errors()

    projection = projectionMatrixTransposed(60.0, float(width) / float(height), 1, 1000.0)

    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame
        glfw.poll_events()

        doCameraMovement(camera, delta_time)

        model = translateM4x4(np.array([0.0, 0.0, 0.0]))
        view = camera.get_view_matrix()

        glClearColor(0.5, 0.5, 0.5, 1.0)
        glViewport(0, 0, width, height)
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        fun_program.bindProgram()

        glUniform3fv(fun_program.uniformLocation("col"), 1 , [1.0, 0, 0] )

        glUniformMatrix4fv(fun_program.uniformLocation("model"), 1, GL_FALSE, np.transpose(model).flatten())
        glUniformMatrix4fv(fun_program.uniformLocation("view"), 1, GL_FALSE, np.transpose(view).flatten())
        glUniformMatrix4fv(fun_program.uniformLocation("projection"), 1, GL_FALSE, projection.flatten())

        glBindVertexArray(fun_vao1)
        glDrawElements(GL_TRIANGLE_STRIP, ind_fun1, GL_UNSIGNED_INT, None)

        model = translateM4x4(np.array([-1.5*surface_size,0.0 ,0.0 ]))
        glUniform3fv(fun_program.uniformLocation("col"), 1, [0.0, 1.0, 0])
        glUniformMatrix4fv(fun_program.uniformLocation("model"), 1, GL_FALSE, np.transpose(model).flatten())
        glBindVertexArray(fun_vao2)
        glDrawElements(GL_TRIANGLE_STRIP, ind_fun2, GL_UNSIGNED_INT, None)

        model = translateM4x4(np.array([1.5 * surface_size, 0.0, 0.0]))
        glUniform3fv(fun_program.uniformLocation("col"), 1, [0.0, 0.0, 1.0])
        glUniformMatrix4fv(fun_program.uniformLocation("model"), 1, GL_FALSE, np.transpose(model).flatten())
        glBindVertexArray(fun_vao3)
        glDrawElements(GL_TRIANGLE_STRIP, ind_fun3, GL_UNSIGNED_INT, None)

        hm_program.bindProgram()

        model = translateM4x4(np.array([0.0, 0.0, -1.5 * surface_size]))

        bindTexture(0, hm_texture)

        glUniform1i(hm_program.uniformLocation("tex"), 0)
        glUniformMatrix4fv(hm_program.uniformLocation("model"), 1, GL_FALSE, np.transpose(model).flatten())
        glUniformMatrix4fv(hm_program.uniformLocation("view"), 1, GL_FALSE, np.transpose(view).flatten())
        glUniformMatrix4fv(hm_program.uniformLocation("projection"), 1, GL_FALSE, projection.flatten())
        glBindVertexArray(heightmap_vao)
        glDrawElements(GL_TRIANGLE_STRIP, ind_hm, GL_UNSIGNED_INT, None)

        hm_program.unbindProgram()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
