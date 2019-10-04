#!coding: utf-8
from __future__ import print_function, division

from OpenGL.GL import *
from OpenGL.GL import shaders
import ctypes
import pygame
import numpy as np
from math import sin, cos, degrees, radians, tan

from vecutils import * # téléchargez vecutils ici

NB_POSITION_AXES = 3
NB_COLOR_AXES = 3
NB_TEX_COORDS_AXES = 2

vertexShader = """
#version 300 es
precision mediump float;

layout (location = 0) in vec3 attrPosition;
layout (location = 1) in vec3 attrColor;
layout (location = 2) in vec2 attrTexCoords;

uniform mat4 matrix;

out vec3 vsColor;
out vec2 vsTexCoords;

void main()
{
    gl_Position = matrix * vec4(attrPosition, 1.0);
    vsColor = attrColor;
    vsTexCoords = attrTexCoords;
}      
"""

fragmentShader = """
#version 300 es
precision mediump float;

in vec3 vsColor;
in vec2 vsTexCoords;

uniform sampler2D texture1;

out vec4 FragColor;

void main()
{
    FragColor = texture(texture1, vsTexCoords);
}
"""

vertices1 = farray([
    # positions        # colors         # texture coords
    -1.0, -1.0,  1.0,   1.0, 0.0, 0.0,    1.0, 0.0,
     1.0, -1.0,  1.0,   0.0, 1.0, 0.0,    0.0, 0.0,
     1.0,  1.0,  1.0,   0.0, 0.0, 1.0,    0.0, 1.0,
    -1.0,  1.0,  1.0,   1.0, 1.0, 0.0,    1.0, 1.0,
    -1.0, -1.0, -1.0,   1.0, 1.0, 0.0,    1.0, 0.0,
     1.0, -1.0, -1.0,   0.0, 0.0, 1.0,    0.0, 0.0,
     1.0,  1.0, -1.0,   0.0, 1.0, 0.0,    0.0, 1.0,
    -1.0,  1.0, -1.0,   1.0, 0.0, 0.0,    1.0, 1.0, 
])

indices1 = np.array([
    0, 1, 3,
    1, 2, 3,
    4, 5, 7,
    5, 6, 7,
    3, 2, 7,
    2, 6, 7,
    0, 1, 4,
    1, 5, 4,
    1, 5, 2,
    5, 6, 2,
    0, 4, 3,
    4, 7, 3,
], dtype=np.uint32)

def createObject(shaderProgram, vertices, indices):

    # Create a new VAO (Vertex Array Object)
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    # Bind the Vertex Array Object first
    glBindVertexArray(VAO);

    # Bind the Vertex Buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW);

    # Bind the Entity Buffer
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(indices), indices, GL_STATIC_DRAW)

    # Configure vertex attributes

    # - Position attribute
    attrPositionIndex = glGetAttribLocation(shaderProgram, 'attrPosition')
    if (attrPositionIndex != -1):
        glVertexAttribPointer(attrPositionIndex, NB_POSITION_AXES, GL_FLOAT, GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0));
        glEnableVertexAttribArray(attrPositionIndex);

    # - Color attribute
    attrColorIndex = glGetAttribLocation(shaderProgram, 'attrColor')
    if (attrColorIndex != -1):
        glVertexAttribPointer(attrColorIndex, NB_COLOR_AXES, GL_FLOAT, GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3* ctypes.sizeof(ctypes.c_float)));
        glEnableVertexAttribArray(attrColorIndex);

    # - Texture coordinates attribute
    attrTexCoordsIndex = glGetAttribLocation(shaderProgram, 'attrTexCoords')
    if (attrTexCoordsIndex != -1):
        glVertexAttribPointer(attrTexCoordsIndex, NB_TEX_COORDS_AXES, GL_FLOAT, GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))
        glEnableVertexAttribArray(attrTexCoordsIndex)

    # Texture
    
    texture1 = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture1)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # Set texture wrapping to GL_REPEAT (default wrapping method)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = pygame.image.load('images/awesomeface.png').convert_alpha()
    imageData = pygame.image.tostring(image, 'RGBA', 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)
    glGenerateMipmap(GL_TEXTURE_2D)

    # Unbind the VAO
    glBindVertexArray(0)
    
    # Unbind the VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    if (attrPositionIndex != -1):
        glDisableVertexAttribArray(attrPositionIndex)
    if (attrColorIndex != -1):
        glDisableVertexAttribArray(attrColorIndex)
    if (attrTexCoordsIndex != -1):
        glDisableVertexAttribArray(attrTexCoordsIndex)

    return VAO, texture1

def prepareDisplay():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def drawObject(shaderProgram, vertices, VAO, texture1, time):

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture1)

    glUseProgram(shaderProgram)

    pMatrix = PerspectiveMatrix(45, 1.0 * 800/600, 0.1, 100)

    lMatrix = LookAtMatrix(vec3(-5.0, 0.0, 3.0), (0, 0, 0), (0, 0, 1))

    # Matrix
    objectMatrix = TranslationMatrix(sin(time), 0, 0) @ RotationMatrix(sin(time)*90, (1,1,1))
    attrMatrixIndex = glGetUniformLocation(shaderProgram, 'matrix')
    glUniformMatrix4fv(attrMatrixIndex, 1, True, pMatrix @ lMatrix @ objectMatrix)

    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, ctypes.c_void_p(0))

def display():
    glBindVertexArray(0)
    glUseProgram(0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.OPENGL|pygame.DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)

    shaderProgram = shaders.compileProgram(
        shaders.compileShader(vertexShader, GL_VERTEX_SHADER),
        shaders.compileShader(fragmentShader, GL_FRAGMENT_SHADER))
    
    VAO, texture1 = createObject(shaderProgram, vertices1, indices1)
    
    clock = pygame.time.Clock()
    
    done = False
    tick = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        tick += 1
        prepareDisplay()
        drawObject(shaderProgram, vertices1, VAO, texture1, tick/60)
        display()
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
