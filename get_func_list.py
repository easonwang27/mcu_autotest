import os
import glob
import subprocess
import logging
from datetime import datetime

KEIL_UV4_PATH = r"C:\Keil_v5\UV4\uv4.exe"

# 配置日志记录器，这里先不设置文件名，稍后在main函数中设置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def compile_mdk_project(project_file, log_filename):
    # 假设编译命令是 'uvprojx' 并且它在系统的PATH中
    # 你可能需要替换成实际的编译命令和参数
    compiler_command = [KEIL_UV4_PATH, '-batchbuild', project_file]
    try:
        # 在编译之前打印工程名
        project_name = os.path.splitext(os.path.basename(project_file))[0]

        # 设置日志处理器以写入指定的日志文件
        log_handler = logging.FileHandler(log_filename)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(log_handler)

        # 运行编译命令并等待其完成
        subprocess.run(compiler_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Project {project_name} compiled successfully.")
        logging.info(f"Project {project_name} compiled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to compile project {project_name}: {e}")
        logging.error(f"Failed to compile project {project_name}: {e}")
        # 如果需要，也可以将错误信息写入日志
        # logging.error(e.output.decode('utf-8'))
    finally:
        # 移除日志处理器，避免在连续调用compile_mdk_project时产生重复的记录
        logging.getLogger().removeHandler(log_handler)
        log_handler.close()


def main():
    current_directory = os.getcwd()  # 获取当前工作目录
    # 使用glob查找所有后缀为.uvprojx的文件
    uvprojx_files = glob.glob(os.path.join(current_directory, '**', '*.uvprojx'), recursive=True)

    # 获取当前时间并格式化，用于日志文件名
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"compile_log_{timestamp}.txt"

    # 对每个找到的.uvprojx文件，调用编译函数
    for uvprojx_file in uvprojx_files:
        # 调用编译函数并传入日志文件名
        compile_mdk_project(uvprojx_file, log_filename)


if __name__ == "__main__":
    main()