import pybullet as p
import time
import math

p.connect(p.GUI)

plane = p.createCollisionShape(p.GEOM_PLANE)
p.createMultiBody(0, plane)

useMaximalCoordinates = True
sphereRadius = 0.25
#colBoxId = p.createCollisionShapeArray([p.GEOM_BOX, p.GEOM_SPHERE],radii=[sphereRadius+0.03,sphereRadius+0.03], halfExtents=[[sphereRadius,sphereRadius,sphereRadius],[sphereRadius,sphereRadius,sphereRadius]])
colBoxId = p.createCollisionShape(p.GEOM_BOX,
                                  halfExtents=[sphereRadius, sphereRadius, sphereRadius])

mass = 1
visualShapeId = -1

link_Masses = []
linkCollisionShapeIndices = []
linkVisualShapeIndices = []
linkPositions = []
linkOrientations = []
linkInertialFramePositions = []
linkInertialFrameOrientations = []
indices = []
jointTypes = []
axis = []

for i in range(36):
  link_Masses.append(1)
  linkCollisionShapeIndices.append(colBoxId)
  linkVisualShapeIndices.append(-1)
  linkPositions.append([0, sphereRadius * 2.0 + 0.01, 0])
  linkOrientations.append([0, 0, 0, 1])
  linkInertialFramePositions.append([0, 0, 0])
  linkInertialFrameOrientations.append([0, 0, 0, 1])
  indices.append(i)
  jointTypes.append(p.JOINT_REVOLUTE)
  axis.append([0, 0, 1])

basePosition = [0, 0, 1]
baseOrientation = [0, 0, 0, 1]
sphereUid = p.createMultiBody(mass,
                              colBoxId,
                              visualShapeId,
                              basePosition,
                              baseOrientation,
                              linkMasses=link_Masses,
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

p.setGravity(0, 0, -10)
p.setRealTimeSimulation(0)

print(p.getNumJoints(sphereUid))

dt = 1. / 240.
while (1):
  p.stepSimulation()
  time.sleep(dt)
