from typing import *
from nimutool.canbus.can_message import *
from nimutool.data.conversion import *
from math import *

SEP = ';'

def format_imuloc(vals):
    nid, x, y, z = vals
    return [f'{nid}', f'{x / 100:2.2f}', f'{y / 100:2.2f}', f'{z / 100:2.2f}']

def format_fixpoint(vals):
    return format_list_of_floats(vals[0])

def format_float(val):
    return [f'{val:7.7f}']

def format_synchronization(vals):
    return [f'{vals[0] + vals[1] / 1e9:7.6f}']

def format_list_of_floats(vals):
    return [f'{v:7.7f}' for v in vals]

def format_fixpoint_err(vals):
    return format_fixpoint(vals) + ['1' if not e else '0' for e in vals[1]]

def format_list_of_integers(vals):
    return [f'{v}' for v in vals]

def format_ekf_status(vals):
    return [f'{vals}']

def formatter_csv(elems):
    return SEP.join(arg.strip() for arg in elems)

def formatter_console(elems):
    return ' '.join(elems)

FORMATTERS = {
    (SensorModel.NotApplicable, SensorDataType.Synchronization): {'formatter': format_synchronization, 'header': ['gpstime']},
    (SensorModel.SCHA63T, SensorDataType.Accelerometer): {'formatter': format_fixpoint, 'header': ['hax', 'hay', 'haz']},
    (SensorModel.SCHA63T, SensorDataType.Gyroscope): {'formatter': format_fixpoint_err, 'header': ['hgx', ' hgy', 'hgz', 'hgxe', 'hgye', 'hgze']},
    (SensorModel.SCHA63T, SensorDataType.Temperature): {'formatter': format_float, 'header': ['ht']},
    (SensorModel.BMX160, SensorDataType.Accelerometer): {'formatter': format_fixpoint, 'header': ['bax', 'bay', 'baz']},
    (SensorModel.BMX160, SensorDataType.Gyroscope): {'formatter': format_fixpoint, 'header': ['bgx', 'bgy', 'bgz']},
    (SensorModel.BMX160, SensorDataType.Temperature): {'formatter': format_float, 'header': ['bt']},
    (SensorModel.SCLxxxx, SensorDataType.Accelerometer): {'formatter': format_fixpoint, 'header': ['pax', 'pay', 'paz']},
    (SensorModel.PI48, SensorDataType.Accelerometer): {'formatter': format_fixpoint, 'header': ['pi48ax', 'pi48ay', 'pi48az']},
    (SensorModel.PI48, SensorDataType.Gyroscope): {'formatter': format_fixpoint, 'header': ['pi48gx', 'pi48gy', 'pi48gz']},
    (SensorModel.NotApplicable, SensorDataType.Pose1): {'formatter': format_fixpoint, 'header': ['dcm11', 'dcm12', 'dcm13']},
    (SensorModel.NotApplicable, SensorDataType.Pose2): {'formatter': format_fixpoint, 'header': ['dcm21', 'dcm22', 'dcm23']},
    (SensorModel.NotApplicable, SensorDataType.Pose3): {'formatter': format_fixpoint, 'header': ['dcm31', 'dcm32', 'dcm33']},
    (SensorModel.NotApplicable, SensorDataType.Position): {'formatter': format_fixpoint, 'header': ['posx', 'posy', 'posz']},
    (SensorModel.NotApplicable, SensorDataType.Velocity): {'formatter': format_fixpoint, 'header': ['velx', 'vely', 'velz']},
    (SensorModel.NotApplicable, SensorDataType.Innovation): {'formatter': format_fixpoint, 'header': ['innox', 'innoy', 'innoz']},
    (SensorModel.NotApplicable, SensorDataType.ImuPosition): {'formatter': format_imuloc, 'header': ['id', 'imuposx', 'imuposy', 'imuposz']},
    (SensorModel.NotApplicable, SensorDataType.PoseRPY): {'formatter': format_list_of_floats, 'header': ['roll', 'pitch', 'yaw']},
    (SensorModel.NotApplicable, SensorDataType.GyroscopeBias): {'formatter': format_fixpoint, 'header': ['gbiasx', 'gbiasy', 'gbiasz']},
    (SensorModel.NotApplicable, SensorDataType.AccelerometerScale): {'formatter': format_fixpoint, 'header': ['ascalex', 'ascaley', 'ascalez']},
    (SensorModel.NotApplicable, SensorDataType.EKFStatus): {'formatter': format_ekf_status, 'header': ['ekf_update_mode']},
    (SensorModel.NotApplicable, SensorDataType.GPSTimepulseStatus): {'formatter': format_list_of_integers, 'header': ['gps_tp_status', 'gps_tp_error_us', 'gps_tp_vco_tune', 'gps_tp_cycles']},
}

class CsvWriter:

    def __init__(self, filename, write_every_nth=1):
        self.f = open(filename, "w")
        self.write_every_nth = write_every_nth
        self.cnt = 0

    def _add_header_if_needed(self, processed_block: ProcessedCanDataBlock):
        hdr = ['timestamp', 'window_us']
        for msg in processed_block.get_messages():
            fmtr = FORMATTERS[(msg.sensor, msg.data_type)]
            hdr += [hdr_item + str(msg.nodeid) for hdr_item in fmtr['header']]
        if self.f.tell() == 0:
            self.f.write(formatter_csv(hdr) + '\n')

    def write(self, processed_block: ProcessedCanDataBlock):
        self.cnt += 1
        if self.cnt % self.write_every_nth != 0:
            return
        calculate_rpy_if_possible(processed_block)
        self._add_header_if_needed(processed_block)
        formatted_data_items = [str(processed_block.timestamp), str(processed_block.reception_window_us)]
        for msg in processed_block.get_messages():
            fmtr = FORMATTERS[(msg.sensor, msg.data_type)]
            formatted_data_items += fmtr['formatter'](msg.data)
        self.f.write(formatter_csv(formatted_data_items) + '\n')


class ConsoleWriter:

    def __init__(self, sensor_filter=None, datatype_filter=None):
        self.sensor_flt = sensor_filter
        self.datatype_flt = datatype_filter

    def is_filtered(self, msg):
        sensor_result = self.sensor_flt is not None and msg.sensor in self.sensor_flt or self.sensor_flt is None
        datatype_result = self.datatype_flt is not None and msg.data_type in self.datatype_flt or self.datatype_flt is None
        return sensor_result and datatype_result

    def write(self, processed_block: ProcessedCanDataBlock):
        calculate_rpy_if_possible(processed_block)
        formatted_data_items = [str(processed_block.timestamp), str(processed_block.reception_window_us)]
        for msg in processed_block.get_messages():
            if self.is_filtered(msg):
                fmtr = FORMATTERS[(msg.sensor, msg.data_type)]
                formatted_data_items += fmtr['formatter'](msg.data)
        print(formatter_console(formatted_data_items))
