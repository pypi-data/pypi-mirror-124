from abc import ABC, abstractmethod
import can
import datetime
import re
import sys
import base64
from .can_message import *

class CanBusReaderBase(ABC):

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    def stop(self):
        pass

class TraceFileCanBusReader(CanBusReaderBase):
    REGEX = re.compile(r'\s*(\d+)\)\s+(\d+\.\d+)\s+([A-Za-z]+)\s+([A-F0-9]{4})\s+(\d)\s+([A-F0-9\s]+)')

    def __init__(self, trace_file):
        self.n = 0
        with open(trace_file) as f:
            self.msgs = [self._parse_line(line) for line in f]
            self.msgs = list(filter(lambda x: x is not None, self.msgs))
    
    def _parse_line(self, line):
        if line.startswith(';'):  # comment
            return
        m = TraceFileCanBusReader.REGEX.match(line)
        if m:
            seq = m.group(1)
            time_ms = float(m.group(2)) / 1000
            direction = m.group(3)
            canid = int(m.group(4), base=16)
            length = m.group(5)
            data = bytes.fromhex(m.group(6))
            return CanMessage(time_ms, canid, data, False)
        else:
            print("no find", line)

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < len(self.msgs):
            msg = self.msgs[self.n]
            self.n += 1
            return msg
        else:
            raise StopIteration

class PiLoggerCanBusReader(CanBusReaderBase):
   
    def __init__(self):
        self.msgs =  [self._parse_line(line) for line in sys.stdin.readlines()]
        self.n = 0

    def _parse_line(self, line):
        items = [item.strip('"\n') for item in line.split(';')]
        timestamp, canid, extended, _, data = items
        canid = int(canid, base=16)
        data = bytes.fromhex(data)
        timestamp = (datetime.datetime.strptime(timestamp, '%H:%M:%S.%f') - datetime.datetime(1900,1,1)).total_seconds()
        return CanMessage(timestamp, canid, data, extended == 'Ext')

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < len(self.msgs):
            msg = self.msgs[self.n]
            self.n += 1
            return msg
        else:
            raise StopIteration

class CSVCanBusReader(CanBusReaderBase):

    def __init__(self, csv_file):
        self.n = 0
        with open(csv_file) as f:
            next(f)  # skip header
            self.msgs = [self._parse_line(line) for line in f]
    
    def _parse_line(self, line):
        timestamp, arbitration_id, extended, remote, error, dlc, data = line.split(',')
        arbitration_id = int(arbitration_id, base=16)
        data = base64.b64decode(data)
        return CanMessage(float(timestamp), arbitration_id, data, extended == '1')

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < len(self.msgs):
            msg = self.msgs[self.n]
            self.n += 1
            return msg
        else:
            raise StopIteration

class CanBusReader(CanBusReaderBase):
   
    def __init__(self, bus: can.interface.Bus):
        self.bus = bus

    def __iter__(self):
        return self

    def __next__(self):
        for msg in self.bus:
            return CanMessage(msg.timestamp, int(msg.arbitration_id), msg.data, msg.is_extended_id)

    def stop(self):
        self.bus.shutdown()
