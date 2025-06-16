import os

def write_file(working_directory, file_path, content):
    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
        working = os.path.abspath(working_directory)
        directory_part = os.path.split(path)[0]

        """
        print(f"file_path: {file_path}")
        print(f"path: {path}")
        print(f"directory_part: {directory_part}")
        print(f"directory_part exists: {os.path.exists(directory_part)}")
        """
        
        if(not path.startswith(working)):
            return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if directory_part and not os.path.exists(directory_part):
            os.makedirs(directory_part)

        with open(path, "w") as f:
            f.write(content)

        return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
        

    except Exception as e:
        return(f"Error: {e}")
    

    #working_path = os.path.abspath(os.path.join(working_directory, directory_part))