from workshop_common import simple_chat

def tell_story(user_prompt="", 
                system_prompt="",
                subject="",
                hero="",
                location="", 
                chat_args={}):

    # Customize user message with subject, hero, and location
    user_message_formatted = user_prompt.format(subject=subject, 
                                                    hero=hero, 
                                                    location=location)

    # Create system and user messages
    system_message = {"role": "system", "content": system_prompt}
    user_message = {"role": "user", "content": user_message_formatted}

    # Get response from OpenAI
    story_response = simple_chat(messages=[system_message, user_message], **chat_args)

    return story_response
