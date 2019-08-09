#!coding: utf-8
from __future__ import print_function, division

from OpenGL.GL import *
from OpenGL.GL import shaders
import ctypes
import pygame

from vecutils import * # téléchargez vecutils ici

NB_AXES_PER_VERTICE = 4

vertex_shader = """
#version 330
layout (location = 0) in vec4 position;

out vec4 vertexColor;

float calc(float coord)
{
    return (coord+1) * 0.5;
}

void main()
{
    gl_Position = position;
    //vertexColor = vec4(0.5, 0.0, 0.0, 1.0);
    vertexColor = vec4(calc(gl_Position.x), calc(gl_Position.y), calc(gl_Position.z), calc(gl_Position.w));//vec4(0.5, 0.0, 0.0, 1.0);
}
"""

fragment_shader = """
#version 330

in vec4 vertexColor;
out vec4 FragColor;

void main()
{
    FragColor = vertexColor;
}
"""

vertices1 = farray([
    -0.9, -0.75, 0, 1.0,
    0.0, 0.75, 0, 1.0,
    0.9, -0.75, 0, 1.0,
])

def create_object(shader_program, vertices):
    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)
    
    # Get the position of the 'position' in parameter of our shader_program and bind it.
    position = glGetAttribLocation(shader_program, 'position')
    
    if position != -1: # maybe the attribute is useless and was discarded by the compiler
        glEnableVertexAttribArray(position)
        
        # Generate buffers to hold our vertices
        vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        
        # Describe the position data layout in the buffer
        glVertexAttribPointer(position, NB_AXES_PER_VERTICE, GL_FLOAT, False, 0, ctypes.c_void_p(0))
    
        # Send the data over to the buffer
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)
    else:
        print('Inactive attribute "{}"'.format('position'))
    
    # Unbind the VAO
    glBindVertexArray(0)
    
    # Unbind the VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    return vertex_array_object

def prepareDisplay():
    glClear(GL_COLOR_BUFFER_BIT)

def drawObject(shader_program, vertices, vertex_array_object):
    glUseProgram(shader_program)
    
    glBindVertexArray(vertex_array_object)
    glDrawArrays(GL_TRIANGLES, 0, len(vertices)//NB_AXES_PER_VERTICE)

def display():
    glBindVertexArray(0)
    glUseProgram(0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((512, 512), pygame.OPENGL|pygame.DOUBLEBUF)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    shader_program = shaders.compileProgram(
        shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))
    
    vertex_array_object1 = create_object(shader_program, vertices1)
    
    clock = pygame.time.Clock()
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        prepareDisplay()
        drawObject(shader_program, vertices1, vertex_array_object1)
        display()
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()

