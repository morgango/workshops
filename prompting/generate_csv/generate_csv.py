from common import set_local_directory, simple_chat, get_file_contents, write_response_to_file, append_line_to_file

# make sure python is looking in the right spot for the files we need.
set_local_directory()

# these are arguments that can be pre-defined and passed to the simple_chat function.
# they can be changed as needed. 
simple_chat_args = {
    'temperature': 0,
    'model': 'gpt-3.5-turbo',
    'max_tokens': 2000,
}

# get the system and user messages from the files
system_message_content = get_file_contents('system-prompt.txt')
user_message_content = get_file_contents('user-prompt.txt')

# create the messages we are going to use to create the story.
system_message = {"role":"system", "content": system_message_content}
user_message = {"role":"user", "content": user_message_content}

# send the information to OpenAI and get back a response
csv_response = simple_chat(messages=[system_message, 
                                       user_message], 
                             **simple_chat_args)

# write the response to a file
write_response_to_file(file_path='results.csv', 
                       response=csv_response)