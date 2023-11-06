import ikpy
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from ikpy.utils import geometry
from controller import Robot



robot=Robot()


# Load your URDF file
urdf_path = 'arm1.urdf'
my_chain = Chain.from_urdf_file(urdf_path)
print(my_chain.links)

part_names = ("base_motor", "shoulder_motor", "elbow_motor", "forearm_motor", "wrist_motor")

for link_id in range(len(my_chain.links)):

    # This is the actual link object
    link = my_chain.links[link_id]
    

    if link.name not in part_names:
        print("Disabling {}".format(link.name))
        my_chain.active_links_mask[link_id] = False
        
motors = []
for part in part_names:

    motor = robot.getDevice(part)
    # Make sure to account for any motors that
    # require a different maximum velocity!
    motor.setVelocity(1)
        
    # position_sensor = motor.getPositionSensor()
    # position_sensor.enable(timestep)
    motors.append(motor)
        
        
print(motors)
initial_position = [0,0,0,0] + [m.getPositionSensor().getValue() for m in motors] + [0,0,0,0]

target = [1,1,1,1]
ikResults = my_chain.inverse_kinematics(target, initial_position=initial_position,  target_orientation = [0,0,1], orientation_mode="Y")

for res in range(len(ikResults)):
    # This if check will ignore anything that isn't controllable
    if my_chain.links[res].name in part_names:
        robot.getDevice(my_chain.links[res].name).setPosition(ikResults[res])
        print("Setting {} to {}".format(my_chain.links[res].name, ikResults[res]))
