from workshop_common import set_local_directory, simple_chat, get_file_contents, write_response_to_file, generate_csv,  model_options
import streamlit as st
import pandas as pd

set_local_directory()

from dotenv import dotenv_values
env_values = dotenv_values(".env")

system_prompt_fn = env_values['SYSTEM_PROMPT_FN'] or 'system-prompt.txt'
user_prompt_fn = env_values['USER_PROMPT_FN'] or 'user-prompt.txt'
results_fn = env_values['RESULTS_FN'] or 'results.txt'

def main():

    st.title("CSV Generation Application")

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

    user_prompt_raw = get_file_contents(user_prompt_fn)
    user_message = st.text_area("User Prompt:", value=user_prompt_raw, height=200, max_chars=None, key=None)

    
    # build our messages to send to openAI.  These should be well formed JSON with a ROLE and CONTENT
    system_message = {"role":"system", 
                    "content": system_message}
    user_message = {"role":"user",
                    "content": user_message}
   
    if st.button("Generate CSV"):

        # send the information to OpenAI and get back a response
        csv_response = generate_csv(system_prompt=system_message, 
                                    user_prompt=user_message, 
                                    chat_args=chat_args)

        # extract the response from the chat response
        response = csv_response.choices[0].message.content

        # write the results to a file
        write_response_to_file(file_path=results_fn, 
                           response=csv_response)
        
        # Read the CSV data into a DataFrame
        csv_data = pd.read_csv(results_fn, delimiter=',')
        # Display the DataFrame as a table
        st.dataframe(csv_data)


if __name__ == "__main__":
    main()