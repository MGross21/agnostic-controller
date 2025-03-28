from agnostic_controller.templates import SocketController as SCT
import math

class UniversalRobotics(SCT):
    def __init__(self, ip:str, port:int):
        super().__init__(ip, port)
        self.JOINT_RANGES = [ 
            (-math.pi, math.pi),
            (-math.pi, math.pi),
            (-math.pi, math.pi),
            (-math.pi, math.pi),
            (-math.pi, math.pi),
            (-math.pi, math.pi)
        ]
        self.DOF = len(self.JOINT_RANGES)

    async def sleep(self, seconds):
        await self.send_command(f"sleep({seconds})")

    async def move_joints(self, joint_positions, *args, **kwargs)->str:
        """
        MoveJ
        --------
        Move the robot to the specified joint positions.

        Parameters
        ----------
        joint_positions : list of float
            Joint positions in radians [j1, j2, j3, j4, j5, j6].
        speed : float, optional
            Speed of the movement in rad/s (default: 0.1).
        acceleration : float, optional
            Acceleration of the movement in rad/s^2 (default: 0.0).
        time : float, optional
            The time in seconds to make the move. If specified, the command will ignore the speed and acceleration values (default: 0.0).
        r : float, optional
            Blend radius in meters (default: 0.0).
        DOF : int, optional
            Degrees of freedom (default: 6).
        """
        if len(joint_positions) != kwargs.get("DOF", 6):
            raise ValueError("Joint positions must have 6 elements")

        v = kwargs.get("speed", 0.1)
        assert v < 2, "Speed out of range: 0 ~ 2" # Source: https://forum.universal-robots.com/t/maximum-axis-speed-acceleration/13338/4
        
        a = kwargs.get("aceleration", 0.0)
        assert a <= 10, "Acceleration out of range: 0 ~ 10" # Source: https://forum.universal-robots.com/t/maximum-axis-speed-acceleration/13338/2
        # OR
        t = kwargs.get("time", 0.0)

        r = kwargs.get("r", 0.0)

        for pos in joint_positions:
            if not (0 <= pos <= math.pi*2):
                raise ValueError(f"Joint position {pos} out of range: 0 ~ {math.pi*2}")
            
        command = f"movej(p[{','.join(map(str, joint_positions))}], a={a}, v={v}, t={t}, r={r})\n"
        return await self.send_command(command)

    async def move_cartesian(self, robot_pose, *args, **kwargs)->str:
        """
        Move the robot to the specified cartesian position. (`movel` or `movep`)

        Parameters
        ----------
        robot_pose : list of float
            Cartesian position and orientation [x, y, z, rx, ry, rz] in meters and radians.
        moveType : str, optional
            Type of movement: "movel" for linear cartesian pathing or "movep" for circular cartesian pathing (default: "movel").
        speed : float, optional
            Velocity of the movement in m/s (default: 0.1).
        acceleration : float, optional
            Acceleration of the movement in m/s^2 (default: 0.0).
        time : float, optional
            The time in seconds to make the move. If specified, the command will ignore the speed and acceleration values (default: 0.0).
        r : float, optional
            Blend radius in meters (default: 0.0).
        """
        moveType = kwargs.get("moveType", "movel")
        assert moveType in ["movel", "movep"], "Unsupported move type: movel or movep"

        v = kwargs.get("speed", 0.1)
        assert v < 2, "Speed out of range: 0 ~ 2" # Source: https://forum.universal-robots.com/t/maximum-axis-speed-acceleration/13338/4
        
        a = kwargs.get("aceleration", 0.0)
        assert a <= 10, "Acceleration out of range: 0 ~ 10" # Source: https://forum.universal-robots.com/t/maximum-axis-speed-acceleration/13338/2
        # OR
        t = kwargs.get("time", 0.0)

        r = kwargs.get("r", 0.0)

        for pos in robot_pose[3:]:
            if not (0 <= pos <= math.pi*2):
                raise ValueError(f"Joint position {pos} out of range: 0 ~ {math.pi*2}")
            
        if await self.send_command("is_within_safety_limits({})".format(','.join(map(str, robot_pose)))) == "False":
            raise ValueError("Cartesian position out of safety limits")

        command = f"{moveType}(p[{','.join(map(str, robot_pose))}], a={a}, v={v}, t={t}, r={r})\n"
        return await self.send_command(command)

    async def get_joint_positions(self, *args, **kwargs):
        return await self.send_command("get_actual_joint_positions()\n")

    async def get_cartesian_position(self, *args, **kwargs):
        return await self.send_command("get_actual_tcp_pose()\n")

    async def stop_motion(self):
        return await self.send_command("stopj(2)") # deceleration: 2 rad/s^2

    async def get_robot_state(self):
        return await self.send_command("get_robot_status()\n")
