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
    p.setTimeStep(1. / 240.)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 420), pygame.OPENGL|pygame.DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)

    shaderProgram = shaders.compileProgram(
        shaders.compileShader(vertexShader, GL_VERTEX_SHADER),
        shaders.compileShader(fragmentShader, GL_FRAGMENT_SHADER))

    boxPos = [0.0, 0.0, 18.0]
    boxOrn = p.getQuaternionFromEuler([0.5,0.2,1.25])
    boxPos2 = [0.0, 0.0, 4.0]
    boxOrn2 = p.getQuaternionFromEuler([0.0,0.0,0])
    planePos = [0.0, 0.0, 0.0]
    planeOrn = p.getQuaternionFromEuler([0.0,0.0,0.0])
    box = pywavefront.Wavefront('data/box-T2F_N3F_V3F.obj')
    boxVisualizer = WavefrontVisualiser(box, boxPos, boxOrn)
    box2 = pywavefront.Wavefront('data/box-T2F_N3F_V3F.obj')
    box2Visualizer = WavefrontVisualiser(box2, boxPos2, boxOrn2)
    plane = pywavefront.Wavefront('data/plane.obj')
    planeVisualizer = WavefrontVisualiser(plane, planePos, planeOrn)

    boxVisualizer.prepare(shaderProgram)
    box2Visualizer.prepare(shaderProgram)
    planeVisualizer.prepare(shaderProgram)

    shift        = [0.0, 0.0, 0.0]
    meshScale    = [1.0, 1.0, 1.0]
    sphereRadius = 1

    initPyBullet()

    # Plane
    collisionPlaneId = p.createCollisionShape(shapeType=p.GEOM_MESH,
                                              fileName="data/plane.obj",
                                              collisionFramePosition=shift,
                                              meshScale=meshScale)

    planeId = p.createMultiBody(baseMass=0,
                               baseInertialFramePosition=[0, 0, 0],
                               baseCollisionShapeIndex=collisionPlaneId,
                               basePosition=planePos,
                               baseOrientation=planeOrn,
                               useMaximalCoordinates=True)

    # Box 1

    collisionBoxId = p.createCollisionShape(shapeType=p.GEOM_MESH,
                                              fileName="data/box-T2F_N3F_V3F.obj",
                                              collisionFramePosition=shift,
                                              meshScale=meshScale)

    collisionBox2Id = p.createCollisionShape(p.GEOM_BOX, 
                                             halfExtents=[sphereRadius, sphereRadius, sphereRadius])
    """
    linkMasses = []
    linkCollisionShapeIndices = []
    linkVisualShapeIndices = []
    linkPositions = []
    linkOrientations = []
    linkInertialFramePositions = []
    linkInertialFrameOrientations = []
    indices = []
    jointTypes = []
    axis = []

    linkMasses.append(1)
    linkCollisionShapeIndices.append(collisionBoxId)
    linkVisualShapeIndices.append(-1)
    linkPositions.append([0, 1 + 0.01, 0])
    linkOrientations.append([0, 0, 0, 1])
    linkInertialFramePositions.append([0, 0, 0])
    linkInertialFrameOrientations.append([0, 0, 0, 1])
    indices.append(1)
    jointTypes.append(p.JOINT_REVOLUTE)
    axis.append([0, 0, 1])
    """
    useMaximalCoordinates = True
    mass = 1
    visualShapeId = -1
    linkMasses = []
    linkCollisionShapeIndices = []
    linkVisualShapeIndices = []
    linkPositions = []
    linkOrientations = []
    linkInertialFramePositions = []
    linkInertialFrameOrientations = []
    indices = []
    jointTypes = []
    axis = []

    for i in range(6):
      linkMasses.append(1)
      linkCollisionShapeIndices.append(collisionBox2Id)
      linkVisualShapeIndices.append(-1)
      linkPositions.append([0, 3, 0])
      linkOrientations.append([0, 0, 0, 1])
      linkInertialFramePositions.append([0, 0, 0])
      linkInertialFrameOrientations.append([0, 0, 0, 1])
      indices.append(i)
      jointTypes.append(p.JOINT_REVOLUTE)
      axis.append([0, 0, 1])

    boxId = p.createMultiBody(mass,
                              collisionBox2Id,
                              visualShapeId,
                              boxPos,
                              boxOrn,
                              linkMasses=linkMasses,
                              linkCollisionShapeIndices=linkCollisionShapeIndices,
                              linkVisualShapeIndices=linkVisualShapeIndices,
                              linkPositions=linkPositions,
                              linkOrientations=linkOrientations,
                              linkInertialFramePositions=linkInertialFramePositions,
                              linkInertialFrameOrientations=linkInertialFrameOrientations,
                              linkParentIndices=indices,
                              linkJointTypes=jointTypes,
                              linkJointAxis=axis,
                              useMaximalCoordinates=useMaximalCoordinates)

    """
    linkMasses = [1]
    linkCollisionShapeIndices = [collisionBox2Id]
    linkVisualShapeIndices = [-1]
    linkPositions = [[0, 2, 0]]
    linkOrientations = [[0, 0, 0, 1]]
    linkInertialFramePositions = [[0, 0, 0]]
    linkInertialFrameOrientations = [[0, 0, 0, 1]]
    indices = [1]
    jointTypes = [p.JOINT_REVOLUTE]
    axis = [[0, 0, 1]]
    

    boxId = p.createMultiBody(baseMass=1,
                              baseCollisionShapeIndex=collisionBoxId,
                              basePosition=boxPos,
                              baseOrientation=boxOrn,
                              linkMasses=linkMasses,
                              linkCollisionShapeIndices=linkCollisionShapeIndices,
                              linkVisualShapeIndices=linkVisualShapeIndices,
                              linkPositions=linkPositions,
                              linkOrientations=linkOrientations,
                              linkInertialFramePositions=linkInertialFramePositions,
                              linkInertialFrameOrientations=linkInertialFrameOrientations,
                              linkParentIndices=indices,
                              linkJointTypes=jointTypes,
                              linkJointAxis=axis,
                              useMaximalCoordinates=True)
    """

    p.setGravity(0, 0, -9.81)
    p.setRealTimeSimulation(0)

    print(p.getNumJoints(boxId))

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
        boxVisualizer.updatePosAndOrn(boxPos, boxOrn)
        #boxPos2, boxOrn2 = p.getBasePositionAndOrientation(box2Id)
        #box2Visualizer.updatePosAndOrn(boxPos2, boxOrn2)
        planePos, planeOrn = p.getBasePositionAndOrientation(planeId)
        planeVisualizer.updatePosAndOrn(planePos, planeOrn)

        startDisplay()
        boxVisualizer.draw(shaderProgram, tick/60)
        #box2Visualizer.draw(shaderProgram, tick/60)
        planeVisualizer.draw(shaderProgram, tick/60)
        endDisplay()
        pygame.display.flip()
        clock.tick(240)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()