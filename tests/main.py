import sys
from pathlib import Path
import threading
import time

# Add the parent directory of the current script to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from agnostic_controller import (
    Dobot, 
    ElephantRobotics, Pro600, 
    UniversalRobotics, UR5, 
    Fanuc, 
    Vention,
    OnRobot
)

pos1_low = [0.6116023063659668, -0.8117355865291138, 0.8821848074542444, -1.6617809734740199, -1.581780258809225, 0.3699551522731781]
pos2_high = [0.8180813789367676, -1.0786418181708832, 1.1617329756366175, -1.6617847881712855, -1.581768814717428, 0.3699668049812317]

close_to_table = [1.5701996088027954, -1.2257346671870728, 2.109311882649557, -2.4544340572752894, -1.5712249914752405, 0.003511645831167698]

def move_vention(vention:Vention, pos):
    vention.move_joints(pos, speed=2_500, acceleration=500, move_type='abs')
    # vention.home()

def move_ur5(ur5:UR5,pos):
    ur5.move_joints(pos, t=3)
    # ur5.home()

def gripper():
    with OnRobot() as gripper:
        gripper.open()


def vention_ur5():
    with Vention("192.168.7.2") as vention, UR5("192.168.1.111") as ur5:
        pass

def ur5():
    with UR5("192.168.1.111") as ur5:
        # [36, -45, 47, -93, -91, 22] -? [....,0]
        angle = ur5.home()
        # time.sleep(10)
        
        # pos1_low = [0.6116023063659668, -0.8117355865291138, 0.8821848074542444, -1.6617809734740199, -1.581780258809225, 0.3699551522731781]
        # pos2_high = [0.8180813789367676, -1.0786418181708832, 1.1617329756366175, -1.6617847881712855, -1.581768814717428, 0.3699668049812317]
        # ur5.move_joints(pos1_low, time=3)
        # cart = ur5.get_cartesian_position()  # Uncomment to get cartesian position
        # print(cart)




def mycobot():
    with Pro600() as pro600:
        pro600.get_cartesian_position()
        pro600.home()
        pro600.move_cartesian([-132,-500,-70 ,0,0,0],speed=750)
        

if __name__ == "__main__":
    gripper()