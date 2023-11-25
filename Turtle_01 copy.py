import numpy as np
from icecream import ic
from matplotlib import pyplot as mp
from scipy.stats import norm
from controller import Robot

def gaussian(x:float, μ: float, Σ: float):
    return (
        1.0 / (np.sqrt(2.0 * np.pi) * Σ) * np.exp(-np.power((x - μ) / Σ, 2.0) / 2)
    )

# x_values = np.linspace(-3, 3, 120)
# for mu, sig in [(-1, 1), (0, 2), (2, 3)]:
#     mp.plot(x_values, gaussian(x_values, mu, sig))

# mp.show()

MAX_VELOCITY = 6.67 # Maximum velocity for the wheels [rad/s]
WHEEL_RADIUS = 0.033 # Wheel radius [m]
INITIAL_POSITION = (-4,0)

FIRST_DOOR = (-2.73, 0)
SECOND_DOOR = (-0.735, 0)
THIRD_DOOR = (2.73, 0)

def showGaussian():
    #x-axis ranges from -5 and 5 with .001 steps
    x = np.arange(-5, 5, 0.001)

    #define multiple normal distributions
    mp.plot(x, norm.pdf(x, FIRST_DOOR[0], 0.1), label=f'μ: {FIRST_DOOR[0]}, σ: 1', color='gold')
    mp.plot(x, norm.pdf(x, SECOND_DOOR[0], 0.1), label=f'μ: {SECOND_DOOR[0]}, σ: 1.5', color='red')
    mp.plot(x, norm.pdf(x, THIRD_DOOR[0], 0.1), label=f'μ: {THIRD_DOOR[0]}, σ: 2', color='pink')

    #add legend to plot
    # mp.legend(title='Parameters')

    #add axes labels and a title
    mp.ylabel('Densidade')
    mp.xlabel('Posição X (m)')
    mp.title('Distribuição Normal do Mapa', fontsize=14)
    mp.show()

def main():
    # showGaussian()
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())
    # get and enable the lidar
    lidar = robot.getDevice("LDS-01")
    lidar.enable(timestep)
    lidar.enablePointCloud()

    # # get lidar motor and enable rotation (only for visualization, no effect on the sensor)
    # lidar_main_motor = robot.getDevice("LDS-01_main_motor")
    # lidar_secondary_motor = robot.getDevice("LDS-01_secondary_motor")
    # lidar_main_motor.setPosition(float('inf'))
    # lidar_secondary_motor.setPosition(float('inf'))
    # lidar_main_motor.setVelocity(30.0)
    # lidar_secondary_motor.setVelocity(60.0)

    # get the motors and enable velocity control
    right_motor = robot.getDevice("right wheel motor")
    left_motor = robot.getDevice("left wheel motor")
    right_motor.setPosition(float('inf'))
    left_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)
    left_motor.setVelocity(0.0)

    # lidar_width = lidar.getHorizontalResolution()
    # lidar_max_range = lidar.getMaxRange()

    # # init braitenberg coefficient
    # braitenberg_coefficients = np.zeros(lidar_width)
    # for i in range(lidar_width):
    #     braitenberg_coefficients[i] = 6 * gaussian(i, lidar_width / 4, lidar_width / 12)

    BASE_SPEED = 1.5
    STEPS = 0
    while robot.step(timestep) != -1:
        STEPS += 1
        left_speed = BASE_SPEED
        right_speed = BASE_SPEED
        
        # get lidar values
        lidar_values = lidar.getRangeImage()
        ic(lidar_values[72:109])

        allInf = True
        for i in range(72, 109):
            if lidar_values[i] != float('inf'):
                allInf = False
                continue
            
        # if allInf:
        #     left_speed = 0.0
        #     right_speed = 0.0

        # # # apply the braitenberg coefficients on the resulted values of the lidar
        # # for i in range(int(0.25 * lidar_width), int(0.5 * lidar_width)):
        # #     j = lidar_width - i - 1
        # #     k = i - 0.25 * lidar_width
        # #     if lidar_values[i] != float('inf') and not np.isnan(lidar_values[i]) and lidar_values[j] != float('inf') and not np.isnan(lidar_values[j]):
        # #         left_speed += braitenberg_coefficients[k] * ((1.0 - lidar_values[i] / lidar_max_range) - (1.0 - lidar_values[j] / lidar_max_range))
        # #         right_speed += braitenberg_coefficients[k] * ((1.0 - lidar_values[j] / lidar_max_range) - (1.0 - lidar_values[i] / lidar_max_range))

        # apply computed velocities
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)



       

if __name__ == "__main__":
    main()