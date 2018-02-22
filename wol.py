import sys
import socket
import struct
import argparse

BROADCAST_ADDR='255.255.255.255'
DEFAULT_PORT = 9

def wake_on_lan(macs, ip=BROADCAST_ADDR, port=DEFAULT_PORT):
    mac_address = "98:90:96:dc:52:f6"
    packets = []
    packets.append(create_magic_packet(mac_address))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect((ip, port))
    for packet in packets:
        sock.send(packet)
    sock.close()

def create_magic_packet(macaddress):
    if len(macaddress)==12:
        pass
    elif len(macaddress) == 12+5:
        macaddress = macaddress.replace(macaddress[2],'')
    else:
        raise ValueError('Invalid MAC address')

    data = ''.join(['FFFFFFFFFFFF', macaddress*16])
    send_data = b''

    for i in range(0, len(data), 2):
        send_data = b''.join([send_data, struct.pack('B', int(data[i:i+2], 16))])

    return send_data

def run(argv):
    parser = argparse.ArgumentParser( description='Wake on lan tool')
    parser.add_argument(
        'macs',
        metavar='mac address',
        nargs='+',
        help='The mac addresses or of the computers you are trying to wake.')
    parser.add_argument(
        '-i',
        metavar='ip',
        default=BROADCAST_ADDR,
        help='The ip address of the host to send the magic packet to.'
             ' (default {})'.format(BROADCAST_ADDR))
    parser.add_argument(
        '-p',
        metavar='port',
        type=int,
        default=DEFAULT_PORT,
        help='The port of the host to send the magic packet to (default 9)')
    args = parser.parse_args(argv)
    wake_on_lan(args.macs, ip=args.i, port=args.p)

if __name__ == "__main__":
    run(sys.argv)