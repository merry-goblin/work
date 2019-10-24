#!coding: utf-8

from OpenGL.GL import *
from OpenGL.GL import shaders
from vecutils import *
import ctypes
import pygame
import numpy as np
import pywavefront


vertexShader = """
#version 300 es

precision mediump float;
layout (location = 0) in vec3 attrPosition;
layout (location = 1) in vec3 attrColor;
uniform mat4 matrix;
out vec3 vsColor;
void main()
{
    gl_Position = matrix * vec4(attrPosition, 1.0);
    vsColor = vec3(1.0, 0.5, 0.0);
}      
"""

fragmentShader = """
#version 300 es

precision mediump float;
in vec3 vsColor;
out vec4 FragColor;
  
void main()
{
    FragColor = vec4(vsColor, 1.0);
}
"""

class WavefrontVisualiser:

    def __init__(self, obj):
        material = obj.materials['Material']
        self.vertices = farray(material.vertices)

    def prepare(self, shaderProgram):

        self.vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        # Bind the Vertex Buffer
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(self.vertices), self.vertices, GL_STATIC_DRAW)

        # Configure vertex attributes

        # - Position attribute
        attrPositionIndex = glGetAttribLocation(shaderProgram, 'attrPosition')
        if (attrPositionIndex != -1):
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(5 * ctypes.sizeof(ctypes.c_float)))
            glEnableVertexAttribArray(0);

        # Unbind the VAO
        glBindVertexArray(0)
    
        # Unbind the VBO
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self, shaderProgram, time):

        glUseProgram(shaderProgram)

        pMatrix = PerspectiveMatrix(45, 1.0 * 800/600, 0.1, 100)

        lMatrix = LookAtMatrix(vec3(-5.0, 0.0, 3.0), (0, 0, 0), (0, 0, 1))

        # Matrix
        objectMatrix = TranslationMatrix(sin(time), 0, 0) @ RotationMatrix(sin(time)*90, (1,1,1))
        attrMatrixIndex = glGetUniformLocation(shaderProgram, 'matrix')
        glUniformMatrix4fv(attrMatrixIndex, 1, True, pMatrix @ lMatrix @ objectMatrix)

        glBindVertexArray(self.vao)
        #glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices)//3)


def prepareDisplay():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def display():
    glBindVertexArray(0)
    glUseProgram(0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 420), pygame.OPENGL|pygame.DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)

    shaderProgram = shaders.compileProgram(
        shaders.compileShader(vertexShader, GL_VERTEX_SHADER),
        shaders.compileShader(fragmentShader, GL_FRAGMENT_SHADER))

    box = pywavefront.Wavefront('data/box-T2F_N3F_V3F.obj')
    boxVisualizer = WavefrontVisualiser(box)

    boxVisualizer.prepare(shaderProgram)

    clock = pygame.time.Clock()
    
    done = False
    tick = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        tick += 1
        prepareDisplay()
        boxVisualizer.draw(shaderProgram, tick/60)
        display()
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()