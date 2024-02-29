
from workshop_common import set_local_directory, simple_chat, get_file_contents, write_response_to_file, tell_story, model_options
import streamlit as st

from dotenv import dotenv_values
env_values = dotenv_values(".env")

system_prompt_fn = env_values['SYSTEM_PROMPT_FN'] or 'system-prompt.txt'
user_prompt_fn = env_values['USER_PROMPT_FN'] or 'user-prompt.txt'
results_fn = env_values['RESULTS_FN'] or 'results.txt'
hero_fn = env_values['HERO_FN'] or 'hero.txt'
subject_fn = env_values['SUBJECT_FN'] or 'subject.txt'
location_fn = env_values['LOCATION_FN'] or 'location.txt'


def main():

    st.title("Storytelling")

    with st.expander("Advanced Options"):
    # break the buttons into three columns so they can be side by side

        # break the buttons into three columns so they can be side by side
        col1, col2, col3 = st.columns(3)
        
        with col1:
            temperature = st.number_input("Temperature:", value=0.5, step=0.1, max_value=1.0, min_value=0.0)
        
        with col2:
            model = st.selectbox("Model:", model_options)
        
        with col3:
            max_tokens = st.number_input("Max Tokens:", value=2000, step=100, max_value=2000, min_value=100)
    
    # these are arguments that can be pre-defined and passed to the simple_chat function.
    simple_chat_args = {
        'temperature': temperature,
        'model': model,
        'max_tokens': max_tokens,
    }

    # break the buttons into three columns so they can be side by side
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hero_text = get_file_contents(hero_fn)
        hero = st.text_area("Hero:", value=hero_text, height=50, max_chars=None, key=None)
    
    with col2:
        subject_text = get_file_contents(subject_fn)
        subject = st.text_area("Subject:", value=subject_text, height=50, max_chars=None, key=None)
    
    with col3:
        location_text = get_file_contents(location_fn)
        location = st.text_area("Location:", value=location_text, height=50, max_chars=None, key=None)
    
    # these are arguments that can be pre-defined and passed to the simple_chat function.
    simple_chat_args = {
        'temperature': temperature,
        'model': model,
        'max_tokens': max_tokens,
    }


    # Read in default values from the system-prompt.txt and user-prompt.txt files
    system_prompt_raw = get_file_contents('system-prompt.txt')
    system_prompt = st.text_area("System Prompt:",value=system_prompt_raw, height=100, max_chars=None, key=None)

    user_prompt_raw = get_file_contents('user-prompt.txt')
    user_prompt = st.text_area("User Prompt:", value=user_prompt_raw, height=200, max_chars=None, key=None,)
    
   
    if st.button("Create a Story"):

            # Get the story response
        story_response = tell_story(user_prompt=user_prompt,
                                system_prompt=system_prompt,
                                subject=subject,
                                hero=hero,
                                location=location,
                                chat_args=simple_chat_args)
        
        # extract the response from the chat response
        response = story_response.choices[0].message.content

        # display the response on the screen
        st.text_area("Here you go:", value=response, height=200, max_chars=None, key=None)
        
        # write the results to a file
        write_response_to_file(file_path='results.txt', 
                           response=story_response)

if __name__ == "__main__":
    main()