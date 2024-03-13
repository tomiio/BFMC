import numpy as np
import scipy

def skew(x):
    '''
    takes in a 3d column vector
    returns its Skew-symmetric matrix
    '''

    x = x.T[0]
    return np.array([[0, -x[2], x[1]], [x[2], 0, -x[0]], [-x[1], x[0], 0]])

# Convert accelerator to roll, pitch, yaw
def accel2EulerAngles(ax, ay, az, dt):
    roll = np.arcsin(ax / scipy.g)
    pitch = -np.arcsin(ay / scipy.g * np.cos(roll))
    print("Roll:", roll, ", Pitch:", pitch)
    yaw = 0
    return roll, pitch, yaw

# Rotates body frame to inertial frame unp.sing quaternion as input
def quat2RotMatrix(q0, q1, q2, q3):
    return np.array([[1 - 2*(q0**2 + q1**2), 2*(q1*q2 - q0*q3), 2*(q1*q3 + q0*q2)],
                     [2*(q1*q2 + q0*q3), 1 - 2*(q0**2 + q2**2), 2*(q2*q3 - q0*q1)],
                     [2*(q1*q3 - q0*q2), 2*(q2*q3 + q0*q1), 1 - 2*(q0**2 + q3**2)]])

# Rotates body frame to inertial frame unp.sing Euler angles as input 
def euler2RotMatrix(roll, pitch, yaw):
    heading = np.array([[np.cos(pitch), -np.sin(yaw), 0],
                        [np.sin(yaw),    np.cos(yaw), 0], 
                        [0,           0,        1]])
    roll_pitch = np.array([[np.cos(pitch),  np.sin(pitch)*np.sin(roll), np.sin(pitch)*np.cos(roll)], 
                           [0,              np.cos(roll),              -np.sin(roll)           ],
                           [-np.sin(pitch), np.cos(pitch)*np.sin(roll), np.cos(pitch)*np.cos(roll)]])
    return np.dot(heading, roll_pitch)

# Transform quaternion to Euler angles
def quat2EulerAngles(q0, q1, q2, q3):
    roll  = np.degrees(np.arctan2(2*(q2*q3 + q0*q1), 1 - 2*(q0**2 + q3**2)))
    pitch = np.degrees(np.arcsin(2*(q1*q3 - q0*q2)))
    yaw   = np.degrees(np.arctan2(2*(q1*q2 + q0*q3), 1 - 2*(q0**2 + q1**2)))
    return np.array([roll, pitch, yaw])

# Construct state transition model for attitude
def gyroTransitionMatrix(wx, wy, wz, dt):
    A = np.array(
        np.eye(4) + \
        dt/2 * np.array(
            [[0 , -wx,  -wy,  -wz],
             [wx,  0,    wz,  -wy],
             [wy, -wz,   0 ,   wx],
             [wz,  wy,  -wx,   0 ]]
        )
    )
    return A

def euler2Quat(roll, pitch, yaw):
    cr = np.cos(0.5 * roll)
    sr = np.sin(0.5 * roll)

    cp = np.cos(0.5 * pitch)
    sp = np.sin(0.5 * pitch)

    cy = np.cos(0.5 * yaw)
    sy = np.sin(0.5 * yaw)

    q0 = cr * cp * cy + sr * sp * sy
    q1 = sr * cp * cy - cr * sp * sy
    q2 = cr * sp * cy + sr * cp * sy
    q3 = cr * cp * sy - sr * sp * cy

    return np.array([[q0, q1, q2, q3]]).T

# Quaternion unit length
def normalizedQuat(q0, q1, q2, q3):
    norm = np.sqrt(q0**2 + q1**2 + q2**2 + q3**2)
    return np.array([q/norm for q in [q0, q1, q2, q3]])

def normalized(x):
    try:
        return x / np.linalg.norm(x)
    except:
        return x
    
def jacobianW(q):
    q = q.T[0]
    return 0.5 * np.array([[-q[1], -q[2], -q[3]], 
                           [ q[0], -q[3],  q[2]],
                           [ q[3],  q[0], -q[1]], 
                           [-q[2],  q[1],  q[0]]])

def Hhelper(q, vector):
    # just for convenience
    x = vector.T[0][0]
    y = vector.T[0][1]
    z = vector.T[0][2]
    q0 = q.T[0][0]
    q1 = q.T[0][1]
    q2 = q.T[0][2]
    q3 = q.T[0][3]

    h = np.array([
        [q0*x - q3*y + q2*z, q1*x + q2*y + q3*z, -q2*x + q1*y + q0*z, -q3*x - q0*y + q1*z],
        [q3*x + q0*y - q1*z, q2*x - q1*y - q0*z, q1*x + q2*y + q3*z, q0*x - q3*y + q2*z],
        [-q2*x + q1*y +q0*z, q3*x + q0*y - q1*z, -q0*x + q3*y - q2*z, q1*x + q2*y + q3*z]
    ])
    return 2 * h


def H(q, gn, mn):
    '''
    Measurement matrix
    '''

    H1 = Hhelper(q, gn)
    H2 = Hhelper(q, mn)
    return np.vstack((-H1, H2))

def rotate(q):
    '''
    rotation transformation matrix
    nav frame to body frame as q is expected to be q^nb
    R(q) @ x to rotate x
    '''

    qv = q[1:4, :]
    qc = q[0]
    return (qc**2 - qv.T @ qv) * np.eye(3) - 2 * qc * skew(qv) + 2 * qv @ qv.T

def filtSignal(data, dt=0.01, wn=10, btype='lowpass', order=1):
    '''
    filter all data at once
    uses butterworth filter of scipy
    @param data: [...]
    @param dt: sampling time
    @param wn: critical frequency
    '''
    
    res = []
    n, s = scipy.signal.butter(order, wn, fs=1 / dt, btype=btype)
    for d in data:
        d = scipy.signal.filtfilt(n, s, d, axis=0)
        res.append(d)
    return res

def yawRotationMatrix(yaw):
    return np.array([[np.cos(yaw), -np.sin(yaw), 0],
                     [np.sin(yaw),  np.cos(yaw), 0],
                     [0, 0, 1]])

if __name__ == "__main__":
    roll = np.deg2rad(45)
    pitch = np.deg2rad(45)
    yaw = np.deg2rad(45)
    x=3
    y=1
    z=0

    q0 = np.cos(np.pi/8)
    q1 = 0
    q3 = np.sin(np.pi/8)
    q2 = 0
    # print(quat2RotMatrix(q0, q1, q2, q3))
    # print(np.dot(quat2RotMatrix(q0, q1, q2, q3), np.array([x, y ,z])))
