from workshops_common import set_local_directory, simple_chat, get_file_contents, write_response_to_file
import streamlit as st
import pandas as pd

set_local_directory()


model_options = ['gpt-3.5-turbo', 'gpt-4.0', 'gpt-4.5']

def main():

    st.title("Designing a Simple Prompt")

    with st.expander("Advanced Options"):
        # break the buttons into three columns so they can be side by side
        col1, col2, col3 = st.columns(3)
        
        with col1:
            temperature = st.number_input("Temperature:", value=0.0, step=0.1, max_value=1.0, min_value=0.0)
        
        with col2:
            model_options = ['gpt-3.5-turbo', 'gpt-4.0', 'gpt-4.5']
            model = st.selectbox("Model:", model_options)
        
        with col3:
            max_tokens = st.number_input("Max Tokens:", value=2000, step=100, max_value=2000, min_value=100)
    
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

        user_message_content = user_message_string.format(location=location,
                                                          format=format,
                                                         length=length,
                                                         mentions=mentions)

        user_message = {"role":"user",
                        "content": user_message_content}

        # send the information to the LLM and get back a response
        chat_response = simple_chat(messages=[system_message, 
                                         user_message], 
                               **simple_chat_args)

        # extract the response from the chat response
        response = chat_response.choices[0].message.content

        # write the results to a file
        write_response_to_file(file_path='results-refined.txt', 
                           response=chat_response)
        
        paragraphs = get_file_contents('results-refined.txt', return_as_list=True)

        for paragraph in paragraphs:
            print(paragraph)
            st.write(paragraph)


if __name__ == "__main__":
    main()