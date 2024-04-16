import re  
import openpyxl
from openpyxl.styles import Alignment
  
# Log file path
log_file_path = 'run_log.txt'  
# Excel file path
excel_file_path = 'test_result.xlsx'  
  
# Open the log file and read its contents
with open(log_file_path, 'r') as log_file:  
    log_content = log_file.read()  
  
# keyboard
keyword = 'TIMER_TEST_001'

# The result of using regular expressions to find keywords (PASS or FAIL)
match = re.search(f'{re.escape(keyword)}\\s+test\\s+result\\s+is:\\s+(PASS|FAIL)', log_content)

# get result
if match:  
    result = match.group(1)  
else:  
    result = None
print(result)

try:
    workbook = openpyxl.load_workbook(excel_file_path)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=1, values_only=False):
        for cell in row:
            if cell.value == keyword:
                result_cell = cell.offset(column=1)
                result_cell.value = result
                alignment = Alignment(horizontal='center', vertical='center')
                result_cell.alignment = alignment
                break  #
        if result is not None:
            break  #

    # save file
    workbook.save(excel_file_path)
except PermissionError:
    print("The Excel file is currently in use. Please confirm and close Excel and run this script again.")
except Exception as e:
    # 捕获其他可能发生的异常
    print(f"An error occurred: {e}, please check if the file path or Excel file is damaged.")