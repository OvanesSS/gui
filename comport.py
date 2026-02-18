import threading
import serial
import queue
import struct
import message_constants


parity_values = {'None':serial.PARITY_NONE, 'Even':serial.PARITY_EVEN, 'Odd':serial.PARITY_ODD,
                 'Mark':serial.PARITY_MARK, 'Space':serial.PARITY_SPACE}


class ComPortProcessor:
    def __init__(self, port, baudrate, bits, sbits, parity):
        self.port = serial.Serial(port=port, baudrate=baudrate, bytesize=int(bits), stopbits=int(sbits),
                                  parity=parity_values[parity], timeout=1)
        self.event = threading.Event()
        self.queue = queue.Queue()
        self.recMessage = ''
        self.sizeMessage = None
        self.checksum = None

    def read_in_thread(self):
        while True:
            if self.event.is_set():
                self.port.close()
                self.event.clear()
                break
            else:
                if not self.recMessage:
                    data = self.port.read(5)
                    if data != b'' and data[:3] == message_constants.HEADER:
                        self.checksum = sum(data)
                        self.sizeMessage = data[4]
                        if data[3] == message_constants.DORIENT_ID: self.recMessage = message_constants.DORIENT
                        if data[3] == message_constants.SETFIL_ID: self.recMessage = message_constants.SETFIL
                elif self.recMessage == message_constants.DORIENT:
                    data = self.port.read(self.sizeMessage+1)
                    self.checksum = (self.checksum+sum(data[:self.sizeMessage]))%256
                    if self.checksum == data[-1]:
                        roll, pitch, azimuth, *accelerations = struct.unpack(message_constants.DORIENT_FORMAT, data[:-1])
                        self.recMessage += (f' Roll = {roll*message_constants.SENSITIVITY:.2f}, '
                                            f'Pitch = {pitch*message_constants.SENSITIVITY:.2f}, '
                                            f'Azimuth = {azimuth*message_constants.SENSITIVITY:.2f}.')
                        self.queue.put(self.recMessage)
                    self.recMessage = ''
                    self.sizeMessage = None
                elif self.recMessage == message_constants.SETFIL:
                    data = self.port.read(self.sizeMessage + 1)
                    self.checksum = (self.checksum+sum(data[:self.sizeMessage]))%256
                    if self.checksum == data[-1]:
                        average, coefficient, *others = struct.unpack(message_constants.SETFIL_FORMAT, data[:-1])
                        self.recMessage += f' Average = {average}, Coefficient = {coefficient/1000}'
                        self.queue.put(self.recMessage)
                    self.recMessage = ''
                    self.sizeMessage = None




    def close_port(self):
        self.event.set()

    def start_thread(self):
        thread_port = threading.Thread(target=self.read_in_thread,)
        thread_port.start()

    def write(self, data):
        self.message = struct.pack(message_constants.SETFIL_ANS_FORMAT, *message_constants.HEADER_TO_BYTES,
                               message_constants.SETFIL_ID, message_constants.SETFIL_COUNT, *data)
        self.message += (sum(self.message)%256).to_bytes()
        print(self.message)
        self.port.write(self.message)
