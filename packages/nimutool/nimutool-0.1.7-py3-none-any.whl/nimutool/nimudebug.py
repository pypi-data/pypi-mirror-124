import argparse
from nimutool import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for reading nimu data from CAN bus')
    parser.add_argument('--trace-file', type=str, help='PCAN-View generated trace file')
    parser.add_argument('--hex2nimu', action='store_true', help='Convert PILogger can2hex output')
    parser.add_argument('--can-adapter', default='pcan', help='Can adapter to use, see options from python-can documentation')
    parser.add_argument('--can-channel', default='PCAN_USBBUS1', help='Can adapter channel to use, see options from python-can documentation')
    args = parser.parse_args()

    if args.hex2nimu:
        bus = PiLoggerCanBusReader()
    elif args.trace_file:
        bus = TraceFileCanBusReader(args.trace_file)
    else:
        bus = CanBusReader(can.interface.Bus(bustype=args.can_adapter, channel=args.can_channel, bitrate=1000000))

    line = {}
    for msg in bus:
        #print(msg)
        if (msg.msg_id & 0xff0) == 0x3d0:
            nodeid = msg.msg_id & 0x00f
            if nodeid not in line:
                line[nodeid] = ''
            line[nodeid] += msg.data.decode(errors="replace")
            lines = line[nodeid].split('\n')
            if len(lines) > 1:
                print(f'{nodeid}: {lines[0]}')
                line[nodeid] = '\n'.join(lines[1:])