from nimutool.canbus import *
from .message_processor import *
import math
from struct import unpack


def is_high_range(number: int): 
    return number & (1 << 60) != 0

def unpack_20b_float(val, range_hi):
    shift = 13 if range_hi else 15
    return twos_comp(val, 20) / (1 << shift)

def parse_fixpoint(data):
    val = unpack('<Q', data)[0]
    vals = [unpack_20b_float((val >> shift) & 0xfffff, is_high_range(val)) for shift in [0, 20, 40]]
    error_flags = [val & (1 << i) != 0 for i in range(61, 64)]
    return vals, error_flags

def parse_sync(data):
    tow, subsecond_ns = 0, 0
    if len(data) == 8:
        tow, subsecond_ns = unpack('<II', data)
    return (tow, subsecond_ns)

def parse_imuloc(data):
    nid, x, y, z = unpack('<Bxhhh', data)
    return (nid, x, y, z)

def parse_ekf_status(data):
    mode, res1, res2, res3 = unpack('<BBhI', data)
    return mode

def parse_gps_tp_status(data):
    status, error_us, pll_tune, clock_cycle_counter = unpack('<BhbI', data)
    return (status, error_us, pll_tune, clock_cycle_counter)

def parse_temps(data):
    temp_hpca, temp_bmx, temp_cpu = unpack('hhhxx', data)
    return temp_hpca, temp_bmx, temp_cpu

def parse_temperature(data):
    temp = unpack('h3h', data)[0]
    return temp / 10

class NimuMessageProcessorOld(MessageProcessorBase):

    MSG_HANDLERS = {
        0x000: {'name': 'sync', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Synchronization, 'frequency': 1, 'is_extended': False, 'parser': None, 'priority': 1},
        0x010: {'name': 'hpca gyro', 'sensor': SensorModel.SCHA63T, 'type': SensorDataType.Gyroscope, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 2},
        0x020: {'name': 'bmx gyro', 'sensor': SensorModel.BMX160, 'type': SensorDataType.Gyroscope, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 4},
        0x080: {'name': 'temp', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Temperature, 'frequency': 1, 'is_extended': False, 'parser': parse_temps, 'priority': 6},
        0x110: {'name': 'hpca acc', 'sensor': SensorModel.SCHA63T, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 3},
        0x120: {'name': 'bmx acc', 'sensor': SensorModel.BMX160, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 5},
        0x140: {'name': 'dcm', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Pose3, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 7},
        0x150: {'name': 'pos', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Position, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 8},
        0x160: {'name': 'vel', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Velocity, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 9},
        0x170: {'name': 'imuloc', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.ImuPosition, 'frequency': 1, 'is_extended': False, 'parser': parse_imuloc, 'priority': 10},
        0x180: {'name': 'innovation', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Innovation, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 11},
        0x190: {'name': 'scl acc', 'sensor': SensorModel.SCLxxxx, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 12},
    }

    def canid2dataid(self, can_id):
        return can_id & 0xff0

    def split_canid_to_msgid_and_nodeid(self, can_id):
        return can_id & 0xff0, can_id & 0x00f


class NimuMessageProcessor(NimuMessageProcessorOld):

    MSG_HANDLERS = {
        0x000: {'name': 'sync', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Synchronization, 'frequency': 1, 'is_extended': False, 'parser': parse_sync, 'priority': 1},
        0x010: {'name': 'hpca acc', 'sensor': SensorModel.SCHA63T, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 3},
        0x020: {'name': 'hpca gyro', 'sensor': SensorModel.SCHA63T, 'type': SensorDataType.Gyroscope, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 2},
        0x040: {'name': 'hpca temperature', 'sensor': SensorModel.SCHA63T, 'type': SensorDataType.Temperature, 'frequency': 1, 'is_extended': False, 'parser': parse_temperature, 'priority': 4},
        0x090: {'name': 'bmx acc', 'sensor': SensorModel.BMX160, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 6},
        0x0a0: {'name': 'bmx gyro', 'sensor': SensorModel.BMX160, 'type': SensorDataType.Gyroscope, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 5},
        0x0c0: {'name': 'bmx temperature', 'sensor': SensorModel.BMX160, 'type': SensorDataType.Temperature, 'frequency': 1, 'is_extended': False, 'parser': parse_temperature, 'priority': 7},
        0x110: {'name': 'hpi acc', 'sensor': SensorModel.SCLxxxx, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 8},
        0x400: {'name': 'dcm1', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Pose1, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 11},
        0x390: {'name': 'dcm2', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Pose2, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 11},
        0x300: {'name': 'dcm3', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Pose3, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 11},
        0x330: {'name': 'imuloc', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.ImuPosition, 'frequency': 1, 'is_extended': False, 'parser': parse_imuloc, 'priority': 13},
        0x340: {'name': 'innovation', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Innovation, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 12},
        0x310: {'name': 'ekf pos', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Position, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 12},
        0x320: {'name': 'ekf vel', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.Velocity, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 12},
        0x410: {'name': 'ekf gbias', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.GyroscopeBias, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 12},
        0x420: {'name': 'ekf ascale', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.AccelerometerScale, 'frequency': 1, 'is_extended': False, 'parser': parse_fixpoint, 'priority': 12},
        0x430: {'name': 'ekf status', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.EKFStatus, 'frequency': 1, 'is_extended': False, 'parser': parse_ekf_status, 'priority': 12},
        0x500: {'name': 'gps timepulse status', 'sensor': SensorModel.NotApplicable, 'type': SensorDataType.GPSTimepulseStatus, 'frequency': 1000, 'is_extended': False, 'parser': parse_gps_tp_status, 'priority': 13},
    }
