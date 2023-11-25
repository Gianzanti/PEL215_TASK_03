class KalmanFilter(object):
  """
  Kalman Filter using a constant acceleration motion model
  """

  def __init__(self, dt, sigma_a, sigma_z, x):
    self.dt = dt # time step
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

