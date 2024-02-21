from workshop_common import simple_chat
import streamlit as st
from icecream import ic

def build_prompt_args_from_session(variable_names):
    result = {}
    for var_name in variable_names:
        value = st.session_state.get(var_name)
        result[var_name] = value

    return result

def build_prompt_args_from_memory(variable_names):
    result = {}
    for var_name in variable_names:
        if var_name in globals():
            value = globals()[var_name]
            result[var_name] = value

    return result


def execute_prompt(user_prompt="", 
                system_prompt="",
                user_prompt_vars={}, 
                system_prompt_vars={}, 
                chat_args={}):

    ic("system:", system_prompt, system_prompt_vars)
    ic("user:", user_prompt, user_prompt_vars)

    # Customize user message with subject, hero, and location
    user_message_formatted = user_prompt.format(**user_prompt_vars)
    system_message_formatted = system_prompt.format(**system_prompt_vars)


    # Create system and user messages
    system_message = {"role": "system", "content": system_message_formatted}
    user_message = {"role": "user", "content": user_message_formatted}

    # Get response from OpenAI
    story_response = simple_chat(messages=[system_message, user_message], **chat_args)

    ic("response:", story_response)
    return story_response


