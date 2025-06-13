# from subdirectory.filename import function_name
#from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

#get_file_content tests
results = get_file_content("calculator", "main.py")
print(results)

results1 = get_file_content("calculator", "pkg/calculator.py")
print(results1)

results2 = get_file_content("calculator", "bin/cat")
print(results2)

"""
#get_file_info tests

results = get_files_info("calculator", ".")
print(results)

results1 = get_files_info("calculator", "pkg")
print(results1)

results2 = get_files_info("calculator","/bin")
print(results2)

results3 = get_files_info("calculator", "../")
print(results3)
"""