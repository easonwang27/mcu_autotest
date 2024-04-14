# Define a list of keywords to search for  
keywords = ['[PASS]']  
  
# Initialize an empty list to store the found keywords  
found_keywords = []  
  
# Path to the text file  
file_path = r'C:\Users\Administrator\Desktop\run_log.txt'  
  
# Try to open and read the text file  
try:  
    with open(file_path, 'r', encoding='utf-8') as file:  
        # Read the file content line by line  
        for line in file:  
            # Iterate over the list of keywords  
            for keyword in keywords:  
                # Check if the keyword is present in the current line  
                if keyword in line:  
                    # If the keyword is found, add it to the found_keywords list (avoid duplicates)  
                    if keyword not in found_keywords:  
                        found_keywords.append(keyword)  
                        print(f"Keyword found in the file: {keyword}")  
  
    # Check if all keywords have been found  
    if len(found_keywords) == len(keywords):  
        print("All keywords have been found in the file.")  
    else:  
        print("Not all keywords have been found in the file.")  
  
except FileNotFoundError:  
    print(f"The file {file_path} was not found.")  
except Exception as e:  
    print(f"An error occurred: {e}")