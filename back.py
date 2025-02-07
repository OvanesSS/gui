import serial
import sys
import struct

cmd = {'MCAL': [0x0D, 0x0A, 0x7E, 0x72, 0x01], 'SETFIL': [0x0D, 0x0A, 0x7E, 0x73, 0x05],
       'SETFIL0': [0x0D, 0x0A, 0x7E, 0x73, 0x01]}
def createmes(average, coef, command):
    l = []
    try:
        l = cmd[command].copy()
    except:
        print('Error. Command is not defined.')
        print('Available commands:', ', '.join(list(cmd.keys())))
        sys.exit(1)
    if command == 'SETFIL':
        ar = bytes(struct.pack('>Bf', int(average),  float(coef)))
    elif command == 'MCAL':
        ar = bytes(struct.pack('=B', int(request)))
    elif command == 'SETFIL0':
        ar = bytes(struct.pack('>B', int(average)))
    for i in ar:
        l.append(i)
    l.append(sum(l)%256)
    return(l)


def initcom(comport, baudrate, parity, sbits, bits): # инициализация COM порта
    port = serial.Serial(
        port=comport,
        baudrate=baudrate,
        parity=parity,
        stopbits=sbits,
        bytesize=bits,
        timeout=1)
    return port