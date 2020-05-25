
import KalmanFilter
import numpy as np
import math
from common import Q_discrete_white_noise
from KalmanFilter import  KalmanFilter
class SinkKalmanFilter:
    def __init__(self, sensor_id):
        self.cache=[]
        self.sensor_id=sensor_id
        self.readings=[]
        r_std, q_std = 1., 0.003
        self.kf = KalmanFilter(dim_x=2, dim_z=1)
        self.kf.x = np.array([[19], [0]])  # position, velocity
        self.kf.F = np.array([[1, 1], [0, 1]])
        self.kf.R = np.array([[r_std ** 2]])  # input noise
        self.kf.H = np.array([[1., 0.]])
        self.kf.P = np.diag([0.001 ** 2, 0])
        self.kf.Q = Q_discrete_white_noise(2, 1, q_std ** 2)
        self.last_est=0


    def run(self, sensorReading):
        est=[]

        est = self.kf.predict()

        if sensorReading is None:
            self.kf.update([self.last_est])
        else:
            self.kf.update([sensorReading])
        self.last_est=est[0][0]
        return est[0][0]



