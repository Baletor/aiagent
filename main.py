import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }
    working_directory = "./calculator"
    function_call_part.args['working_directory'] = working_directory
    function_name = function_call_part.name
    if function_name not in ["get_files_info", "get_file_content", "write_file", "run_python_file"]:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    actual_function = function_map[function_name]

    function_result = actual_function(**function_call_part.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model_name = 'gemini-2.0-flash-001'

if len(sys.argv) < 2 :
    print('No input received')
    exit(1)
user_prompt = sys.argv[1]

messages = [ 
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists contents of file specified, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to file  from, relative to the working directory. If not provided, file in the working directory itself.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs python file specified, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path to python file, relative to the working directory. If not provided, python file in the working directory itself.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write file in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to write file to, relative to the working directory. If not provided, write file in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to write or modify in the file."
            )
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
verbose = False
if '--verbose' in sys.argv:
    verbose = True
response = client.models.generate_content(model=model_name,contents=messages, config=config,)
if response.function_calls:
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Function call failed - no response")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
else:
    print(response.text)
if '--verbose' in sys.argv: 
    print("User prompt:", user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)