from dotenv import load_dotenv
import os
from os import environ
from openai import OpenAI
from icecream import ic

# load our environment file
load_dotenv(dotenv_path="../.env")

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

from typing import List, Dict, Any

open_ai_models = ['text-search-babbage-doc-001', 'gpt-3.5-turbo-16k-0613', 'gpt-3.5-turbo-0613', 'curie-search-query', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'text-search-babbage-query-001', 'babbage', 'babbage-search-query', 'text-babbage-001', 'fanw-json-eval', 'whisper-1', 'text-similarity-davinci-001', 'gpt-4', 'davinci', 'davinci-similarity', 'code-davinci-edit-001', 'curie-similarity', 'babbage-search-document', 'curie-instruct-beta', 'text-search-ada-doc-001', 'davinci-instruct-beta', 'text-similarity-babbage-001', 'text-search-davinci-doc-001', 'gpt-4-0314', 'babbage-similarity', 'davinci-search-query', 'text-similarity-curie-001', 'text-davinci-001', 'text-search-davinci-query-001', 'ada-search-document', 'ada-code-search-code', 'babbage-002', 'gpt-4-0613', 'davinci-002', 'davinci-search-document', 'curie-search-document', 'babbage-code-search-code', 'text-search-ada-query-001', 'code-search-ada-text-001', 'babbage-code-search-text', 'code-search-babbage-code-001', 'ada-search-query', 'ada-code-search-text', 'text-search-curie-query-001', 'text-davinci-002', 'text-embedding-ada-002', 'text-davinci-edit-001', 'code-search-babbage-text-001', 'gpt-3.5-turbo-instruct-0914', 'ada', 'text-ada-001', 'ada-similarity', 'code-search-ada-code-001', 'text-similarity-ada-001', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo-instruct', 'text-search-curie-doc-001', 'text-davinci-003', 'text-curie-001', 'curie']

def is_valid_message(message: Dict[str, Any]) -> bool:
    # Check if the message dictionary has 'role' and 'content' keys of the correct types.
    if isinstance(message, dict) and 'role' in message and 'content' in message:
        if isinstance(message['role'], str) and isinstance(message['content'], str):
            return True
    return False

def are_valid_messages(messages: List[Dict[str, Any]]) -> bool:

    return all(is_valid_message(message) for message in messages)

def simple_chat(messages: List[Dict[str, Any]], model: str = 'gpt-3.5-turbo', temperature: float = 0.9, max_tokens: int = 1024) -> str:

    if not messages:
        raise ValueError("Input messages list cannot be empty.")

    # Check if all messages are in the correct format.
    if not are_valid_messages(messages):
        raise ValueError("Input messages must be in the format [{'role': str, 'content': str}, ...]")

    # Send the messages to OpenAI and get the response
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature,
    max_tokens=max_tokens)

    return response


def get_file_contents(file_path: str, return_as_list: bool = False):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()

        # Filter out lines starting with # and blank lines
        lines = [line.strip() for line in lines if not line.startswith('#') and line.strip()]

        # Join all lines into a single string or return as a list
        if return_as_list:
            return lines
        else:
            return ''.join(lines)


def write_response_to_file(response, file_path: str):
    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Write the content to the file
        file.write(response.choices[0].message.content)

def set_local_directory():
    import os
    import inspect

    # Get the caller's frame
    caller_frame = inspect.stack()[1]
    
    # Get the path of the caller's script
    caller_script_path = caller_frame.filename
    
    # Get the directory of the caller's script
    caller_script_directory = os.path.dirname(os.path.realpath(caller_script_path))
    
    # Change the current working directory to the directory of the caller's script
    os.chdir(caller_script_directory)

def append_line_to_file(file_path: str, line: str):
    # Open the file in append mode
    with open(file_path, 'a') as file:
        # Append the line to the file
        file.write(line + '\n')

def get_file_size(file_path: str) -> int:
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
    return len(file_bytes)


def get_file_lines(file_path: str) -> int:
    with open(file_path, 'rb') as file:
        lines = file.readlines()
    return len(lines)

