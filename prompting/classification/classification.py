from workshop_common import set_local_directory, simple_chat, get_file_contents, write_response_to_file, execute_prompt, build_prompt_args_from_memory
from icecream import ic 

from dotenv import dotenv_values
env_values = dotenv_values(".env")

ic(env_values)
# make sure python is looking in the right spot for the files we need.
set_local_directory()

system_prompt_fn = env_values['SYSTEM_PROMPT_FN']
user_prompt_fn = env_values['USER_PROMPT_FN']
items_fn = env_values['ITEMS_FN']
buckets_fn = env_values['BUCKETS_FN']
results_fn = env_values['RESULTS_FN']

temperature = 0
model = 'gpt-3.5-turbo'
max_tokens = 2000

items_list = get_file_contents(file_path=items_fn, return_as_list=True, strip_newline=True)
items = "\n".join(["- " + item for item in items_list])

buckets_list = get_file_contents(file_path=buckets_fn, return_as_list=True, strip_newline=True)
buckets = "\n".join(["- " + bucket for bucket in buckets_list])

system_prompt_raw = get_file_contents(system_prompt_fn)
user_prompt_raw = get_file_contents(user_prompt_fn)

# Specify the variable names you want to extract from memory
user_variable_names = ["items"]
user_prompt_args = build_prompt_args_from_memory(user_variable_names)

ic(user_variable_names, user_prompt_args)

system_variable_names = ["buckets"]
system_prompt_args = build_prompt_args_from_memory(system_variable_names)
ic(system_variable_names, system_prompt_args)

chat_variable_names = ["temperature", "model", "max_tokens"]
chat_args = build_prompt_args_from_memory(chat_variable_names)

user_variable_names = ["items"]
system_variable_names = ["buckets"]

# turn into a dictionary ready for substitution
user_prompt_args = build_prompt_args_from_memory(user_variable_names)
system_prompt_args = build_prompt_args_from_memory(system_variable_names)

# get back the response from the AI
prompt_response = execute_prompt(user_prompt=user_prompt_raw, 
                        system_prompt=system_prompt_raw, 
                        user_prompt_vars=user_prompt_args,
                        system_prompt_vars=system_prompt_args,
                        chat_args=chat_args)

# extract the response from the chat response
response = prompt_response.choices[0].message.content

# write the results to a file
write_response_to_file(file_path=results_fn, 
                    response=prompt_response)



