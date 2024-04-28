# main_script.py  
import serial_reader  
  
if __name__ == "__main__":  
    port = 'COM7'  # 串口端口号，根据您的实际串口修改  
    baudrate = 115200  # 波特率，根据您的设备配置修改  
    data_save_path = 'serial_data.txt'  # 数据保存的文件路径  
  
    try:  
        serial_reader.start_serial_reader(port, baudrate, data_save_path)  
    except KeyboardInterrupt:  
        print("Program interrupted by user.")