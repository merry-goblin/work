#!coding: utf-8
from __future__ import print_function, division

from OpenGL.GL import *
from OpenGL.GL import shaders
import ctypes
import pygame

from vecutils import * # téléchargez vecutils ici

NB_AXES_PER_VERTICE = 4

vertexShader = """
#version 330 core
layout (location = 0) in vec3 aPos;   // the position variable has attribute position 0
layout (location = 1) in vec3 aColor; // the color variable has attribute position 1

uniform mat4 matrix;

out vec3 ourColor; // output a color to the fragment shader

void main()
{
    gl_Position = matrix * vec4(aPos, 1.0);
    ourColor = aColor; // set ourColor to the input color we got from the vertex data
}      
"""

fragmentShader = """
#version 330 core
out vec4 FragColor;  
in vec3 ourColor;
  
void main()
{
    FragColor = vec4(ourColor, 1.0);
}
"""

vertices1 = farray([
     0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
    -0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
     0.0,  0.5, 0.0,  0.0, 0.0, 1.0
])

def createObject(shaderProgram, vertices):

    # Create a new VAO (Vertex Array Object) and bind it
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    # Bind the Vertex Array Object first
    glBindVertexArray(VAO);

    # Bind the Vertex Buffer(s)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW);

    # Configure vertex attributes(s)

    # - Position attribute
    #positionAttribute = glGetAttribLocation(shaderProgram, 'position')
    glVertexAttribPointer(0, NB_AXES_PER_VERTICE, GL_FLOAT, GL_FALSE, 6 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0));
    glEnableVertexAttribArray(0);

    # - Color attribute
    #colorAttribute = glGetAttribLocation(shader_program, 'color')
    glVertexAttribPointer(1, NB_AXES_PER_VERTICE, GL_FLOAT, GL_FALSE, 6 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3* ctypes.sizeof(ctypes.c_float)));
    glEnableVertexAttribArray(1);

    # Unbind the VAO
    glBindVertexArray(0)
    
    # Unbind the VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    return VAO

def prepareDisplay():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

def drawObject(shaderProgram, vertices, VAO, time):
    glUseProgram(shaderProgram)

    # set matrix
    m = TranslationMatrix((sin(time)*.5), 0, 0)
    loc_matrix = glGetUniformLocation(shaderProgram, 'matrix')
    glUniformMatrix4fv(loc_matrix, 1, True, m)

    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 3)

def display():
    glBindVertexArray(0)
    glUseProgram(0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.OPENGL|pygame.DOUBLEBUF)

    shaderProgram = shaders.compileProgram(
        shaders.compileShader(vertexShader, GL_VERTEX_SHADER),
        shaders.compileShader(fragmentShader, GL_FRAGMENT_SHADER))
    
    VAO = createObject(shaderProgram, vertices1)
    
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
