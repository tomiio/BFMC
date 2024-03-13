#!/usr/bin/env python3
import numpy as np
from helpers import *
import json

import rospy
from std_msgs.msg import String

class IMUNode:
    def __init__(self):
    
        self.speed = 0.2
        self.imuData = []
        self.tracker = IMU(sampling=10)
        
        rospy.init_node('imuNODE', anonymous=False)
        self.command_subscriber = rospy.Subscriber("/automobile/command", String, self.callback)
        self.imu_data = rospy.Subscriber("/automobile/imu_data", String, self.callback2) 
        self.publisher = rospy.Publisher("/automobile/position", String, queue_size=1)
        
        rospy.spin()
        
    def callback(self, msg):
        command = json.loads(msg.data)
        if command["action"] == '1':
            self.speed = command["speed"]
    
    def callback2(self, msg):
        data = msg.data
        data = json.loads(data)
        self.imuData.append([float(data['roll']), 
                             float(data['pitch']), 
                             float(data['yaw']), 
                             float(data['accX']), 
                             float(data['accY']), 
                             float(data['accZ'])])
        
        if len(self.imuData) == 10:
            
            # print('initializing...')
            # init_list = tracker.initVariance(data[5:30])

            # print('--------')
            # print('processing...')
            
            # EKF step
            # a_nav, orix, oriy, oriz = tracker.attitudeTracking(data[30:], init_list)
            a_nav = self.tracker.attitudeObtain(self.imuData)
            p = self.tracker.posTrackWithConstantSpeed(a_nav, self.imuData, self.speed).tolist()
            pub = {"x": p[-1][0], "y": p[-1][1], "z":p[-1][2]}
            pub = json.dumps(pub)
            print(pub)
            self.publisher.publish(pub)
            self.imuData.pop(0)
            # Acceleration correction step
            
            # a_nav_filtered = tracker.removeAccErr(a_nav, filter=False)
            #p lot3([a_nav, a_nav_filtered])
 
            # ZUPT step
            # v = tracker.zupt(a_nav_filtered, threshold=0.2)
            # plot3([v])
        
            # Integration Step
            # p = tracker.positionTracking(a_nav_filtered, v)
            # plot3D([[p, 'position']])
            
            
class IMU(object):
    def __init__(self, sampling):
        self.sampling = sampling
        self.accel    = np.zeros(3)
        self.gyro     = np.zeros(3)
        self.magne    = np.zeros(3)
        self.dt       = 1 / self.sampling
        
        # ---- Init kalman filter matrix ----
        # Transition matrix
        Ft = np.array([[1., self.dt, 0.5 * self.dt**2],
                       [0.,      1.,       self.dt   ],
                       [0.,      0.,       1.        ]])
        self.F = np.eye(9)
        self.F[0:3, 0:3] = Ft
        self.F[3:6, 3:6] = Ft
        self.F[6:9, 6:9] = Ft

        self.n = self.F.shape[1]

        Qt = np.array([[self.dt**5 / 20, self.dt**4 / 8, self.dt**3/ 6], \
                        [self.dt**4 / 8, self.dt**3 / 9, self.dt**2 / 2], \
                        [self.dt**3 / 6, self.dt**2 / 2, self.dt]])
        self.Q = np.eye(9)
        self.Q[0:3, 0:3] = Qt
        self.Q[3:6, 3:6] = Qt
        self.Q[6:9, 6:9] = Qt

        self.P = np.eye(9) * 25
        self.x = np.zeros(self.F.shape[0])

        self.H = np.array([[0, 1, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 1, 0],])
        
        self.R = np.eye(3) * (0.5)
        
    # Get variance and bias from data
    def initVariance(self, data, noiseCoeff={'w': 100, 'a': 100, 'm': 10}):
        
        # Discard the first few readings due to fluctuation
        a = data[:, 0:3] # change here for data
        w = data[:, 3:6]
        m = data[:, 6:9]

        # ---- Gravity ----
        gn = -a.mean(axis=0)
        gn = gn[:, np.newaxis]
        # Save the initial magnitude of gravity
        g0 = np.linalg.norm(gn)

        # ---- Magnetic field ----
        mn = m.mean(axis=0)
        mn = normalized(mn)[:, np.newaxis]

        # ---- Noise covariance ---- 
        aVar = a.var(axis=0)
        wVar = w.var(axis=0)
        mVar = m.var(axis=0)
        print('acc var: %s, norm: %s' % (aVar, np.linalg.norm(aVar)))
        print('ang var: %s, norm: %s' % (wVar, np.linalg.norm(wVar)))
        print('mag var: %s, norm: %s' % (mVar, np.linalg.norm(mVar)))

        # ---- Sensor noise ----
        gyroNoise  = noiseCoeff['w'] * np.linalg.norm(wVar)
        gyroBias   = w.mean(axis=0)

        accelNoise = noiseCoeff['a'] * np.linalg.norm(aVar)

        magneNoise = noiseCoeff['m'] * np.linalg.norm(mVar)

        return (gn, g0, mn, gyroNoise, gyroBias, accelNoise, magneNoise)
    
    def initVar(self, data):
        a = data[:, 3:6]
        
        # Gravity
        gn = -a.mean(axis=0)
        gn = gn[:, np.newaxis]
        # Save the initial magnitude of gravity
        g0 = np.linalg.norm(gn)
        
        return gn, g0
    
    # Track attitude of vehicle
    def attitudeTracking(self, data, initVal):
        # ---- Calibrated data goes here! ----
        gn, g0, mn, gyroNoise, gyroBias, accelNoise, magneNoise= initVal
        a = data[:, 0:3] - gyroBias
        w = data[:, 3:6] 
        m = data[:, 6:9] 
        sampleSize = np.shape(data)[0]

        # ---- Data container ----
        aNav = []
        oriX = []
        oriY = []
        oriZ = []

        # ---- States and covariance matrix ----
        P = 1e-10 * np.eye(4)
        x = np.array([[1, 0, 0, 0]]).T      # Quaternion state column vector [[q0 q1 q2 q3]]
        initOri = np.eye(3)           # Rotation matrix

        # ---- Extended Kalman filter ----
        t = 0
        while t < sampleSize:
            # ---- Data prep ----
            wt = w[t, np.newaxis].T
            at = a[t, np.newaxis].T
            mt = normalized(m[t, np.newaxis].T)

            # ---- Predict ----
            # Use normalized measurements to reduce error
            F = gyroTransitionMatrix(wt[0][0], wt[1][0], wt[2][0], self.dt)
            W = jacobianW(x)
            Q = (gyroNoise * self.dt) ** 2 * W @ W.T
            x = normalized(F @ x)
            P = F @ P @ F.T + Q

            # ---- Update ----
            # ---- Acceleration and magnetic field prediction ---- 
            q  = x.T[0]
            pa = normalized(-quat2RotMatrix(q[0], q[1], q[2], q[3]) @ gn)
            pm = normalized(quat2RotMatrix(q[0], q[1], q[2], q[3]) @ mn)

            # Residual    
            y = np.vstack((normalized(at), mt)) - np.vstack((pa, pm))

            # Sensor noise matrix
            Ra = [(accelNoise/ np.linalg.norm(at))**2 + (1 - g0 / np.linalg.norm(at))**2] * 3
            Rm = [magneNoise**2] * 3
            R  = np.diag(Ra + Rm)

            # Kalman gain
            Ht = H(x, gn, mn)
            S  = Ht @ P @ Ht.T + R
            K  = P @ Ht.T @ np.linalg.inv(S)
            x = x + K @ y
            P = P - K @ Ht @ P

            # ---- Post update ----
            x = normalized(x)
            P = 0.5 * (P + P.T)         # Symmetric

            # ---- Navigation frame acceleration ----
            conj = -np.eye(4)
            conj[0][0] = 1
            an = rotate(conj @ x) @ at + gn
            orin = rotate(conj @ x) @ initOri

            # ---- Save data ----
            aNav.append(an.T[0])
            oriX.append(orin.T[0, :])
            oriY.append(orin.T[1, :])
            oriZ.append(orin.T[2, :])

            t += 1
        
        aNav = np.array(aNav)
        oriX = np.array(oriX)
        oriY = np.array(oriY)
        oriZ = np.array(oriZ)

        return (aNav, oriX, oriY, oriZ)

    def attitudeObtain(self, data):
        #  ---- Data preparation ----
        data = np.array(data)
        sampleSize = np.shape(data)[0]
        gn, _ = self.initVar(data)

        euler = data[:, 0:3]
        euler = np.deg2rad(euler)
        a     = data[:, 3:6]
        
         # ---- Data container ----
        aNav = []
        
        t = 0
        while t < sampleSize:
            eulert = euler[t, np.newaxis].T
            at     = a[t, np.newaxis].T
            q = euler2Quat(eulert[0][0], eulert[1][0], eulert[2][0]) 
            q = normalized(q)

            # ---- Navigation frame acceleration ----
            conj = -np.eye(4)
            conj[0][0] = 1
            an = rotate(conj @ q) @ at + gn
            # print(rotate(conj @ q))

            # ---- Save data ----
            aNav.append(an.T[0])
            t += 1
        
        aNav = np.array(aNav)
        return aNav

    def posTrackWithConstantSpeed(self, aNav, data, speed):
        #  ---- Data preparation ----
        data = np.array(data)
        sampleSize = np.shape(data)[0]
        euler = data[:, 2]
   
        euler = np.deg2rad(euler)
        aVar = aNav.mean(axis=0)
        accelNoise = np.linalg.norm(aVar) * 100

        self.Q = self.Q * accelNoise
        # ---- Data container ----
        pos = []

        t = 0
        while t < sampleSize: 
            # ---- Predict step ----
            self.x[2] = aNav[t][0]
            self.x[5] = aNav[t][1]
            self.x[8] = aNav[t][2]

            self.x = self.F @ self.x
            self.P = self.F @ self.P @ self.F.T + self.Q
            # ---- Update step ----
            # Đưa speed xe về navigation frame
            z = [0., 0., 0.] 
            x_speed = speed * np.cos(euler[t])
            y_speed = speed * np.sin(euler[t])
            # z = [x_speed, y_speed, 0.]
            
            S = self.H @ self.P @ self.H.T + self.R
            Sinv = np.linalg.inv(S)
            K = self.P @ self.H.T @ Sinv

            y = z - self.H @ self.x
            print(y)
            self.x = self.x + K @ y

            I = np.eye(self.n)
            self.P = (I - K @ self.H) @ self.P
            self.P = 0.5 * (self.P + self.P.T)    

            pos.append([self.x[0], self.x[3], self.x[6]])

            t += 1
        pos = np.array(pos)
        return pos
        
    def removeAccErr(self, aNav, threshold=0.2, filter=False, wn=(0.01, 15)):
        sampleSize = np.shape(aNav)[0]
        tStart = 0
        for t in range(sampleSize):
            at = aNav[t]
            if np.linalg.norm(at) > threshold:
                tStart = t
                break
        
        tEnd = 0
        for t in range(sampleSize - 1, -1, -1):
            at = aNav[t]
            if np.linalg.norm(at - aNav[-1]) > threshold:
                tEnd = t
                break

        anDrift = aNav[tEnd:].mean(axis=0)     
        anDriftRate = anDrift / (tEnd - tStart)

        for i in range(tEnd - tStart):
            aNav[tStart + i] -= (i + 1) * anDriftRate

        for i in range(sampleSize - tEnd):
            aNav[tEnd + i] -= anDrift

        if filter:
            filteredAccNav = filtSignal([aNav], dt=self.dt, wn=wn, btype='bandpass')[0]
            return filteredAccNav
        else: 
            return aNav
    
    # Applies zero velocity update (ZUPT) algorithm to accel data
    def zupt(self, aNav, threshold):
        sampleSize = np.shape(aNav)[0]
        vel = []
        prevt = -1
        stillPhase = False

        v = np.zeros((3, 1))
        t = 0
        while t < sampleSize:
            at = aNav[t, np.newaxis].T

            if np.linalg.norm(at) < threshold:
                if not stillPhase:
                    predictVel = v + at * self.dt
                    
                    velDriftRate = predictVel / (t - prevt)
                    for i in range(t - prevt - 1):
                        vel[prevt + 1 + i] -= (i + 1) * velDriftRate.T[0]

                v = np.zeros((3, 1))
                prevt = t
                stillPhase = True
            else:
                v = v + at * self.dt
                stillPhase = False

            vel.append(v.T[0])
            t += 1
        vel = np.asarray(vel)
        return vel
    
    def positionTracking(self, aNav, vel):
        sampleSize = np.shape(aNav)[0]
        pos = []
        p = np.array([[0., 0., 0.]]).T

        t = 0
        while t < sampleSize:
            at = aNav[t, np.newaxis].T
            vt = vel[t, np.newaxis].T 

            p = p + vt * self.dt + 0.5 * at + self.dt**2
            pos.append(p.T[0])
            t += 1

        pos = np.array(pos)
        # fields = ['x', 'y', 'z']
        # filename = "pos.csv"
        # with open(filename, 'w') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(fields)
        #     writer.writerows(pos)
        return pos

if __name__ == '__main__':
    imu = IMUNode()
    