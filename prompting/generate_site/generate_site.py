from decouple import config
import os

openai_api_key = config('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = openai_api_key

from workshop_common import set_local_directory, simple_chat, get_file_contents, write_response_to_file, get_file_size, execute_prompt
from icecream import ic
import argparse
import re
import ast
    
if __name__ == "__main__":
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Customize user message and run story response")
    parser.add_argument('--temperature', type=float, default=0, help="Temperature for simple_chat function")
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help="Model for simple_chat function")
    parser.add_argument('--max_tokens', type=int, default=2000, help="Max tokens for simple_chat function")

    # Add command-line arguments for file paths
    parser.add_argument('--system_prompt_file', type=str, default='system-prompt.txt', help="File containing system message content")
    parser.add_argument('--user_prompt_file', type=str, default=f'user-prompt.txt', help="File containing user message content")
    parser.add_argument('--user_prompt_list_file', type=str, default='user-prompt-list.txt', help="File containing user message content")
    parser.add_argument('--user_prompt_page_file', type=str, default='user-prompt-page.txt', help="File containing user message content")
    parser.add_argument('--response_file', help="File to write the response to", default=f'results.txt')
    parser.add_argument('--pages', help="The number of pages to generate", default=25)
    parser.add_argument('--company', help="The name of the company to use", default='Acme Corporation')

    args = parser.parse_args()

    # Set local directory, initialize simple_chat_args

    set_local_directory()
    chat_args = {
        'temperature': args.temperature,
        'model': args.model,
        'max_tokens': args.max_tokens
    }

    user_prompt_args={
        'pages': args.pages,
        'company': args.company,
    } 

    # # use the information from our files to customize the user message
    # user_message = get_file_contents(args.user_prompt_file)
    user_list_message = get_file_contents(args.user_prompt_list_file)
    user_page_message = get_file_contents(args.user_prompt_page_file)
    system_message = get_file_contents(args.system_prompt_file)

    prompt_response = execute_prompt(user_prompt=user_list_message, 
                                    user_prompt_vars=user_prompt_args, 
                                    system_prompt=system_message, 
                                    chat_args=chat_args)

    # Write response to a file
    write_response_to_file(file_path=args.response_file, response=prompt_response)

    # Turn the response back into a list
    response_text = prompt_response.choices[0].message.content
    extracted_list = re.search(r'\[.*\]', response_text, flags=re.DOTALL)

    if extracted_list:
        extracted_list = extracted_list.group()

    page_list = ast.literal_eval(extracted_list)

    def convert_to_filename(text):
        # Remove special characters and spaces, convert to lowercase
        clean_text = re.sub(r'[^a-zA-Z0-9 ]', '', text).lower()
        
        # Replace spaces with underscores
        clean_text = clean_text.replace(' ', '_')
        
        # Add .txt extension
        filename = clean_text + '.txt'
        
        return filename


    # generate individual pages
    for page in page_list:

        user_prompt_args['subject'] = page

        page_response = execute_prompt(user_prompt=user_page_message, 
                                    user_prompt_vars=user_prompt_args, 
                                    system_prompt=system_message, 
                                    chat_args=chat_args)
        
        page_as_file = convert_to_filename(page)
        filename = f"site/{page_as_file}"
        
        write_response_to_file(file_path=filename, response=page_response)
