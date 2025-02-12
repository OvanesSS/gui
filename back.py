import threading

import serial
import queue
import sys
import struct
from typing import Optional

cmd = {'MCAL': [0x0D, 0x0A, 0x7E, 0x72, 0x01], 'SETFIL': [0x0D, 0x0A, 0x7E, 0x73, 0x05],
       'SETFIL0': [0x0D, 0x0A, 0x7E, 0x73, 0x01]}
parity_values = {'None':serial.PARITY_NONE, 'Even':serial.PARITY_EVEN, 'Odd':serial.PARITY_ODD, 'Mark':serial.PARITY_MARK,
          'Space':serial.PARITY_SPACE}


class SerialPort:
    def __init__(self, port: str, baudrate: int, bits: int, sbits: int, parity: str, data_queue: queue.Queue) -> None:
        self.port = port
        self.baudrate = baudrate
        self.bits = bits
        self.sbits = sbits
        self.parity = parity
        self.data_queue = data_queue
        self.running: bool = False
        self.serial: Optional[serial.Serial] = None
    def start(self) -> None:
        self.serial = serial.Serial(self.port, self.baudrate, self.bits, self.sbits, parity_values[self.parity],
                                    timeout=1)
        self.running = True
        self.thred = threading.Thread(target = self.read_serial)
        self.thread.start()
    def stop(self) -> None:
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        if self.serial is not None:
            self.serial.close()
    def read_serial(self) -> None:
        while self.running:
            if self.serail.in_waiting > 0:
                data = self.serial.read(24)
                self.data_queue.put(data)
    def write_serial(selfself, data) -> None:
        if self.serial is not None and sekf.serial.is_open:
            self.serial.write(data)













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


