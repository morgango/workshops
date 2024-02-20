from workshop_common import set_local_directory, simple_chat, get_file_contents, write_response_to_file, model_options, execute_prompt
import streamlit as st
import pandas as pd
from icecream import ic

design_type="refined"

set_local_directory()

from dotenv import dotenv_values
env_values = dotenv_values(".env")

system_prompt_fn = env_values['SYSTEM_PROMPT_FN'] or 'system-prompt.txt'
user_prompt_fn = env_values['USER_PROMPT_FN'] or f'user-prompt-{design_type}.txt'
results_fn = env_values['RESULTS_FN'] or f'results-{design_type}.txt'
location_fn = env_values['LOCATION_FN'] or 'location.txt'
format_fn = env_values['FORMAT_FN'] or 'format.txt'
length_fn = env_values['LENGTH_FN'] or 'length.txt'
mentions_fn = env_values['MENTIONS_FN'] or 'mentions.txt'

def main():

    st.title("Designing a Refined Prompt")

    with st.expander("Advanced Options"):
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

    
    with st.expander("Prompt Options"):
    # break the buttons into three columns so they can be side by side

        # break the buttons into three columns so they can be side by side
        col1, col2  = st.columns(2)
        
        with col1:
            location_text = get_file_contents('location.txt')
            location = st.text_area("Location:", value=location_text, height=50, max_chars=None, key=None)

            format_text = get_file_contents('format.txt')
            format = st.text_area("Format", value=format_text, height=50, max_chars=None, key=None)

        with col2:
            length_text = get_file_contents('length.txt')
            length = st.text_area("Length:", value=length_text, height=50, max_chars=None, key=None)

            mentions_text = get_file_contents('mentions.txt')
            mentions = st.text_area("mentions:", value=mentions_text, height=50, max_chars=None, key=None)

    # Read in default values from the system-prompt.txt and user-prompt.txt files
    system_prompt = get_file_contents('system-prompt.txt')
    system_message_content = st.text_area("Enter System Prompt:",value=system_prompt, height=100, max_chars=None, key=None)

    
    # build our messages to send to openAI.  These should be well formed JSON with a ROLE and CONTENT
    system_message = {"role":"system", 
                    "content": system_message_content}
   
    user_prompt = get_file_contents('user-prompt-refined.txt')
    user_message_string = st.text_area("User Prompt:", value=user_prompt, height=200, max_chars=None, key=None)

    if st.button("Generate Response"):

        prompt_args = {'location': location,
                          'format': format,
                          'length': length,
                          'mentions': mentions}

        prompt_response = execute_prompt(user_prompt=user_message_string, 
                                        system_prompt=system_message_content, 
                                        prompt_vars=prompt_args, 
                                        chat_args=chat_args)
        
        # extract the response from the chat response
        response = prompt_response.choices[0].message.content

        # write the results to a file
        write_response_to_file(file_path=results_fn, 
                           response=prompt_response)
        
        paragraphs = get_file_contents(results_fn, return_as_list=True)

        for paragraph in paragraphs:
            st.write(paragraph)

        ic(response)


if __name__ == "__main__":
    main()