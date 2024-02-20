from workshop_common import simple_chat

def generate_csv(user_prompt="",
                   system_prompt="",
                   chat_args={}):
    
    # build our messages to send to openAI.  These should be well formed JSON with a ROLE and CONTENT
    system_message = {"role":"system", 
                    "content": system_prompt}
    user_message = {"role":"user",
                    "content": user_prompt}

    # send the information to OpenAI and get back a response
    csv_response = simple_chat(messages=[system_message, 
                                            user_message], 
                                **chat_args)
    
    return csv_response
