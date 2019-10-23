#!coding: utf-8

from OpenGL.GL import *
from OpenGL.GL import shaders
from vecutils import *
import ctypes
import pygame
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
        self.vertices = material.vertices

    def declareVAO(self, shaderProgram):

        self.vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        # Bind the Vertex Buffer
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(self.vertices), self.vertices, GL_STATIC_DRAW);

        # Configure vertex attributes

        # - Position attribute
        attrPositionIndex = glGetAttribLocation(shaderProgram, 'attrPosition')
        if (attrPositionIndex != -1):
            glVertexAttribPointer(0, NB_POSITION_AXES, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0));
            glEnableVertexAttribArray(0);



def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 420), pygame.OPENGL|pygame.DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)

    shaderProgram = shaders.compileProgram(
        shaders.compileShader(vertexShader, GL_VERTEX_SHADER),
        shaders.compileShader(fragmentShader, GL_FRAGMENT_SHADER))

    box = pywavefront.Wavefront('data/box-T2F_N3F_V3F.obj')
    boxVisualizer = new WavefrontVisualiser(box)

    boxVisualizer.declareVAO(shaderProgram)

material = scene.materials['Material']
print(material.vertex_format)

for name, material in scene.materials.items():
    print(material.vertex_format)
    
    material.vertices
    # Material properties
    material.diffuse
    material.ambient
    material.texture

    
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