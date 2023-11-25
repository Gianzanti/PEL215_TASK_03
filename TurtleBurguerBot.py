from abc import ABC, abstractmethod
from controller import Robot

INF = float("+inf")

class TurtleBurguerBot(ABC):
    def __init__(self, initPos: tuple[float, float] = (0.0, 0.0)) -> None:
        """
        initPos: tuple[float, float] - defines initial position (x,y) for robot, defaults to (0.0, 0.0)
        """
        self.me = Robot()
        self.timestep = int(self.me.getBasicTimeStep()) * 1
        maxVelocity = 6.67  # rad/s
        self.wheel_radius = 0.033  # m
        self.max_speed = maxVelocity * self.wheel_radius  # m/s
        self.speed_increment = 0.5 * self.max_speed
        self.v = {"x": 0.0, "y": 0.0}
        self.p = {"x": initPos[0], "y": initPos[1]}
        self.wheels = []
        self.steps = 0
        self.initMotors()
        self.initSensors()

    def initMotors(self):
        self.wheels.append(self.me.getDevice("left wheel motor"))
        self.wheels.append(self.me.getDevice("right wheel motor"))
        self.set_wheel_speeds([0, 0])

    def set_wheel_speeds(self, speeds):
        for i in range(0, 2):
            self.wheels[i].setPosition(INF)
            self.wheels[i].setVelocity(speeds[i])

    def initSensors(self):
        self.lidar = self.me.getDevice("LDS-01")
        self.lidar.enable(self.timestep)
        self.lidar.enablePointCloud()

    def base_move(self):
        speeds = [
            1 / self.wheel_radius * (self.v["x"] + self.v["y"]),
            1 / self.wheel_radius * (self.v["x"] - self.v["y"]),
        ]
        self.set_wheel_speeds(speeds)
        # print(f"Speeds: vx: {self.v['x']:2f}[m/s], vy: {self.v['y']:2f}[m/s]")

    def move_forward(self, speed):
        self.v["x"] += speed
        self.v["x"] = self.v["x"] if self.v["x"] < self.max_speed else self.max_speed

    def move_backward(self, speed):
       
        self.v["x"] -= speed
        self.v["x"] = self.v["x"] if self.v["x"] > -self.max_speed else -self.max_speed

    def stop(self):
        self.v["x"] = 0

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def odometry(self):
        pass

    def run(self):
        while self.me.step(self.timestep) != -1:
            self.update()
            self.move()
            self.odometry()
            self.steps += 1
