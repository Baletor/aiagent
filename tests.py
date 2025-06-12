# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info

results = get_files_info("calculator", ".")
print(results)

results1 = get_files_info("calculator", "pkg")
print(results1)

results2 = get_files_info("calculator","/bin")
print(results2)

results3 = get_files_info("calculator", "../")
print(results3)