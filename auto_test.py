import subprocess  
import os  
import time  
  
# Keil uVision5和JLinkExe的路径设置  
KEIL_UV5_PATH = r"C:\Keil_v5\UV5\uv5.exe"  
JLINK_PATH = r"C:\Program Files (x86)\SEGGER\JLink_V630d\JLink.exe"  
  
# Keil项目目录和文件设置  
PROJECT_DIRECTORY = r"C:\Users\Administrator\Desktop\test\USER"  
PROJECT_NAME = "test"  
PROJECT_EXTENSION = ".uvprojx"  
TARGET_NAME = "Debug"  
HEX_FILE = os.path.join(PROJECT_DIRECTORY, "Obj", TARGET_NAME, f"{PROJECT_NAME}.hex")  
  
# MCU型号和J-Link设置  
MCU_TYPE = "HC32F448"  
INTERFACE = "SWD"  
SPEED = 4000  
  
def compile_keil_project(project_path, target_name):  
    # 构建Keil命令行参数  
    cmd = [  
        KEIL_UV5_PATH,  
        "-build",  
        os.path.join(project_path, f"{target_name}{PROJECT_EXTENSION}")  
    ]  
      
    # 调用Keil命令行工具进行编译  
    try:  
        subprocess.run(cmd, check=True)  
        print("Keil project has been successfully compiled.")  
        return True  
    except subprocess.CalledProcessError as e:  
        print(f"Error occurred while compiling the Keil project: {e}")  
        return False  
def download_hex_with_jlink():
    # Check if the HEX file exists
    if not os.path.isfile(HEX_FILE):
        print(f"Error: The HEX file {HEX_FILE} does not exist. Please ensure the compilation was successful.")
        return False

        # Create a script file for J-Link commands
    with open("commands.jlink", "w") as f:
        f.write("erase\n")
        f.write(f"loadfile {HEX_FILE}\n")
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
    # 编译Keil项目  
    if compile_keil_project(PROJECT_DIRECTORY, TARGET_NAME):  
        # 等待一段时间以确保HEX文件已生成  
        time.sleep(5)  # 根据实际情况调整等待时间  
          
        # 下载HEX文件到MCU  
        if download_hex_with_jlink():  
            # 下载成功，可以执行其他任务  
            pass  
        else:  
            # 下载失败，处理错误  
            pass  
    else:  
        # 编译失败，处理错误  
        pass  
  
# 等待用户按键后退出  
input("Press Enter to exit...")