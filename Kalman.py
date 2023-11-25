import numpy as np
from matplotlib import pyplot as plt


class KalmanFilter(object):
  """
  Kalman Filter using a constant acceleration motion model
  """

  def __init__(self, dt, sigma_a, sigma_z, x):
    self.dt = dt # time step
    # self.u = u  # motion model control input
    self.sigma_a = sigma_a # motion model noise
    self.sigma_z = sigma_z # measurement noise
    
    # self.A = np.matrix([[1, self.dt], [0, 1]])
    self.A = 1

    # self.B = np.matrix([[(self.dt**2)/2], [self.dt]])
    self.B = self.dt

    # self.R = np.matrix([self.dt**2]) * self.sigma_a ** 2
    self.R = self.dt**2 * self.sigma_a ** 2
    
    self.Q = sigma_z ** 2
    
    self.E = 1

    self.C = 1

    self.x = x

  def predict(self, u):
    self.x = (self.A * self.x) + (self.B * u)
    self.E = self.E + self.R
    return [self.x, self.E]

  def update(self, z):
    K = self.E / (self.E + self.Q)
    self.x = self.x + K*(z-self.x)
    self.E = self.E - K*self.E
    return [self.x, self.E]


def main():
  dt = 0.1

  t = np.arange(0, 100, dt)

  # real
  real_x = 0.1*((t**2)-t)

  u = 1
  sigma_a = 0.25
  sigma_z = 2.0
  kf = KalmanFilter(dt, u, sigma_a, sigma_z)

  predictions = []
  measurements = []

  for x in real_x:
    z = kf.C.item(0)*x + np.random.normal(0, 50)

    measurements.append(z)
    x_kf = kf.predict().item(0)
    kf.update(z)

    predictions.append(x_kf)

  fig = plt.figure()

  plt.plot(t, measurements, label='Measurements', color='b', linewidth=0.5)
  plt.plot(t, np.array(real_x), label='Real Track',
           color='y', linewidth=1.5)
  plt.plot(t, predictions,
           label='Kalman Filter Prediction', color='r', linewidth=1.5)
  plt.show()


if __name__ == "__main__":
  main()