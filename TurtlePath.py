from Kalman import KalmanFilter
from TurtleBurguerBot import TurtleBurguerBot
import numpy as np
from icecream import ic
from matplotlib import pyplot as mp
import matplotlib.animation as animation
from scipy.stats import norm
import time
import os

FIRST_DOOR = (-2.73, 0)
SECOND_DOOR = (-0.735, 0)
THIRD_DOOR = (2.73, 0)


# def animateGaussian(timeStep):
#     x = np.arange(-5, 5, timeStep)

#     fig, ax = mp.subplots()
#     # y = norm.pdf(x, mu_pred[0], np.sqrt(S_pred[0,0]))e

#     # ax.plot(x, norm.pdf(x, FIRST_DOOR[0], 0.1), '-', label=f'μ: {FIRST_DOOR[0]}, σ: 1', color='gold')
#     # ax.plot(x, norm.pdf(x, SECOND_DOOR[0], 0.1),  '-', label=f'μ: {SECOND_DOOR[0]}, σ: 1.5', color='red')
#     # ax.plot(x, norm.pdf(x, THIRD_DOOR[0], 0.1),  '-', label=f'μ: {THIRD_DOOR[0]}, σ: 2', color='pink')

#     # # line_pred = ax.plot(x, y, '-', color='orange')

#     # plotting current door locations
#     doors = [FIRST_DOOR[0], SECOND_DOOR[0], THIRD_DOOR[0]]
#     for door in doors:
#         x = np.linspace(door-1, door+1, 50)
#         y = norm.pdf(x, door, np.sqrt(0.1))
#         line_pred = ax.plot(x, y, '-', color='orange')

#     mp.show()



class TurtlePath(TurtleBurguerBot):
    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos)
        self.state = "find-next-door"

        # u = self.v["x"]
        self.sigma_a = 0.2  # Desvio padrão de odometria [m]
        self.sigma_z = 1.0   # Desvio padrão do sensor [m]
        
        self.kf = KalmanFilter(self.timestep/1000, self.sigma_a, self.sigma_z, pos[0])
        self.doors = [FIRST_DOOR[0], SECOND_DOOR[0], THIRD_DOOR[0]]

        steps = 1000
        self.data_predictions = np.zeros((1000,), dtype='f,f')
        self.data_measurements = np.zeros((1000,), dtype='f,f')
        self.data_corrections = np.zeros((1000,), dtype='f,f')


    def move(self):
        self.base_move()

    def odometry(self):
        # self.update_position()
        print(f'previous Position: x: {self.kf.x:2f}[m]')
        [xbarra, Ebarra] = self.kf.predict(self.v["x"])
        print(f'Position Predicted: x: {xbarra:2f}[m]')
        self.data_predictions[self.steps] = (xbarra, Ebarra)

    def correctPrediction(self):
        ic(self.doors)
        z = self.doors.pop(0)
        ic(z)
        self.data_measurements[self.steps] = (z, self.sigma_z)
        [x, E] = self.kf.update(z)
        self.data_corrections[self.steps] = (x, E)
        print(f'Position Updated: x: {x:2f}[m]')

    def update(self):
        ic(self.steps, self.state)
        match self.state:
            case "checking":
                # get lidar values
                lidar_values = self.lidar.getRangeImage()
                # ic(lidar_values[72:109])

                allInf = True
                for i in range(71, 110):
                    if lidar_values[i] != float('inf'):
                        allInf = False
                        continue

                if allInf:
                    if (len(self.doors) > 0):
                        self.correctPrediction()
                        self.state = "find-next-door"
                    else:
                        self.state = "graph"

            
            case "find-next-door":
                self.move_forward(self.max_speed)
                self.state = "checking"

            case "graph":
                self.stop()
                self.state = "stop"
                np.savez_compressed(
                    f"./data_kalman.npz",
                    timeStep=self.timestep,
                    predictions=self.data_predictions,
                    measurements=self.data_measurements,
                    corrections=self.data_corrections,
                )
                # showGaussian()

            case "stop":
                self.stop()
                
