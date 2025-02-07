import serial
import sys
import argparse
import struct

from serial.tools import list_ports as tools

cmd = {'MCAL': [0x0D, 0x0A, 0x7E, 0x72, 0x01], 'SETFIL': [0x0D, 0x0A, 0x7E, 0x73,0x05], 'SETFIL0': [0x0D, 0x0A, 0x7E, 0x73,0x01]}

def writeCOM(comport): # отправка сообщения
    j = 0
    for i in createmes():
        comport.write(i.to_bytes())
        j+=1
    print(j)

def createmes():
    l = []
    try:
        l = cmd[namespace.command].copy()
    except:
        print('Error. Command is not defined.')
        print('Available commands:', ', '.join(list(cmd.keys())))
        sys.exit(1)
    if namespace.command == 'SETFIL':
        ar = bytes(struct.pack('>Bf', int(namespace.average),  float(namespace.weight)))
    elif namespace.command == 'MCAL':
        ar = bytes(struct.pack('=B', int(namespace.request)))
    elif namespace.command == 'SETFIL0':
        ar = bytes(struct.pack('>B', int(namespace.average)))
    for i in ar:
        l.append(i)
    l.append(sum(l)%256)
    return(l)


def initcom(comport): # инициализация COM порта
    port = serial.Serial(
        port = comport,
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1)
    return port


def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    parser.add_argument('-c', '--command')
    parser.add_argument('-r', '--request')
    parser.add_argument('-a', '--average')
    parser.add_argument('-w', '--weight')
    return parser

if __name__ == '__main__':
    if '-p' in sys.argv or '--port' in sys.argv:
        ports = [info.device for info in tools.comports()]
        parser = argParser()
        namespace = parser.parse_args(sys.argv[1:])
        port = initcom(namespace.port)
        try:
            writeCOM(port)
        except:
            print('Error. Inactive com port {}.'.format(namespace.port))
            print('Available ports:', ', '.join(ports))
            sys.exit(1)
        data = port.read(1000).hex()
        n = data.find('0d0a7e7303')
        for i in range(n, len(data[n:n+18])+n, 2):
            print(f'0x{data[i:i+2]}', end=' ')
    else:
        print('Error. Enter -p and com port name.')
        sys.exit(1)
