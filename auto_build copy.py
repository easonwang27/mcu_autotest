import subprocess
import os
import datetime

# Define variables for the paths
KEIL_UV4_PATH = r"C:\Keil_v5\UV4\uv4.exe"
PROJECT_DIRECTORY = r"C:\Users\Administrator\Desktop\test\USER"
PROJECT_NAME = "test"
PROJECT_EXTENSION = ".uvprojx"
TARGET_NAME = "Debug"

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

def main():
    # No need to set the project path and target name here since they are already defined as variables

    # Compile the project using the defined variables
    if compile_keil_project(None, TARGET_NAME):  # Pass None for project_path since it's built inside the function
        # Compilation successful, can perform other tasks such as generating reports or deploying
        print("Compilation successful. Can proceed with other automation tasks...")
    else:
        # Compilation failed, can perform error handling steps as needed
        print("Compilation failed.")

# Call the main function to start the compilation process
if __name__ == "__main__":
    main()