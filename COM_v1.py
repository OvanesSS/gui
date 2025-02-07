import serial
import sys
import argparse

from serial.tools import list_ports as tools


def writeCOM(comport): # отправка сообщения
    port = initcom(comport)
    j = 0
    for i in messagePackaging(splittingMeas(namespace)):
        port.write(i.to_bytes())
        j+=1
    print(j)

def initcom(comport): # инициализация COM порта
    port = serial.Serial(
        port = comport,
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1)
    return port

def serialPorts(): # список доступных COM портов
    '''
    <!>: У Serial есть функция поиска портов
    '''
    return [info.device for info in tools.comports()]

def messagePackaging(arg): # создание списка из элементов сообщения
    sum = 0x0117 # сумма элементов заголовка
    res = [0x0D, 0x0A, 0x7E, 0x70, 0x12]
    for i in arg:
        res.append(i)
        sum += i
    res.append(sum % 256)
    return res

def splittingMeas(obj): # разделение значений на два байта, дополнение до стандартного сообщения
    res = []
    for key in obj.__dict__.keys():
        if key != 'port':
            if int(obj.__dict__[key]) < 0xFFFF:
                if key == 'right':
                    res.extend([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
                res.append(int(obj.__dict__[key]) >> 8)
                res.append(int(obj.__dict__[key]) & 0xFF)
            else:
                print('Error. Going beyond the range of acceptable values of the \'%s\' parameter. Enter a number from 0 to 65535' % key)
                sys.exit(1)
    return res

def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    parser.add_argument('-r', '--roll', default = 0xDA00)
    parser.add_argument('-pt', '--pitch', default = 0x4305)
    parser.add_argument('-a', '--azimuth', default = 0x488A)
    parser.add_argument('-rg', '--right', default = 0x8301, help = 'Magnetometer reading in the local-coordinates rightward direction')
    parser.add_argument('-f', '--forward', default = 0x6BFA, help = 'Magnetometer reading in the local-coordinates forward direction')
    parser.add_argument('-u', '--up', default = 0x16F3, help = 'Magnetometer reading in the local-coordinates upward direction')
    return parser

if __name__ == '__main__':
    if '-p' in sys.argv or '--port' in sys.argv:
        ports = serialPorts()
        parser = argParser()
        namespace = parser.parse_args(sys.argv[1:])
        print(type(namespace))

        # Принято делать через исключения
        # try:
        #     writeCOM(namespace.port)
        # except:
        #     print('Error. Inactive com port {}.'.format(namespace.port))
        #     print('Available ports:', ', '.join(ports))
        #     sys.exit(1)


        if namespace.port in ports:
            writeCOM(namespace.port)
        else:
            print('Error. Inactive com port {}.'.format(namespace.port))
            print('Available ports:', ', '.join(ports))
            sys.exit(1)

    else:
        print('Error. Enter -p and com port name.')
        sys.exit(1)
