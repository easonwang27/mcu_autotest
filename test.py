import os
import glob


def main():
    # 获取当前工作目录
    current_directory = os.getcwd()

    # 使用glob查找所有后缀为.uvprojx的文件
    uvprojx_files = glob.glob(os.path.join(current_directory, '**', '*.uvprojx'), recursive=True)

    # 创建一个列表来存储工程名（不带后缀）
    project_names = [os.path.splitext(os.path.basename(file))[0] for file in uvprojx_files]

    # 将工程名写入文本文件
    with open('project_names.txt', 'w') as file:
        for name in project_names:
            file.write(name + '\n')

    print(f"Wrote {len(project_names)} project names to project_names.txt")


if __name__ == "__main__":
    main()