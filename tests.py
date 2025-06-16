# from subdirectory.filename import function_name
#from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

results = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(results)

results1 = write_file("calculator", "pkg/morelorem.txt", "lorem ispum dolor sit amet")
print(results1)

results2 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(results2)

"""
#get_file_content tests
results = get_file_content("calculator", "main.py")
print(results)

results1 = get_file_content("calculator", "pkg/calculator.py")
print(results1)

results2 = get_file_content("calculator", "bin/cat")
print(results2)
"""

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