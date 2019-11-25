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
    p.setTimeStep(1. / 60.)
    p.setGravity(0, 0, -9.81)
    p.setRealTimeSimulation(0)

    return physicsClientId

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 480), pygame.OPENGL|pygame.DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)

    shaderProgram = shaders.compileProgram(
        shaders.compileShader(vertexShader, GL_VERTEX_SHADER),
        shaders.compileShader(fragmentShader, GL_FRAGMENT_SHADER))

    boxPos = [0.0, 0.0, 5.0]
    boxOrn = p.getQuaternionFromEuler([0.0,0.0,0.0])
    planePos = [0.0, 0.0, 0.0]
    planeOrn = p.getQuaternionFromEuler([0.0,0.0,0.0])

    physicsClientId = initPyBullet()

    objectManager = URDFManager(physicsClientId)
    planeId = objectManager.add("data/plane.urdf", planePos, planeOrn)
    boxId = objectManager.add("data/006-box.urdf", boxPos, boxOrn)

    shapes = objectManager.getVisualShapes(planeId)
    for key, visualShape in shapes.items():
        visualShape.vs.prepare(shaderProgram)

    shapes = objectManager.getVisualShapes(boxId)
    for key, visualShape in shapes.items():
        visualShape.vs.prepare(shaderProgram)
    print("----------")
    print(p.getNumJoints(boxId))
    print(p.getJointInfo(boxId, 0))

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
    velocity = 0.0
    force = 0.0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    velocity = -100
                    force = 1000.0
                elif event.key == pygame.K_DOWN:
                    velocity = 100
                    force = 1000.0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    velocity = 0.0
                    force = 0.0

        p.setJointMotorControl2(bodyUniqueId=boxId, 
                           jointIndex=0,
                           controlMode=p.VELOCITY_CONTROL,
                           targetVelocity=velocity,
                           force=force)

        tick += 1

        startDisplay()

        shapes = objectManager.getVisualShapes(planeId)
        for key, visualShape in shapes.items():
            #visualShape.updatePosAndOrn(planePos, planeOrn)
            visualShape.vs.draw(shaderProgram)

        quatBoxPos, quatBoxOrn = p.getBasePositionAndOrientation(boxId)
        boxPos = TranslationMatrix(quatBoxPos)
        boxOrn = getOrnMatrixFromQuaternion(quatBoxOrn)
        shapes = objectManager.getVisualShapes(boxId)
        for key, visualShape in shapes.items():
            if (key != -1):
                linkState = p.getLinkState(boxId, key)
                quatLinkPos = linkState[0]
                quatLinkOrn = linkState[1]
                linkPos = TranslationMatrix(quatLinkPos)
                linkOrn = getOrnMatrixFromQuaternion(quatLinkOrn)
                #visualShapePos = linkOrn @ visualShape.pos
                #visualShapePos = TranslationMatrix(visualShapePos[0][3], visualShapePos[1][3], visualShapePos[2][3])
            else:
                linkPos = boxPos
                linkOrn = boxOrn
                #visualShapePos = visualShape.pos
            pos = linkPos #visualShapePos @ linkPos
            orn = visualShape.orn @ linkOrn
            visualShape.vs.updatePosAndOrn(pos, orn)
            visualShape.vs.draw(shaderProgram)

        endDisplay()

        p.stepSimulation()

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
