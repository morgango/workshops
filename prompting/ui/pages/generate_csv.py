from workshop_common import set_local_directory, get_file_contents, write_response_to_file, generate_csv,  model_options, execute_prompt, build_prompt_args_from_session
import streamlit as st
import pandas as pd
from icecream import ic

from dotenv import dotenv_values
env_values = dotenv_values(".env")

system_prompt_fn = env_values['CSV_SYSTEM_PROMPT_FN']
user_prompt_fn = env_values['CSV_USER_PROMPT_FN']
results_fn = env_values['CSV_RESULTS_FN']

def main():

    st.title("CSV Generation")

    with st.expander("Advanced Options"):

        # break the buttons into three columns so they can be side by side
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.session_state['temperature'] = st.number_input("Temperature:", value=0.5, step=0.1, max_value=1.0, min_value=0.0)
        
        with col2:
            st.session_state['model'] = st.selectbox("Model:", model_options)
        
        with col3:
            st.session_state['max_tokens'] = st.number_input("Max Tokens:", value=2000, step=100, max_value=2000, min_value=100)

    # Read in default values from the system-prompt.txt and user-prompt.txt files
    system_prompt_raw = get_file_contents(system_prompt_fn)
    system_prompt = st.text_area("Enter System Prompt:",value=system_prompt_raw, height=100, max_chars=None, key=None)

    user_prompt_raw = get_file_contents(user_prompt_fn)
    user_prompt = st.text_area("User Prompt:", value=user_prompt_raw, height=200, max_chars=None, key=None)

       
    if st.button("Generate CSV"):

        chat_variable_names = ["temperature", "model", "max_tokens"]
        chat_args = build_prompt_args_from_session(chat_variable_names)

        # get back the response from the AI
        prompt_response = execute_prompt(user_prompt=user_prompt, 
                                system_prompt=system_prompt, 
                                chat_args=chat_args)

        response = prompt_response.choices[0].message.content

        # write the results to a file
        write_response_to_file(file_path=results_fn, 
                           response=prompt_response)
        
        # Read the CSV data into a DataFrame
        csv_data = pd.read_csv(results_fn, delimiter=',')
        # Display the DataFrame as a table
        st.dataframe(csv_data)


if __name__ == "__main__":
    main()