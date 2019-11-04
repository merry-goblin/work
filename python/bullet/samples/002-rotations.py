#!coding: utf-8

from OpenGL.GL import *
from OpenGL.GL import shaders
from vecutils import *
import ctypes
import pygame
import numpy as np
import pywavefront
import pybullet as p

vertexShader = """
#version 300 es
precision mediump float;

layout (location = 0) in vec3 attrPosition;
layout (location = 1) in vec3 attrNormal;
layout (location = 2) in vec2 attrTexCoords;

uniform mat4 matrix;

out vec3 vsColor;
out vec3 vsNormal;
out vec2 vsTexCoords;

void main()
{
    gl_Position = matrix * vec4(attrPosition, 1.0);
    vsColor = vec3(1.0, 0.5, 0.0);
    vsNormal = attrNormal;
    vsTexCoords = attrTexCoords;
}      
"""

fragmentShader = """
#version 300 es
precision mediump float;

in vec3 vsColor;
in vec3 vsNormal;
in vec2 vsTexCoords;

uniform sampler2D uTexture;

out vec4 FragColor;
  
void main()
{
    FragColor = texture(uTexture, vsTexCoords);
}
"""

class WavefrontVisualiser:

    def __init__(self, obj, pos, orn=None):
        material = obj.materials['Material']
        self.vertex_format = material.vertex_format
        self.vertices = farray(material.vertices)
        self.texture = material.texture
        self.uTexture = None
        self.pos = pos
        self.orn = orn

        if self.vertex_format == "T2F_N3F_V3F":
            self.initT2F_N3F_V3F()
        elif self.vertex_format == "T2F_V3F":
            self.initT2F_V3F()

    def initT2F_N3F_V3F(self):
        self.hasNormals = True
        self.hasTextures = True
        self.hasColors = False

        self.rowSize = 8
        self.positionSize = 3
        self.positionStart = 5
        self.normalSize = 3
        self.normalStart = 2
        self.textureSize = 3
        self.textureStart = 0
        
    def initT2F_V3F(self):
        self.hasNormals = False
        self.hasTextures = True
        self.hasColors = False

        self.rowSize = 5
        self.positionSize = 3
        self.positionStart = 2
        self.textureSize = 3
        self.textureStart = 0
        

    def updatePosAndOrn(self, pos, orn):
        self.pos = pos
        self.orn = orn

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
            glVertexAttribPointer(attrPositionIndex, self.positionSize, GL_FLOAT, GL_FALSE, self.rowSize * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(self.positionStart * ctypes.sizeof(ctypes.c_float)))
            glEnableVertexAttribArray(attrPositionIndex)

        # - Texture attribute
        if (self.hasTextures):
            attrTexCoordIndex = glGetAttribLocation(shaderProgram, 'attrTexCoords')
            if (attrTexCoordIndex != -1):
                glVertexAttribPointer(attrTexCoordIndex, self.textureSize, GL_FLOAT, GL_FALSE, self.rowSize * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(self.textureStart * ctypes.sizeof(ctypes.c_float)))
                glEnableVertexAttribArray(attrTexCoordIndex)

        self.uTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.uTexture)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # Set texture wrapping to GL_REPEAT (default wrapping method)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = pygame.image.load(self.texture.path).convert_alpha()
        imageData = pygame.image.tostring(image, 'RGBA', 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)
        glGenerateMipmap(GL_TEXTURE_2D)

        # Unbind the VAO
        glBindVertexArray(0)
        
        # Unbind attribute buffer
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        if (attrPositionIndex != -1):
            glDisableVertexAttribArray(attrPositionIndex)
        if (attrTexCoordIndex != -1):
            glDisableVertexAttribArray(attrTexCoordIndex)

    def draw(self, shaderProgram, time):

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.uTexture)

        glUseProgram(shaderProgram)

        pMatrix = PerspectiveMatrix(45, 1.0 * 800/600, 0.1, 100)

        lMatrix = LookAtMatrix(vec3(-10.0, 10.0, 10.0), (0, 0, 2), (0, 0, 1))

        xOrn = 0
        yOrn = 0
        zOrn = 0
        if self.orn is not None:
            orn = p.getEulerFromQuaternion(self.orn)
            xOrn = degrees(orn[0])
            yOrn = degrees(orn[1])
            zOrn = degrees(orn[2])

        #orn = p.getEulerFromQuaternion(self.orn)
        #orn = p.getEulerFromQuaternion(self.orn)
        #xOrn = degrees(orn[0])
    
        # Matrix
        #objectMatrix = TranslationMatrix(sin(time), 0, 0) @ RotationMatrix(sin(time)*90, (1,1,1))
        objectMatrix = TranslationMatrix(self.pos) @ RotationMatrix(yOrn, (0,1,0)) @ RotationMatrix(zOrn, (0,0,1)) @ RotationMatrix(xOrn, (1,0,0)) #@ p.getMatrixFromQuaternion(self.orn)
        attrMatrixIndex = glGetUniformLocation(shaderProgram, 'matrix')
        glUniformMatrix4fv(attrMatrixIndex, 1, True, pMatrix @ lMatrix @ objectMatrix)

        glBindVertexArray(self.vao)
        #glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices)//3)

def startDisplay():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def endDisplay():
    glBindVertexArray(0)
    glUseProgram(0)

def initPyBullet():
    p.connect(p.DIRECT)

    p.setPhysicsEngineParameter(numSolverIterations=10)
    p.setTimeStep(1. / 60.)
    p.setGravity(0, 0, -9.81)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 420), pygame.OPENGL|pygame.DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)

    shaderProgram = shaders.compileProgram(
        shaders.compileShader(vertexShader, GL_VERTEX_SHADER),
        shaders.compileShader(fragmentShader, GL_FRAGMENT_SHADER))

    boxPos = [0.0, 0.0, 18.0]
    boxOrn = p.getQuaternionFromEuler([0.5,0.2,1.25])
    planePos = [0.0, 0.0, 0.0]
    planeOrn = None
    box = pywavefront.Wavefront('data/box-T2F_N3F_V3F.obj')
    boxVisualizer = WavefrontVisualiser(box, boxPos, boxOrn)
    plane = pywavefront.Wavefront('data/plane.obj')
    planeVisualizer = WavefrontVisualiser(plane, planePos, planeOrn)

    boxVisualizer.prepare(shaderProgram)
    planeVisualizer.prepare(shaderProgram)

    initPyBullet()

    planeId = p.loadURDF("data/plane.urdf")

    shift     = [0.0, 0.0, 0.0]
    meshScale = [1.0, 1.0, 1.0]
    collisionBoxId = p.createCollisionShape(shapeType=p.GEOM_MESH,
                                              fileName="data/box-T2F_N3F_V3F.obj",
                                              collisionFramePosition=shift,
                                              meshScale=meshScale)
    boxId = p.createMultiBody(baseMass=1,
                               baseInertialFramePosition=[0, 0, 0],
                               baseCollisionShapeIndex=collisionBoxId,
                               basePosition=boxPos,
                               baseOrientation=boxOrn,
                               useMaximalCoordinates=True)
    collisionPlaneId = p.createCollisionShape(shapeType=p.GEOM_MESH,
                                              fileName="data/plane.obj",
                                              collisionFramePosition=shift,
                                              meshScale=meshScale)
    planeId = p.createMultiBody(baseMass=1,
                               baseInertialFramePosition=[0, 0, 0],
                               baseCollisionShapeIndex=collisionPlaneId,
                               basePosition=planePos,
                               useMaximalCoordinates=True)

    boxPos, boxOrn = p.getBasePositionAndOrientation(boxId)

    clock = pygame.time.Clock()
    done  = False
    tick  = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        tick += 1

        p.stepSimulation()
        boxPos, boxOrn = p.getBasePositionAndOrientation(boxId)
        boxVisualizer.updatePosAndOrn(boxPos, boxOrn)
        startDisplay()
        boxVisualizer.draw(shaderProgram, tick/60)
        planeVisualizer.draw(shaderProgram, tick/60)
        endDisplay()
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()