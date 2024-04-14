import subprocess
import os
import datetime

KEIL_UV4_PATH = r"C:\Keil_v5\UV4\uv4.exe"

def compile_keil_project(project_path, target_name):
    # 确保 uv4.exe 的路径是正确的，这取决于你的 Keil 安装位置
    uv4_path = r"C:\Keil_v5\UV4\uv4.exe"

    # 检查 uv4.exe 是否存在
    if not os.path.exists(uv4_path):
        print(f"错误: {uv4_path} 不存在。请确保 Keil uVision5 已正确安装。")
        return False

        # 构建 uv4 命令
    command = [uv4_path, '-batchbuild', project_path]
    #command = [uv4_path, '-batchbuild', project_path + ' ' + target_name]

    # 运行命令并等待完成
    try:
        start_time = datetime.datetime.now()
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        end_time = datetime.datetime.now()

        # 输出编译结果
        if result.returncode == 0:
            print(f"编译完成，没有错误。用时: {end_time - start_time}")
            return True
        else:
            print("编译失败，错误信息如下：")
            print(result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，打印错误信息
        print("编译失败，错误信息如下：")
        print(e.stderr)
        return False


def main():
    # 设置项目路径和目标名称
    project_path = r"C:\Users\Administrator\Desktop\test\USER\test.uvprojx"
    target_name = "Debug"

    # 编译项目
    if compile_keil_project(project_path, target_name):
        # 编译成功，可以执行其他任务，比如生成报告或部署
        print("编译成功，可以执行其他自动化任务...")
    else:
        # 编译失败，可以根据需要执行一些错误处理步骤
        print("编译失败，请检查错误信息并手动干预。")

    # 运行主函数


if __name__ == "__main__":
    main()