#!coding: utf-8
from __future__ import print_function, division

from OpenGL.GL import *
from OpenGL.GL import shaders
import ctypes
import pygame

import numpy

from vecutils import * # téléchargez vecutils ici

NB_AXES_PER_VERTICE = 4

vertexShader = """
#version 330
in vec4 position;
in vec2 myTexCoord;
out vec2 texCoord;
void main()
{
    texCoord = myTexCoord;
    gl_Position = position;
}   
"""

fragmentShader = """
#version 330
uniform sampler2D vaisseau;
in vec2 texCoord;
out vec4 pixel;
void main()
{
    pixel = vec4(texture(vaisseau, texCoord).rgb, 1);
}
"""

vertices1 = farray([
    0.6, 0.6, 0.0, 1.0,
    -0.6, 0.6, 0.0, 1.0,
    -0.6, -0.6, 0.0, 1.0,
])

texCoords1 = farray([
    1, 1,
    0, 1,
    0, 0,
])

def createObject(shaderProgram, vertices, texCoords):

    # Create a new VAO (Vertex Array Object) 
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    TBO = glGenBuffers(1)

    # Bind the Vertex Array Object first
    glBindVertexArray(VAO);

    # Bind the Vertex Buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW);

    # Configure vertex attribute

    # - Position attribute
    position = glGetAttribLocation(shaderProgram, 'position')
    glVertexAttribPointer(position, NB_AXES_PER_VERTICE, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0));
    glEnableVertexAttribArray(position);

    # Bind the Texture Buffer
    glBindBuffer(GL_ARRAY_BUFFER, TBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(texCoords), texCoords, GL_STATIC_DRAW);

    # Configure texture attribute

    # - Texture attribute
    myTexCoords = glGetAttribLocation(shaderProgram, 'myTexCoord')
    glVertexAttribPointer(myTexCoords, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0));
    glEnableVertexAttribArray(myTexCoords);

    # Texture
    image = pygame.image.load('images/wall.jpg').convert_alpha()
    imageData = pygame.image.tostring(image, 'RGBA', 1)
    
    vaisseauTex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, vaisseauTex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBindTexture(GL_TEXTURE_2D, 0)

    # Unbind the VAO
    glBindVertexArray(0)
    
    # Unbind the VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glDisableVertexAttribArray(position)
    
    return VAO, vaisseauTex

def initDisplay():
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glEnable(GL_DEPTH_TEST)

def prepareDisplay():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def drawObject(shaderProgram, VAO, texture):
    glUseProgram(shaderProgram)

    glBindVertexArray(VAO)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)
    locVaisseau = glGetUniformLocation(shaderProgram, 'vaisseau')
    glUniform1i(locVaisseau, 0)
    glDrawArrays(GL_TRIANGLES, 0, 3)

def display():
    glBindVertexArray(0)
    glUseProgram(0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.OPENGL|pygame.DOUBLEBUF)

    initDisplay()

    shaderProgram = shaders.compileProgram(
        shaders.compileShader(vertexShader, GL_VERTEX_SHADER),
        shaders.compileShader(fragmentShader, GL_FRAGMENT_SHADER))
    
    VAO, texture = createObject(shaderProgram, vertices1, texCoords1)

    clock = pygame.time.Clock()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        prepareDisplay()
        drawObject(shaderProgram, VAO, texture)
        display()
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
