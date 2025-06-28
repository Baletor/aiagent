import os
import subprocess

def run_python_file(working_directory, file_path):
    try: 
        path = os.path.abspath(os.path.join(working_directory, file_path))
        working = os.path.abspath(working_directory)
        #directory_part = os.path.split(path)[0]
        if(not path.startswith(working)):
            return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.exists(path):
            return (f'Error: File "{file_path}" not found.')
        if not path.endswith(".py"):
            return (f'Error: "{file_path}" is not a Python file.')
        
        results = subprocess.run(['python3', file_path],capture_output=True, cwd = working, timeout = 30)

        if results.stdout == b"" and results.stderr == b"" and results.returncode == 0:
             return "No output produced." 

        output_parts = [] 

        if results.stdout:
            output_parts.append("STDOUT:")
            output_parts.append((results.stdout).decode(encoding='UTF-8',errors='strict'))

        if results.stderr:    
            output_parts.append("STDERR:")
            output_parts.append((results.stderr).decode(encoding='UTF-8',errors='strict'))

        if results.returncode != 0:
            output_parts.append(f"Process exited with code {results.returncode}") 

        final_output = "\n".join(output_parts)

        return final_output 

    except Exception as e:
        return(f"Error: executing Python file: {e}")