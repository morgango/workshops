from workshop_common import set_local_directory, get_file_contents, write_response_to_file, execute_prompt, model_options, build_prompt_args_from_session
import streamlit as st
import pandas as pd
from icecream import ic

from dotenv import dotenv_values
env_values = dotenv_values(".env")

system_prompt_fn = env_values['DESIGNING_SYSTEM_PROMPT_FN']
user_prompt_fn = env_values['DESIGNING_SIMPLE_USER_PROMPT_FN']
results_fn = env_values['DESIGNING_RESULTS_FN']
location_fn = env_values['DESIGNING_LOCATION_FN']
format_fn = env_values['DESIGNING_FORMAT_FN']
length_fn = env_values['DESIGNING_LENGTH_FN']
mentions_fn = env_values['DESIGNING_MENTIONS_FN']
instructions_fn = env_values['DESIGNING_INSTRUCTIONS_FN']
shots_fn = env_values['DESIGNING_SHOTS_FN']
start_fn = env_values['DESIGNING_START_FN']
nickname_fn = env_values['DESIGNING_NICKNAME_FN']

def main():

    import streamlit as st

    is_simple = True

    st.title("Designing Prompts")

    with st.expander("Advanced Options"):
        # break the buttons into three columns so they can be side by side
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.session_state['temperature'] = st.number_input("Temperature:", value=0.5, step=0.1, max_value=1.0, min_value=0.0)
        
        with col2:
            st.session_state['model'] = st.selectbox("Model:", model_options)
        
        with col3:
            st.session_state['max_tokens'] = st.number_input("Max Tokens:", value=2000, step=100, max_value=2000, min_value=100)

    # there are three input states.
    st.session_state['design'] = st.selectbox("Design State:", ["Simple", "Refined", "Complete"])

    is_simple = st.session_state['design'] == "Simple"
    is_refined = st.session_state['design'] == "Refined"
    is_complete = st.session_state['design'] == "Complete"
                                                 
    with st.expander("Prompt Options"):
        # break the inputs into three columns so they can be side by side.
        # only make them usable when in the right state.
        col1, col2 = st.columns(2)
                    
        with col1:
            location_text = get_file_contents(location_fn)
            st.session_state['location'] = st.text_area("Location:", 
                                                        value=location_text, 
                                                        height=50, 
                                                        max_chars=None, 
                                                        key=None,
                                                        disabled=False)

            format_text = get_file_contents(format_fn)
            st.session_state['format'] = st.text_area("Format:", 
                                                        value=format_text, 
                                                        height=50, 
                                                        max_chars=None, 
                                                        key=None,
                                                        disabled=is_simple)

            nickname_text = get_file_contents(nickname_fn)
            st.session_state['nickname'] = st.text_area("Nickname:", 
                                                        value=nickname_text, 
                                                        height=50, 
                                                        max_chars=None, 
                                                        key=None,
                                                        disabled=is_simple or is_refined)

        with col2:
            length_text = get_file_contents(length_fn)
            st.session_state['length'] = st.text_area("Length:", 
                                                        value=length_text, 
                                                        height=50, 
                                                        max_chars=None, 
                                                        key=None,
                                                        disabled=is_simple)

            mentions_text = get_file_contents(mentions_fn)
            st.session_state['mentions'] = st.text_area("Mentions:", 
                                                        value=mentions_text, 
                                                        height=50, 
                                                        max_chars=None, 
                                                        key=None,
                                                        disabled=is_simple)

            start_text = get_file_contents(start_fn)
            st.session_state['start'] = st.text_area("Start:", 
                                                        value=start_text, 
                                                        height=50, 
                                                        max_chars=None, 
                                                        key=None,
                                                        disabled=is_simple or is_refined)

        instructions_text = get_file_contents(instructions_fn)
        st.session_state['instructions'] = st.text_area("Instructions:", 
                                                    value=instructions_text, 
                                                    height=50, 
                                                    max_chars=None, 
                                                    key=None,
                                                    disabled=is_simple or is_refined)

        shots_text = get_file_contents(shots_fn)
        st.session_state['shots'] = st.text_area("Shots:", 
                                                    value=shots_text, 
                                                    height=50, 
                                                    max_chars=None, 
                                                    key=None,
                                                    disabled=is_simple or is_refined)


    # Read in default values from the system and user prompts
    system_prompt_raw = get_file_contents(system_prompt_fn)
    system_prompt = st.text_area("Enter System Prompt:",value=system_prompt_raw, height=100, max_chars=None, key=None)

    # choose the user prompt based on the design state
    if is_simple:
            user_prompt_fn = env_values['DESIGNING_SIMPLE_USER_PROMPT_FN']
    elif is_refined:
            user_prompt_fn = env_values['DESIGNING_REFINED_USER_PROMPT_FN']
    elif is_complete:
            user_prompt_fn = env_values['DESIGNING_COMPLETE_USER_PROMPT_FN']

    user_prompt_raw = get_file_contents(user_prompt_fn)
    user_prompt = st.text_area("User Prompt:", value=user_prompt_raw, height=200, max_chars=None, key=None)


    if st.button("Generate Response"):

        chat_variable_names = ["temperature", "model", "max_tokens"]
        chat_args = build_prompt_args_from_session(chat_variable_names)

        # get the variable names for the prompt
        variable_names = []

        if is_simple:
            variable_names = ["location"]
        elif is_refined:
            variable_names = ["location", 
                                "format", 
                                "length", 
                                "mentions"]
        elif is_complete:
            variable_names = ["location", 
                                "format", 
                                "length", 
                                "mentions", 
                                "instructions",
                                "shots",
                                "start",
                                "nickname"]
        
        # turn into a dictionary ready for substitution
        prompt_args = build_prompt_args_from_session(variable_names)

        # get back the response from the AI
        prompt_response = execute_prompt(user_prompt=user_prompt, 
                                system_prompt=system_prompt, 
                                user_prompt_vars=prompt_args,
                                chat_args=chat_args)
        
        # extract the response from the chat response
        response = prompt_response.choices[0].message.content

        # write the results to a file
        write_response_to_file(file_path=results_fn, 
                            response=prompt_response)
        
        paragraphs = get_file_contents(results_fn, return_as_list=True)

        for paragraph in paragraphs:
            st.write(paragraph)

        

if __name__ == "__main__":
    main()