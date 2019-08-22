#!coding: utf-8
from __future__ import print_function, division

from OpenGL.GL import *
from OpenGL.GL import shaders
import ctypes
import pygame

from vecutils import * # téléchargez vecutils ici

NB_POSITION_AXES = 3
NB_COLOR_AXES = 3
NB_TEX_COORDS_AXES = 2

vertexShader = """
#version 330 core
layout (location = 0) in vec3 attrPosition;
layout (location = 1) in vec3 attrColor;

uniform mat4 matrix;

out vec3 vsColor;

void main()
{
    gl_Position = matrix * vec4(attrPosition, 1.0);
    vsColor = attrColor;
}      
"""

fragmentShader = """
#version 330 core
in vec3 vsColor;

out vec4 FragColor;
  
void main()
{
    FragColor = vec4(vsColor, 1.0);
}
"""

vertices1 = farray([
    # positions        # colors         # texture coords
     0.5,  0.5, 0.0,   1.0, 0.0, 0.0,   1.0, 1.0,   # top right
     0.5, -0.5, 0.0,   0.0, 1.0, 0.0,   1.0, 0.0,   # bottom right
    -0.5, -0.5, 0.0,   0.0, 0.0, 1.0,   0.0, 0.0,   # bottom left
    -0.5,  0.5, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0,   # top left 
])

indices1 = np.array([
    0, 1, 3, # first triangle
    1, 2, 3,  # second triangle
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
        glVertexAttribPointer(0, NB_POSITION_AXES, GL_FLOAT, GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0));
        glEnableVertexAttribArray(0);

    # - Color attribute
    attrColorIndex = glGetAttribLocation(shaderProgram, 'attrColor')
    if (attrColorIndex != -1):
        glVertexAttribPointer(1, NB_COLOR_AXES, GL_FLOAT, GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3* ctypes.sizeof(ctypes.c_float)));
        glEnableVertexAttribArray(1);

    # Unbind the VAO
    glBindVertexArray(0)
    
    # Unbind the VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    if (attrPositionIndex != -1):
        glDisableVertexAttribArray(attrPositionIndex)
    if (attrColorIndex != -1):
        glDisableVertexAttribArray(attrColorIndex)

    return VAO

def prepareDisplay():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

def drawObject(shaderProgram, vertices, VAO, time):
    glUseProgram(shaderProgram)

    # Matrix
    matrix = ScaleMatrix(1/4)
    attrMatrixIndex = glGetUniformLocation(shaderProgram, 'matrix')
    glUniformMatrix4fv(attrMatrixIndex, 1, True, matrix)

    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, ctypes.c_void_p(0))

def display():
    glBindVertexArray(0)
    glUseProgram(0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600), pygame.OPENGL|pygame.DOUBLEBUF)

    shaderProgram = shaders.compileProgram(
        shaders.compileShader(vertexShader, GL_VERTEX_SHADER),
        shaders.compileShader(fragmentShader, GL_FRAGMENT_SHADER))
    
    VAO = createObject(shaderProgram, vertices1, indices1)
    
    clock = pygame.time.Clock()
    
    done = False
    tick = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        tick += 1
        prepareDisplay()
        drawObject(shaderProgram, vertices1, VAO, tick/60)
        display()
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
