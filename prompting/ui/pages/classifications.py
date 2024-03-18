from workshop_common import get_file_contents, write_response_to_file, execute_prompt, model_options, build_prompt_args_from_session
import streamlit as st
import pandas as pd
from icecream import ic

from dotenv import dotenv_values
env_values = dotenv_values(".env")

system_prompt_fn = env_values['CLASSIFICATION_SYSTEM_PROMPT_FN']
user_prompt_fn = env_values['CLASSIFICATION_USER_PROMPT_FN']
items_fn = env_values['CLASSIFICATION_ITEMS_FN']
buckets_fn = env_values['CLASSIFICATION_BUCKETS_FN']
results_fn = env_values['CLASSIFICATION_RESULTS_FN']

def main():

    import streamlit as st

    is_simple = True

    st.title("Classifying Items")

    with st.expander("Advanced Options"):
        # break the buttons into three columns so they can be side by side
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.session_state['temperature'] = st.number_input("Temperature:", value=0.5, step=0.1, max_value=1.0, min_value=0.0)
        
        with col2:
            st.session_state['model'] = st.selectbox("Model:", model_options)
        
        with col3:
            st.session_state['max_tokens'] = st.number_input("Max Tokens:", value=2000, step=100, max_value=2000, min_value=100)

    with st.expander("Prompt Options"):
        # break the inputs into three columns so they can be side by side.
        # only make them usable when in the right state.
        col1, col2 = st.columns(2)
                    
        with col1:
            items_list = get_file_contents(file_path=items_fn, return_as_list=True, strip_newline=True)
            items_text = "\n".join(["- " + item for item in items_list])

            st.session_state['items'] = st.text_area("Items:", 
                                                        value=items_text, 
                                                        height=250, 
                                                        max_chars=None, 
                                                        key=None)

        with col2:
            buckets_list = get_file_contents(file_path=buckets_fn, return_as_list=True, strip_newline=True)
            buckets_text = "\n".join(["- " + bucket for bucket in buckets_list])
            st.session_state['buckets'] = st.text_area("Buckets:", 
                                                        buckets_text, 
                                                        height=250, 
                                                        max_chars=None, 
                                                        key=None)

    # Read in default values from the system and user prompts
    system_prompt_raw = get_file_contents(system_prompt_fn)
    system_prompt = st.text_area("System Prompt:",value=system_prompt_raw, height=250, max_chars=None, key=None)

    user_prompt_raw = get_file_contents(user_prompt_fn)
    user_prompt = st.text_area("User Prompt:", value=user_prompt_raw, height=200, max_chars=None, key=None)


    if st.button("Generate Response"):

        chat_variable_names = ["temperature", "model", "max_tokens"]
        chat_args = build_prompt_args_from_session(chat_variable_names)

        user_variable_names = ["items"]
        system_variable_names = ["buckets"]
        
        # turn into a dictionary ready for substitution
        user_prompt_args = build_prompt_args_from_session(user_variable_names)
        system_prompt_args = build_prompt_args_from_session(system_variable_names)

        # get back the response from the AI
        prompt_response = execute_prompt(user_prompt=user_prompt, 
                                system_prompt=system_prompt, 
                                user_prompt_vars=user_prompt_args,
                                system_prompt_vars=system_prompt_args,
                                chat_args=chat_args)
        
        # extract the response from the chat response
        response = prompt_response.choices[0].message.content

        # write the results to a file
        write_response_to_file(file_path=results_fn, 
                            response=prompt_response)
        
        paragraphs = get_file_contents(results_fn, return_as_list=True, strip_newline=True)

        for paragraph in paragraphs:
            st.write(paragraph)        

if __name__ == "__main__":
    main()