import threading
import serial
import queue

parity_values = {'None':serial.PARITY_NONE, 'Even':serial.PARITY_EVEN, 'Odd':serial.PARITY_ODD, 'Mark':serial.PARITY_MARK,
                'Space':serial.PARITY_SPACE}

class ComPortProcessor:
    def __init__(self, port, baudrate, bits, sbits, parity):
        self.port = serial.Serial(port=port, baudrate=baudrate, bytesize=int(bits), stopbits=int(sbits), parity=parity_values[parity],
                  timeout=1)
        self.event = threading.Event()
        self.queue = queue.Queue()

    def read_in_thread(self):
        n = 0
        while True:
            if self.event.is_set():
                self.port.close()
                self.event.clear()
                break
            else:
                n+=1
                data = self.port.read(24)
                if data != b'':
                    self.queue.put(data)
                    #print(f'Из потока порта ', data, n)

    def close_port(self):
        self.event.set()

    def start_thread(self):
        thread_port = threading.Thread(target=self.read_in_thread,)
        thread_port.start()