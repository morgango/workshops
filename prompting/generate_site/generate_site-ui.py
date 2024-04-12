from workshop_common import set_local_directory, get_file_contents, write_response_to_file, convert_to_filename,  execute_prompt, model_options
import ast
import streamlit as st
import pandas as pd
import re

from ragas.testset.generator import TestsetGenerator

generator = TestsetGenerator.with_openai()
testset = generator.generate_with_langchain_docs()
 
test_df = testset.to_pandas()

set_local_directory()

# from dotenv import dotenv_values
# env_values = dotenv_values(".env")

import decouple
from decouple import config

system_prompt_fn = config('SYSTEM_PROMPT_FN', default='system-prompt.txt')
user_prompt_list_fn = config('USER_PROMPT_LIST_FN', default='user-prompt-list.txt')
user_prompt_page_fn = config('USER_PROMPT_PAGE_FN', default='user-prompt-page.txt')
page_count = config('PAGES', default=25)
company_name = config('COMPANY', default='Acme Corporation')
results_fn = config('RESULTS_FN', default='results.txt')  

# system_prompt_fn = env_values['SYSTEM_PROMPT_LIST_FN'] or 'system-prompt-list.txt'
# user_prompt_list_fn = env_values['USER_PROMPT_LIST_FN'] or 'user-prompt-list.txt'
# user_prompt_page_fn = env_values['USER_PROMPT_PAGE_FN'] or 'user-prompt-page.txt'
# pages = env_values['PAGES'] or 25
# company = env_values['COMPANY'] or 'Acme Corporation'

def main():

    st.title("Site Generation Application")

    with st.expander("Advanced Options"):
        # break the buttons into three columns so they can be side by side

        # break the buttons into three columns so they can be side by side
        col1, col2, col3 = st.columns(3)
        
        with col1:
            temperature = st.number_input("Temperature:", value=0.0, step=0.1, max_value=1.0, min_value=0.0)
        
        with col2:
            model = st.selectbox("Model:", model_options)
        
        with col3:
            max_tokens = st.number_input("Max Tokens:", value=2000, step=100, max_value=2000, min_value=100)
    
    # these are arguments that can be pre-defined and passed to the simple_chat function.
    chat_args = {
        'temperature': temperature,
        'model': model,
        'max_tokens': max_tokens,
    }

    # Read in default values from the system-prompt.txt and user-prompt.txt files
    system_prompt_raw = get_file_contents(system_prompt_fn)
    system_prompt = st.text_area("Enter System Prompt:",value=system_prompt_raw, height=100, max_chars=None, key=None)

    # system_prompt_list_raw = get_file_contents(system_prompt_fn)
    # system_prompt_list = st.text_area("Enter System Prompt:",value=system_prompt_list_raw, height=100, max_chars=None, key=None)

    user_prompt_list_raw = get_file_contents(user_prompt_list_fn)
    user_prompt_page_raw = get_file_contents(user_prompt_page_fn)
    pages = st.number_input("Number of Pages to Generate:", value=page_count, step=1, min_value=1, max_value=100)   
    company = st.text_input("Company Name:", value=company)
    user_list_message = st.text_area("User List Prompt:", value=user_prompt_list_raw, height=200, max_chars=None, key=None)
    user_page_message = st.text_area("User Page Prompt:", value=user_prompt_page_raw, height=200, max_chars=None, key=None)

    user_prompt_args = {
        'pages': pages,
        'company': company
    }

    
    # build our messages to send to openAI.  These should be well formed JSON with a ROLE and CONTENT
    system_message = {"role":"system", 
                    "content": system_prompt}
    user_list_message = {"role":"user",
                    "content": user_list_message}
    user_page_message = {"role":"user",
                    "content": user_page_message}
   
    if st.button("Generate Site"):

        prompt_response = execute_prompt(user_prompt=user_list_message, 
                                        user_prompt_vars=user_prompt_args,
                                        system_prompt=system_message, 
                                        chat_args=chat_args)

        # Write response to a file
        write_response_to_file(file_path=results_fn, response=prompt_response)

        # Turn the response back into a list
        response_text = prompt_response.choices[0].message.content
        extracted_list = re.search(r'\[.*\]', response_text, flags=re.DOTALL)

        if extracted_list:
            extracted_list = extracted_list.group()

        page_list = ast.literal_eval(extracted_list)

        # generate individual pages
        for page in page_list:

            user_prompt_args = {}
            user_prompt_args['subject'] = page

            page_response = execute_prompt(user_prompt=user_page_message, 
                                        user_prompt_vars=user_prompt_args,
                                        system_prompt=system_message, 
                                        chat_args=chat_args)
            
            page_as_file = convert_to_filename(page)
            filename = f"site/{page_as_file}"
            
            write_response_to_file(file_path=filename, response=page_response)


if __name__ == "__main__":
    main()