import os

def get_files_info(working_directory, directory=None):
    try: 
        path = os.path.abspath(os.path.join(working_directory, directory))
        working = os.path.abspath(working_directory)
        if(not path.startswith(working)):
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if(not os.path.isdir(path)):
            return(f'Error: "{directory}" is not a directory')
        
        info = ""
        contents = os.listdir(path)
        for item in contents:
            isdir = os.path.isdir(os.path.join(path, item))
            size = os.path.getsize(os.path.join(path, item))
            info += (f'- {item}: file_size={size} bytes, is_dir={isdir}\n')
        
        return info
    except Exception as e:
        return(f"Error: {e}")

