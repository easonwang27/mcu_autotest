import os  
import glob  
import subprocess  
import datetime
import time

KEIL_UV4_PATH = r"C:\Keil_v5\UV4\uv4.exe"

TARGET_NAME = "Debug"
JLINK_PATH = r"D:\SEGGER\SEGGER\JLink_V630d\JLink.exe"
# Set your MCU model (ensure it matches a device supported by J-Link)
MCU_TYPE = "HC32F448"
# Set the J-Link interface and speed (modify based on your hardware)
INTERFACE = "SWD"
SPEED = 4000
  
def compile_keil_project(uvprojx_file, target_name):
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
    # 获取当前工作目录  
    current_directory = os.getcwd()  
  
    # 使用glob查找所有后缀为.uvprojx的文件  
    uvprojx_files = glob.glob(os.path.join(current_directory, '**', '*.uvprojx'), recursive=True)  
  
    # 遍历每个uvprojx文件  
    for uvprojx_file in uvprojx_files:  
        # 编译工程  
        if compile_keil_project(uvprojx_file, TARGET_NAME):
             # Compilation was successful, allowing for further tasks such as generating reports or deploying
            print("Compilation successful. Can proceed with other automation tasks...")
            # Wait for a period to ensure the HEX file has been generated
            wait_time = 5  
            time.sleep(wait_time)
            # 获取工程名（不带后缀）  
            project_name = os.path.splitext(os.path.basename(uvprojx_file))[0]  
            print(f"Processing project: {project_name}") 
             # 假设hex文件在output/debug目录下，并且文件名与工程名相同  
            hex_file_dir = os.path.join(os.path.dirname(uvprojx_file), 'output', 'debug')  
            hex_file_path = os.path.join(hex_file_dir, f"{project_name}.hex")  
            print(f"Processing HEX: {hex_file_path}")
             # 检查hex文件是否存在  
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