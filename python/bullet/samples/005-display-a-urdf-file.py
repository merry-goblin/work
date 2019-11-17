#!coding: utf-8

from OpenGL.GL import *
from OpenGL.GL import shaders
from vecutils import *
import ctypes
import pygame
import numpy as np
import pybullet as p
from pyengine import *



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
    physicsClientId = p.connect(p.DIRECT)
    p.resetSimulation()
    #p.setPhysicsEngineParameter(numSolverIterations=10)
    p.setTimeStep(1. / 240.)
    p.setGravity(0, 0, -9.81)
    p.setRealTimeSimulation(0)

    return physicsClientId

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 420), pygame.OPENGL|pygame.DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)

    shaderProgram = shaders.compileProgram(
        shaders.compileShader(vertexShader, GL_VERTEX_SHADER),
        shaders.compileShader(fragmentShader, GL_FRAGMENT_SHADER))

    boxPos = [0.0, 0.0, 5.0]
    boxOrn = p.getQuaternionFromEuler([0.5,0.2,1.25])
    planePos = [0.0, 0.0, 0.0]
    planeOrn = p.getQuaternionFromEuler([0.0,0.0,0.0])

    physicsClientId = initPyBullet()
    planeId = p.loadURDF("data/plane.urdf")
    #r2d2 = p.loadURDF("data/r2d2/r2d2.urdf")

    objectManager = URDFManager(physicsClientId)
    boxId = objectManager.add("data/box.urdf", planePos, planeOrn)

    shapes = objectManager.getVisualShapes(boxId)
    for key, visualShape in shapes.items():
        visualShape.prepare(shaderProgram)


    """
    for i in range(p.getNumJoints(r2d2)):
        jointInfo = p.getJointInfo(r2d2, i)
        print("-------"+str(i)+"-------")
        print(jointInfo)
    """

    #GEOM_SPHERE, GEOM_BOX, GEOM_CAPSULE, GEOM_CYLINDER, GEOM_PLANE, GEOM_MESH

    """
    visualShapes = p.getVisualShapeData(r2d2)
    i = 0
    for vs in visualShapes:
        print("-------"+str(i)+"-------")
        print(vs)
        i += 1
    """

    clock = pygame.time.Clock()
    done  = False
    tick  = 0
    applyForce = False
    force = (0,0,5000)
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
        shapes = objectManager.getVisualShapes(boxId)
        for key, visualShape in shapes.items():
            visualShape.updatePosAndOrn(boxPos, boxOrn)
            visualShape.draw(shaderProgram)

        #boxVisualizer.updatePosAndOrn(boxPos, boxOrn)
        #boxPos2, boxOrn2 = p.getBasePositionAndOrientation(box2Id)
        #box2Visualizer.updatePosAndOrn(boxPos2, boxOrn2)
        #planePos, planeOrn = p.getBasePositionAndOrientation(planeId)
        #planeVisualizer.updatePosAndOrn(planePos, planeOrn)

        #startDisplay()
        #boxVisualizer.draw(shaderProgram, tick/60)
        #box2Visualizer.draw(shaderProgram, tick/60)
        #planeVisualizer.draw(shaderProgram, tick/60)
        #endDisplay()
        pygame.display.flip()
        clock.tick(240)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
