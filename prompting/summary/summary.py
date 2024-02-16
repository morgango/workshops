from workshops_common import set_local_directory, simple_chat, get_file_contents, get_file_size, write_response_to_file
from icecream import ic

# make sure python is looking in the right spot for the files we need.
set_local_directory()


# these are arguments that can be pre-defined and passed to the simple_chat function.
# they can be changed as needed. 
simple_chat_args = {
    'temperature': 0,
    'model': 'gpt-3.5-turbo',
    'max_tokens': 2000,
}

# Get a really long file to deal with
user_message_content = get_file_contents('user-prompt.txt')

# Tell how to deal with the file
system_message_content = get_file_contents('system-prompt.txt')
 
# build our messages to send to openAI.  These should be well formed JSON with a ROLE and CONTENT
system_message = {"role":"system", 
                  "content": system_message_content}
user_message = {"role":"user",
                "content": user_message_content}

# send the information to OpenAI and get back a response
summary_response = simple_chat(messages=[system_message, 
                                         user_message], 
                               **simple_chat_args)


# write the response to a file
write_response_to_file(file_path='results.txt', 
                       response=summary_response)

# get the size of the prompt and the result
prompt_size = get_file_size('user-prompt.txt')
result_size = get_file_size('results.txt')

ic(prompt_size, result_size)
