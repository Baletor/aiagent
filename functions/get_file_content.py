import os

def get_file_content(working_directory, file_path):
    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
        working = os.path.abspath(working_directory)
        if(not path.startswith(working)):
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if(not os.path.isfile(path)):
            return (f'Error: File not found or is not a regular file: "{file_path}"')
        
        MAX_CHARS = 10000

        with open(path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            extra = f.read(1)
            if extra != '':
                file_content_string += f"\n[...File {file_path} truncated at 10000 characters]\n"

        return file_content_string
    except Exception as e:
        return(f"Error: {e}")