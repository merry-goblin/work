#!coding: utf-8

from OpenGL.GL import *
from OpenGL.GL import shaders
from vecutils import *
import ctypes
import pygame
import numpy as np
import pywavefront
import pybullet as p
from pyengine import WavefrontVisualiser


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
    applyForce = False
    force = (0,0,100)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    applyForce = True
        tick += 1

        p.stepSimulation()

        if (applyForce) :
            applyForce = False
            forcePos = [0.0, 0.0, 0.0]
            p.applyExternalForce(objectUniqueId=boxId, 
                                 linkIndex=-1,
                                 forceObj=force, 
                                 posObj=forcePos,
                                 flags=p.LINK_FRAME)

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