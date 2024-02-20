from workshop_common import simple_chat
import streamlit as st

def build_prompt_args(variable_names):
    result = {}
    for var_name in variable_names:
        value = st.session_state.get(var_name)
        result[var_name] = value

    return result

def execute_prompt(user_prompt="", 
                system_prompt="",
                prompt_vars={}, 
                chat_args={}):

    # Customize user message with subject, hero, and location
    user_message_formatted = user_prompt.format(**prompt_vars)

    # Create system and user messages
    system_message = {"role": "system", "content": system_prompt}
    user_message = {"role": "user", "content": user_message_formatted}

    # Get response from OpenAI
    story_response = simple_chat(messages=[system_message, user_message], **chat_args)

    return story_response


