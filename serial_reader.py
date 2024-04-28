import serial  
import time  
import threading  
  
class SerialReaderThread(threading.Thread):  
    def __init__(self, port, baudrate, data_save_path):  
        super().__init__()  
        self.port = port  
        self.baudrate = baudrate  
        self.data_save_path = data_save_path  
        self.no_data_timeout = 70  # 设置无数据读取的超时时间为70秒  
        self.running = False  
        self.ser = None  
  
    def run(self):  
        try:  
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)  
            self.running = True  
            print(f"Serial port {self.port} opened successfully in thread.")  
  
            with open(self.data_save_path, 'a', encoding='utf-8') as data_file:  
                self.read_data(data_file)  
  
        except serial.SerialException as e:  
            print(f"Error opening serial port {self.port} in thread: {e}")  
        except Exception as e:  
            print(f"Unexpected error occurred while opening serial port {self.port} in thread: {e}")  
        finally:  
            self.close()  
            self.running = False  
  
    def read_data(self, data_file):  
        last_read_time = time.time()  
        while self.running:  
            if self.ser.in_waiting:  
                data = self.ser.readline().decode().strip()  
                print(f"Received data: {data}")  
                data_file.write(data + '\n')  
                last_read_time = time.time()  
            else:  
                if time.time() - last_read_time > self.no_data_timeout:  
                    print("No data received for 70 seconds. Exiting thread...")  
                    break  
            time.sleep(0.1)  
  
    def close(self):  
        if self.ser and self.ser.isOpen():  
            self.ser.close()  
  
    def stop(self):  
        self.running = False  
  
def start_serial_reader(port, baudrate, data_save_path):  
    reader_thread = SerialReaderThread(port, baudrate, data_save_path)  
    reader_thread.start()  
    return reader_thread 