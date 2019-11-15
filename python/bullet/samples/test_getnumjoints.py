#!coding: utf-8

import pybullet as p

p.connect(p.GUI)

#p.resetSimulation()

plane = p.loadURDF("data/plane.urdf")
robot = p.loadURDF(fileName="data/r2d2bis/r2d2.urdf",basePosition=[0,0,0.5])

#position, orientation = p.getBasePositionAndOrientation(robot)
numJoints = p.getNumJoints(robot)
print("-----------------")
print(numJoints)

p.setGravity(0, 0, -9.81)   # everything should fall down
p.setRealTimeSimulation(True)  # we want to be faster than real time :)

while(True):
    p.stepSimulation()