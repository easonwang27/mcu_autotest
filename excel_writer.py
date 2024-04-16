import re  
import openpyxl  
from openpyxl.styles import Alignment  
  
def write_result_to_excel(log_file_path, excel_file_path, keyword):  
    """  
    从日志文件中查找关键词对应的测试结果，并写入Excel文件的相应单元格中。  
      
    :param log_file_path: 日志文件的路径  
    :param excel_file_path: Excel文件的路径  
    :param keyword: 要查找的关键词  
    :return: None  
    """  
    try:  
        # 读取日志文件内容  
        with open(log_file_path, 'r') as log_file:  
            log_content = log_file.read()  
          
        # 查找关键词后的结果  
        match = re.search(f'{re.escape(keyword)}\\s+test\\s+result\\s+is:\\s+(PASS|FAIL)', log_content)  
        result = match.group(1) if match else None  
          
        # 加载Excel工作簿  
        workbook = openpyxl.load_workbook(excel_file_path)  
        sheet = workbook.active  
          
        # 遍历Excel文件中的每一行来查找与关键词相关的单元格  
        for row in sheet.iter_rows(min_row=1, values_only=False):  
            for cell in row:  
                if cell.value == keyword:  
                    # 找到关键词，获取其所在列的下一个单元格并写入结果  
                    result_cell = cell.offset(column=1)  
                    result_cell.value = result  
                      
                    # 设置单元格内容的对齐方式为居中  
                    alignment = Alignment(horizontal='center', vertical='center')  
                    result_cell.alignment = alignment  
                      
                    break  # 找到后退出内部循环  
            if result is not None:  
                break  # 如果已经找到结果，退出外部循环  
          
        # 保存Excel工作簿  
        workbook.save(excel_file_path)  
    except PermissionError:  
        print("Excel文件正在使用中，请确认后关闭Excel并重新运行此脚本。")  
    except Exception as e:  
        print(f"发生错误：{e}，请检查文件路径或Excel文件是否已损坏。")  
  
# 示例用法  
# write_result_to_excel('test_log.txt', 'test_results.xlsx', 'TIMER_TEST_001')