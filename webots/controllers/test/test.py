from controller import Robot

robot=Robot()
timestep=64

m=robot.getDevice("base_motor")
m.setPosition(float('inf'))
m.setVelocity(1)

n=robot.getDevice("shoulder_motor")
n.setPosition(float('inf'))
n.setVelocity(1)

b=robot.getDevice("elbow_motor")
b.setPosition(float('inf'))
b.setVelocity(1)

c=robot.getDevice("forearm_motor")
c.setPosition(float('inf'))
c.setVelocity(1)

d=robot.getDevice("wrist_motor")
d.setPosition(float('inf'))
d.setVelocity(1)