import subprocess
import os
import datetime
import time

# Define variables for the paths
KEIL_UV4_PATH = r"C:\Keil_v5\UV4\uv4.exe"
PROJECT_DIRECTORY = r"E:\0-study\5-xhsc\mcu_autotest\timer\projects\ev_hc32f448_lqfp80\examples\timer0\timer0_basetimer\MDK"
PROJECT_NAME = "timer0_basetimer"
PROJECT_EXTENSION = ".uvprojx"
TARGET_NAME = "Debug"
JLINK_PATH = r"D:\SEGGER\SEGGER\JLink_V630d\JLink.exe"
HEX_FILE = r"E:\0-study\5-xhsc\mcu_autotest\timer\projects\ev_hc32f448_lqfp80\examples\timer0\timer0_basetimer\MDK\output\debug\timer0_basetimer.hex"
# Set your MCU model (ensure it matches a device supported by J-Link)
MCU_TYPE = "HC32F448"
# Set the J-Link interface and speed (modify based on your hardware)
INTERFACE = "SWD"
SPEED = 4000

def compile_keil_project(project_path, target_name):
    # Check if uv4.exe exists using the defined variable
    if not os.path.exists(KEIL_UV4_PATH):
        print(f"Error: {KEIL_UV4_PATH} does not exist. Please ensure Keil uVision5 is installed correctly.")
        return False

    # Build the uv4 command using the defined variables
    project_full_path = os.path.join(PROJECT_DIRECTORY, f"{PROJECT_NAME}{PROJECT_EXTENSION}")
    command = [KEIL_UV4_PATH, '-batchbuild', project_full_path]

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
    # Compile the project using the defined variables
    if compile_keil_project(None, TARGET_NAME):  # Pass None for project_path because it's built within the function
        # Compilation was successful, allowing for further tasks such as generating reports or deploying
        print("Compilation successful. Can proceed with other automation tasks...")
        
        # Wait for a period to ensure the HEX file has been generated
        wait_time = 5  
        time.sleep(wait_time)

        # Download the HEX file to the MCU
        if download_hex_with_jlink():
            # Download was successful, allowing for further tasks
            print("HEX file downloaded successfully.")
        else:
            # Download failed, handle the error
            print("Failed to download the HEX file.")
            # Additional error handling code can be placed here (e.g., logging, retries, etc.)
    else:
        # Compilation failed, perform necessary error handling steps
        print("Compilation failed.")
        # Additional error handling code can be placed here (e.g., logging, notifications, etc.)

# Call the main function if this script is executed directly
if __name__ == "__main__":
    main()