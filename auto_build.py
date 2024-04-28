import os  
import glob  
import subprocess  
import datetime
import time
import serial_reader  

# Define variables for the paths
KEIL_UV4_PATH = r"C:\Keil_v5\UV4\uv4.exe"
TARGET_NAME = "Debug"
JLINK_PATH = r"D:\SEGGER\SEGGER\JLink_V630d\JLink.exe"
# Set your MCU model (ensure it matches a device supported by J-Link)
MCU_TYPE = "HC32F448"
# Set the J-Link interface and speed (modify based on your hardware)
INTERFACE = "SWD"
SPEED = 4000
  
def compile_keil_project(uvprojx_file, target_name):
    """
    使用Keil uVision5的命令行工具uv4.exe编译Keil工程文件(.uvprojx)
    
    Args:
        uvprojx_file (str): Keil工程文件(.uvprojx)的路径
        target_name (str): 目标名称
    
    Returns:
        bool: 编译成功返回True，否则返回False
    
    """
        # Check if uv4.exe exists using the defined variable
    if not os.path.exists(KEIL_UV4_PATH):
        print(f"Error: {KEIL_UV4_PATH} does not exist. Please ensure Keil uVision5 is installed correctly.")
        return False
    # Build the uv4 command using the defined variables
    command = [KEIL_UV4_PATH, '-batchbuild', uvprojx_file]
    print(f"uvprojx_file project: {uvprojx_file}") 
    try:
        # Start timing the compilation process
        start_time = datetime.datetime.now()
        # Run the command and wait for completion
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Stop timing the compilation process
        end_time = datetime.datetime.now()
        # Output the compilation result
        if result.returncode == 0:
            print(f"Compilation completed successfully. Time taken: {end_time - start_time}")
            #if 1
            # 使用os.path.splitext分割文件名和扩展名  
            _logname, file_extension = os.path.splitext(uvprojx_file)  
            # 替换扩展名为.log  
            logname = _logname + '.log'  
            print(logname)  # 输出新的文件路径
            with open(logname, 'w') as file:  
             # 不写入任何内容，文件将是空的  
                pass 
            try:  
                serial_reader.start_serial_reader( 'COM7', 115200, logname)
            except KeyboardInterrupt:  
             print("Program interrupted by user.")
        #endif
            return True
        else:
            print("Compilation failed. Error details follow:")
            print(result.stderr)
            return False
    except Exception as e:
        # If the command execution fails, print the error details
        print("An exception occurred during compilation:")
        print(e)
        return False


def download_hex_with_jlink(hex_file_path, target_device):
    """
    使用J-Link下载HEX文件到目标设备
    
    Args:
        hex_file_path (str): HEX文件路径
        target_device (str): 目标设备名称
    
    Returns:
        bool: 下载是否成功
    
    """
    # Check if the HEX file exists
    if not os.path.isfile(hex_file_path):
        print(f"Error: The HEX file {hex_file_path} does not exist. Please ensure the compilation was successful.")
        return False

        # Create a script file for J-Link commands
    with open("commands.jlink", "w") as f:
        f.write("erase\n")
        f.write(f"loadfile {hex_file_path}\n")
        f.write("r\n")  # Reset MCU
        f.write("g\n")  # Start executing MCU
        f.write("exit\n")

        # Build the J-Link command line
    cmd = [
        JLINK_PATH,
        "-device", MCU_TYPE,
        "-if", INTERFACE,
        "-speed", str(SPEED),
        "-CommanderScript", "commands.jlink"
    ]

    try:
        # Run the J-Link command and wait for completion
        subprocess.run(cmd, check=True)
        print("The HEX file has been successfully downloaded to the MCU and is running.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing J-Link command: {e}")
        return False
    finally:
        # Delete the temporary script file
        try:
            #os.remove("commands.jlink")
            print("Temporary script file has been deleted.")
        except OSError as e:
            print(f"Error occurred while deleting the temporary script file: {e}")

        # Call the functions to compile the project and download the HEX file
  
  
def main():  
    """
    This function is responsible for compiling and downloading Keil uVision projects (*.uvprojx) 
    from the current working directory. It uses glob to find all files with the specified suffix,
    then traverses each file to compile it using the `compile_keil_project` function. If compilation
    is successful, it waits for a specified period to ensure the HEX file has been generated,
    then processes the HEX file by downloading it to the MCU using the `download_hex_with_jlink` function.
    If any errors occur during the process, appropriate error handling steps are performed.
    
    Args:
        None
    
    Returns:
        None
    
    """
   # port = 'COM7'  # 串口端口号，根据您的实际串口修改  
   # baudrate = 115200  # 波特率，根据您的设备配置修改  
   # data_save_path = 'serial_data.txt'  # 数据保存的文件路径  
    # Get the current working directory
    current_directory = os.getcwd()  
    # Use glob to find all files with the suffix. uvprojx  
    uvprojx_files = glob.glob(os.path.join(current_directory, '**', '*.uvprojx'), recursive=True)  
    # Traverse each uvprojx file 
    for uvprojx_file in uvprojx_files:  
        # Compiling a Project  
        if compile_keil_project(uvprojx_file, TARGET_NAME):
             # Compilation was successful, allowing for further tasks such as generating reports or deploying
            print("Compilation successful. Can proceed with other automation tasks...")
            # Wait for a period to ensure the HEX file has been generated
            wait_time = 5  
            time.sleep(wait_time)
            # Get project name (without suffix)  
            project_name = os.path.splitext(os.path.basename(uvprojx_file))[0]  
            print(f"Processing project: {project_name}") 
             #The hex file is located in the output/debug directory and has the same file name as the project name 
            hex_file_dir = os.path.join(os.path.dirname(uvprojx_file), 'output', 'debug')  
            hex_file_path = os.path.join(hex_file_dir, f"{project_name}.hex")  
            print(f"Processing HEX: {hex_file_path}")
             # Check if the hex file exists  
            if os.path.exists(hex_file_path):      
                print(f"Processing HEX: {hex_file_path}") 
                # Download the HEX file to the MCU
                if download_hex_with_jlink(hex_file_path, MCU_TYPE):
                    # Download was successful, allowing for further tasks
                    print("HEX file downloaded successfully.")
                else:
                # Download failed, handle the error
                    print("Failed to download the HEX file.")
            # Additional error handling code can be placed here (e.g., logging, retries, etc.)  
            else:  
                print(f"Hex file not found for project: {project_name}")  
        else:
            # Compilation failed, perform necessary error handling steps
            print("Compilation failed.")
            # Additional error handling code can be placed here (e.g., logging, notifications, etc.)

    print("Compilation and download completed.")  
if __name__ == "__main__":  
    main()