from workshop_common import get_file_contents, write_response_to_file, model_options, execute_prompt, build_prompt_args_from_session

from dotenv import dotenv_values
env_values = dotenv_values(".env")

system_prompt_fn = env_values['STORYTELLING_SYSTEM_PROMPT_FN']
user_prompt_fn = env_values['STORYTELLING_USER_PROMPT_FN']
results_fn = env_values['STORYTELLING_RESULTS_FN']
hero_fn = env_values['STORYTELLING_HERO_FN']
subject_fn = env_values['STORYTELLING_SUBJECT_FN']
location_fn = env_values['STORYTELLING_LOCATION_FN']

def main():

    import streamlit as st

    st.title("Storytelling")

    with st.expander("Advanced Options"):

        # break the buttons into three columns so they can be side by side
        col1, col2, col3 = st.columns(3)
        
        with col1:
            hero_text = get_file_contents(hero_fn)
            st.session_state['hero'] = st.text_area("Hero:", value=hero_text, height=50, max_chars=None, key=None)
        
        with col2:
            subject_text = get_file_contents(subject_fn)
            st.session_state['subject'] = st.text_area("Subject:", value=subject_text, height=50, max_chars=None, key=None)
        
        with col3:
            location_text = get_file_contents(location_fn)
            st.session_state['location'] = st.text_area("Location:", value=location_text, height=50, max_chars=None, key=None)
        
    
    # Read in default values from the system-prompt.txt and user-prompt.txt files
    system_prompt = get_file_contents(system_prompt_fn)
    system_message_content = st.text_area("System Prompt:",value=system_prompt, height=100, max_chars=None, key=None)

    user_prompt = get_file_contents(user_prompt_fn)
    user_message_string = st.text_area("User Prompt:", value=user_prompt, height=200, max_chars=None, key=None,)
    
   
    if st.button("Create a Story"):

        chat_variable_names = ["temperature", "model", "max_tokens"]
        chat_args = build_prompt_args_from_session(chat_variable_names)

        # define the variables that we want to pass to the prompt
        variable_names = ["subject", 
                          "hero", 
                          "location"]
        
        # turn into a dictionary ready for substitution
        prompt_args = build_prompt_args_from_session(variable_names)

        # get back the response from the AI
        story_response = execute_prompt(user_prompt=user_prompt, 
                                system_prompt=system_prompt, 
                                user_prompt_vars=prompt_args,
                                chat_args=chat_args)
                
        # extract the response from the chat response
        response = story_response.choices[0].message.content

        # display the response on the screen
        st.text_area("Here you go:", value=response, height=200, max_chars=None, key=None)
        
        # write the results to a file
        write_response_to_file(file_path=results_fn, 
                           response=story_response)

if __name__ == "__main__":
    main()